-- 우리 방 요정 저장소 (Supabase 프로젝트 third-roommate에 이미 적용됨)
create table public.docs (
  path text primary key,          -- 예: rooms/ABC123/cards/s0
  room text not null,             -- 방 코드 (실시간 구독 필터)
  parent text not null,
  data jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);
create index docs_room_idx on public.docs(room);
alter table public.docs enable row level security;
create policy "docs read" on public.docs for select to anon, authenticated using (true);
create policy "docs insert" on public.docs for insert to anon, authenticated with check (path like 'rooms/%' and room = split_part(path,'/',2) and length(path) < 200 and pg_column_size(data) < 60000);
create policy "docs update" on public.docs for update to anon, authenticated using (true) with check (path like 'rooms/%' and room = split_part(path,'/',2) and pg_column_size(data) < 60000);
create or replace function public.doc_merge(p text, patch jsonb) returns boolean
language plpgsql security invoker set search_path = public as $$
declare n int;
begin
  update public.docs set data = data || patch, updated_at = now() where path = p;
  get diagnostics n = row_count;
  return n > 0;
end $$;
alter publication supabase_realtime add table public.docs;
-- AI 호출 하루 상한 카운터 (서버 함수만 씀)
create table public.ai_usage (day date primary key, n int not null default 0);
alter table public.ai_usage enable row level security;
create or replace function public.ai_tick(cap int) returns boolean
language plpgsql security definer set search_path = public as $$
declare c int;
begin
  insert into public.ai_usage(day,n) values (current_date,1)
  on conflict (day) do update set n = ai_usage.n + 1 returning n into c;
  return c <= cap;
end $$;
revoke execute on function public.ai_tick(int) from public, anon, authenticated;
grant execute on function public.ai_tick(int) to service_role;
