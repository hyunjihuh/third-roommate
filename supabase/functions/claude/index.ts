// 브라우저 대신 LLM API를 부른다. 키는 Edge Function Secret에만 둔다.
// OPENAI_KEY(또는 OPENAI_API_KEY)가 있으면 OpenAI, ANTHROPIC_API_KEY가 있으면 Claude.
// GET -> {ok, provider}, POST {prompt, tier} -> {json}
import { createClient } from "jsr:@supabase/supabase-js@2";
const DAILY_CAP = 1500;
const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
};
const out = (o: unknown, status = 200) => new Response(JSON.stringify(o), { status, headers: { ...cors, "Content-Type": "application/json" } });
const openaiKey = () => Deno.env.get("OPENAI_KEY") || Deno.env.get("OPENAI_API_KEY") || "";
const anthropicKey = () => Deno.env.get("ANTHROPIC_API_KEY") || "";
const parse = (text: string) => { const m = text.match(/\{[\s\S]*\}/); try { return m ? JSON.parse(m[0]) : null; } catch (_) { return null; } };

async function viaOpenAI(key: string, prompt: string, tier?: string) {
  const pref = tier === "quick" ? (Deno.env.get("OPENAI_MODEL_QUICK") || "gpt-4.1-mini") : (Deno.env.get("OPENAI_MODEL") || "gpt-4.1");
  const tries = [...new Set([pref, "gpt-4o-mini"])];
  let last = "upstream";
  for (const model of tries) {
    const r = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: { "content-type": "application/json", authorization: "Bearer " + key },
      body: JSON.stringify({
        model, temperature: 0.2, max_tokens: 1200, response_format: { type: "json_object" },
        messages: [{ role: "system", content: "지시를 따르고, [출력]에 적힌 모양의 JSON 객체 하나만 답한다. 다른 글은 쓰지 않는다." }, { role: "user", content: prompt }],
      }),
    });
    const data = await r.json().catch(() => ({}));
    if (r.ok) return { json: parse(data?.choices?.[0]?.message?.content || "") };
    last = data?.error?.message || String(r.status);
    if (r.status !== 404 && data?.error?.code !== "model_not_found") break;
  }
  return { error: last };
}
async function viaClaude(key: string, prompt: string, tier?: string) {
  const r = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "content-type": "application/json", "x-api-key": key, "anthropic-version": "2023-06-01" },
    body: JSON.stringify({ model: tier === "quick" ? "claude-haiku-4-5-20251001" : "claude-sonnet-5-5", max_tokens: 1200, messages: [{ role: "user", content: prompt }] }),
  });
  const data = await r.json().catch(() => ({}));
  if (!r.ok) return { error: data?.error?.message || String(r.status) };
  return { json: parse((data.content || []).map((c: { text?: string }) => c.text || "").join("")) };
}

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  const ok = openaiKey(), ak = anthropicKey();
  const provider = ok ? "openai" : ak ? "anthropic" : null;
  if (req.method === "GET") return out({ ok: !!provider, provider });
  if (req.method !== "POST") return out({ error: "method" }, 405);
  if (!provider) return out({ error: "no key" }, 503);
  let body: { prompt?: unknown; tier?: string } = {};
  try { body = await req.json(); } catch (_) { return out({ error: "bad json" }, 400); }
  const prompt = body.prompt;
  if (!prompt || typeof prompt !== "string" || prompt.length > 20000) return out({ error: "bad prompt" }, 400);
  try {
    const admin = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
    const { data: okToday } = await admin.rpc("ai_tick", { cap: DAILY_CAP });
    if (okToday === false) return out({ error: "daily cap" }, 429);
  } catch (_) { /* 카운터가 실패해도 응답은 한다 */ }
  try {
    const res = provider === "openai" ? await viaOpenAI(ok, prompt, body.tier) : await viaClaude(ak, prompt, body.tier);
    if ("error" in res) return out({ error: res.error }, 502);
    return out({ json: res.json });
  } catch (e) {
    return out({ error: String(e) }, 500);
  }
});
