(()=>{
const store=new Map();const subs=[];let n=0;
const clone=o=>JSON.parse(JSON.stringify(o));
const notify=()=>setTimeout(()=>subs.forEach(f=>f()),0);
function snapDoc(path){const d=store.get(path);return {exists:!!d,id:path.split('/').pop(),data:()=>d?clone(d):undefined}}
function docRef(path){return {id:path.split('/').pop(),path,
 get:async()=>snapDoc(path),
 set:async(v)=>{store.set(path,clone(v));notify()},
 update:async(v)=>{if(!store.has(path))throw {code:'not-found'};store.set(path,{...store.get(path),...clone(v)});notify()},
 onSnapshot:(cb)=>{const f=()=>cb(snapDoc(path));subs.push(f);f();return()=>{}}}}
function coll(path,ord,lim){const q={
 doc:(id)=>docRef(path+'/'+(id||('id'+(++n)+Math.random().toString(36).slice(2,6)))),
 add:async(v)=>{const r=q.doc();await r.set(v);return r},
 orderBy:(k,dir)=>coll(path,[k,dir],lim),limit:(l)=>coll(path,ord,l),
 onSnapshot:(cb)=>{const f=()=>{let docs=[...store.keys()].filter(k=>k.startsWith(path+'/')&&k.slice(path.length+1).indexOf('/')<0).map(k=>({id:k.split('/').pop(),data:()=>clone(store.get(k))}));if(ord){docs.sort((a,b)=>(a.data()[ord[0]]-b.data()[ord[0]])*(ord[1]==='desc'?-1:1))}if(lim)docs=docs.slice(0,lim);cb({docs})};subs.push(f);f();return()=>{}}};return q}
const db={doc:docRef,collection:(p)=>coll(p)};
window.__prompts=[];
const sample={json:async(p)=>{window.__prompts.push(p);await new Promise(r=>setTimeout(r,60));
 if(p.includes('[C0'))return p.split('<private_complaint>')[1].split('</private_complaint>')[0].includes('(')?{draft:"아침 7시 반에 드라이기 소리 때문에 깨는 날이 있어. 평일 아침엔 욕실에서 말려줄 수 있어?",clarification:"",missing_fields:[],key_facts:["평일 아침","7:30","드라이기","욕실"],unsafe:false}:{draft:"",clarification:"보통 몇 시쯤이야?",missing_fields:["time"],key_facts:[]};
 if(p.includes('[C1')){const req=p.split('<request>')[1];const g=(p.match(/id: (g_\S+)/)||[])[1];
   if(req.includes('드라이기'))return {kind:"request",route:"coordination_needed",evidence_ids:[],missing_fields:[],reason:"상대가 하는 일을 바꿔 달라는 부탁이에요."};
   if(req.includes('스터디룸')&&g)return {kind:"permission",action:"스터디룸에서 과외",time:"내일 아침 8시",duration:"1시간",route:"covered_by_agreement",evidence_ids:[g],missing_fields:[],hour:8,minutes:60,reason:"지난번에 같이 만든 카드와 같은 내용이에요.",unsafe:false};
   if(req.includes('통화'))return {kind:"permission",action:"방에서 통화",time:"지금",duration:"10분",route:"covered_by_agreement",evidence_ids:["s2"],missing_fields:[],clarification:"",hour:22,minutes:10,weekend:false,reason:"통화 카드가 둘 다 O이고 23시 전, 15분 이내 조건 안이에요.",unsafe:false};
   if(req.includes('친구')&&!req.includes('('))return {kind:"permission",route:"clarification_needed",evidence_ids:["s4"],missing_fields:["time"],clarification:"몇 시까지 있을 예정이에요?",reason:"끝나는 시간이 없어요."};
   return {kind:"permission",action:"방에서 과외",time:"내일 아침 8시",duration:"1시간",route:"coordination_needed",evidence_ids:[],missing_fields:[],hour:8,minutes:60,reason:"과외는 정해둔 카드가 없어요.",unsafe:false};}
 if(p.includes('[C2'))return {questions:["아침에 꼭 지켜야 하는 건 뭐야?","바꿀 수 있는 건 있어?"],unresolved_fields:[]};
 if(p.includes('[C3')){const own=p.match(/\[owner_id\] (\w)/)[1];const parts=p.split('source_id: ').slice(1);return {constraints:parts.map((x,i)=>({owner_id:own,condition:(x.match(/답: (.*)/)||[])[1]||"",flexibility:"preference",source_id:"q"+i,sharing_status:x.includes('UI 공유 동의: shared')?"shared":"private"})),clarification_needed:[]};}
 if(p.includes('[C4'))return {status:"ok",options:[{option_id:"o1",action:"과외는 거실 스터디룸에서",time_place:"내일 8시, 스터디룸",adjustments_by_person:{A:"장소를 옮김",B:""},constraint_ids:["B0"],open_questions:[]},{option_id:"o2",action:"9시로 미뤄서 방에서",time_place:"내일 9시, 방",adjustments_by_person:{A:"시간을 한 시간 미룸",B:""},constraint_ids:[],open_questions:["학생이 9시 가능한지"]},{option_id:"o3",action:"8시에 방에서, B는 이어플러그",time_place:"내일 8시, 방",adjustments_by_person:{A:"",B:"이어플러그 사용"},constraint_ids:[],open_questions:[]}]};
 if(p.includes('[C6'))return {status:"confirmed",agreement_text:"내일 아침 8시 과외는 A가 스터디룸에서 해요. 1주 해보고 다시 봐요.",option_version:1,review_date:"10/14"};
 if(p.includes('[C7'))return {status:"proposal",proposed_card:{category:"방 사용",title:"아침 9시 전 방에서 과외",conditions:"9시 이후는 방에서",exceptions:""},rationale:"아침 과외가 또 생길 수 있어요.",source_case_id:"x"};
 if(p.includes('[전달 말투'))return {text:p.includes('직설적이고')?"내일 아침 8시, 방에서 과외 1시간. 괜찮아?":"혹시 내일 아침 8시에 방에서 1시간쯤 과외해도 괜찮을까?"};
 return {};}};
window.claude={use:async(n)=>n==='db'?db:n==='sample'?sample:n==='downloads'?{save:async()=>{}}:null};
try{localStorage.clear()}catch(e){}
})();
