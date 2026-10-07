// Supabase 흉내: 저장소 연결 코드(supaDB)가 맞게 도는지 네트워크 없이 확인하는 용도
(()=>{
const rows=new Map();const chans=[];
const emit=row=>setTimeout(()=>chans.forEach(c=>{if(c.filter==="room=eq."+row.room)c.cb({new:JSON.parse(JSON.stringify(row))})}),30);
function q(){const st={f:[],single:false,lim:null};const api={
  select(){return api},eq(k,v){st.f.push([k,v]);return api},limit(n){st.lim=n;return api},maybeSingle(){st.single=true;return api},
  then(res){let d=[...rows.values()].filter(r=>st.f.every(([k,v])=>r[k]===v)).map(r=>JSON.parse(JSON.stringify(r)));if(st.lim)d=d.slice(0,st.lim);res({data:st.single?(d[0]||null):d,error:null})},
  upsert(r){rows.set(r.path,JSON.parse(JSON.stringify(r)));emit(r);return Promise.resolve({error:null})}};return api}
window.supabase={createClient:()=>({from:()=>q(),
  rpc:async(n,{p,patch})=>{const r=rows.get(p);if(!r)return{data:false,error:null};r.data={...r.data,...JSON.parse(JSON.stringify(patch))};emit(r);return{data:true,error:null}},
  channel:()=>{const c={};c.on=(e,o,cb)=>{c.filter=o.filter;c.cb=cb;return c};c.subscribe=f=>{chans.push(c);setTimeout(()=>f("SUBSCRIBED"),20);return c};return c},
  removeChannel:c=>{const i=chans.indexOf(c);if(i>=0)chans.splice(i,1)}})};
const of=window.fetch;window.fetch=async(u,o)=>{if(String(u).includes("/functions/v1/claude"))return new Response(JSON.stringify({ok:false}),{status:200,headers:{"content-type":"application/json"}});return of(u,o)};
try{localStorage.clear()}catch(e){}
})();
