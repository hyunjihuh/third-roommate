(()=>{
const store=new Map();const subs=[];let n=0;
const clone=o=>JSON.parse(JSON.stringify(o));
const notify=()=>setTimeout(()=>subs.forEach(f=>f()),0);window.__del=(re)=>{for(const k of [...store.keys()])if(re.test(k))store.delete(k);notify()};
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
const sample={json:async(p)=>{window.__prompts.push(p);await new Promise(r=>setTimeout(r,window.__delay||60));
 if(p.includes('[C0')&&p.includes('치이카와'))return {draft:"토요일에 같이 치이카와 영화 보러 갈래? 예매는 내가 할게.",clarification:"",missing_fields:[],key_facts:["토요일","치이카와 영화","예매는 하늘"],unsafe:false};
 if(p.includes('[C0'))return p.split('<private_complaint>')[1].split('</private_complaint>')[0].includes('(')?{draft:"평일 아침 7시 반에 드라이기 소리 때문에 깨는 날이 있어. 그 시간엔 욕실에서 말려줄 수 있어?",clarification:"",missing_fields:[],key_facts:["평일 아침","7시 반","드라이기","욕실"],unsafe:false}:{draft:"",clarification:"보통 몇 시쯤이야?",missing_fields:["time"],key_facts:[]};
 if(p.includes('[C1')){const req=p.split('<request>')[1];const g=(p.match(/id: (g_\S+|id\S+)/)||[])[1];
   if(req.includes('치이카와'))return {kind:"request",route:"coordination_needed",evidence_ids:[],missing_fields:[],reason:"같이 하자는 제안이에요."};
   if(req.includes('3시쯤'))return {kind:"permission",action:"술 마신 뒤 새벽 귀가",time:"새벽 3시",duration:"",route:"coordination_needed",evidence_ids:[],missing_fields:[],reason:"늦은 귀가는 정한 카드가 없어서 물어봐야 해요.",unsafe:false};
   if(req.includes('가만 안'))return {kind:"permission",route:"coordination_needed",evidence_ids:[],missing_fields:[],reason:"",unsafe:true};
   if(req.includes('자고 가'))return {kind:"permission",action:"친구 자고 가기",route:"coordination_needed",evidence_ids:["r0"],missing_fields:[],reason:"외부인 숙박은 기숙사 규칙이에요.",unsafe:false};
   if(req.includes('통화 좀'))return {kind:"permission",action:"방에서 통화",time:"지금",duration:"",route:"clarification_needed",evidence_ids:["s4"],cond_check:"unknown",missing_fields:["duration"],clarification:"통화는 몇 분쯤 할 거예요?",reason:"통화 카드 조건이 15분 안이라 길이가 필요해요.",unsafe:false};
   if(req.includes('통화'))return {kind:"permission",action:"방에서 통화",time:"오늘 밤 10시",duration:"10분",route:"covered_by_agreement",evidence_ids:["s4"],cond_check:"met",missing_fields:[],hour:22,minutes:10,reason:"통화 카드에서 바다가 15분 안이면 괜찮다고 했고 10분이에요.",unsafe:false};
   if(req.includes('드라이기'))return {kind:"request",route:"coordination_needed",evidence_ids:[],missing_fields:[],reason:"룸메가 하는 일을 바꿔 달라는 부탁이에요."};
   if(req.includes('11시')&&g)return {kind:"permission",action:"스탠드 켜고 과제",time:"오늘 밤 11시까지",duration:"",route:"covered_by_agreement",evidence_ids:[g],missing_fields:[],hour:23,minutes:0,reason:"같이 만든 카드의 12시 전 범위 안이에요.",unsafe:false};
   return {kind:"permission",action:"스탠드 켜고 과제",time:"오늘 밤 12시 넘어서",duration:"1시간",route:"coordination_needed",evidence_ids:["s2"],missing_fields:[],hour:0,minutes:60,reason:"밤늦게 방에서 공부하기 카드는 바다가 먼저 물어봐 달라고 했어요.",unsafe:false};}
 if(p.includes('[C2')){const asker=p.includes('물어본 사람')||p.includes('부탁한 사람');return {questions:asker?["12시 넘어서도 꼭 방이어야 하는 이유가 있어?","시간이나 장소 중에 바꿀 수 있는 건 있어?"]:["불빛이 어느 정도면 잠이 깨?","몇 시까지는 괜찮을 것 같아?"],unresolved_fields:[]};}
 if(p.includes('[C3')){const own=p.match(/\[owner_id\] (\w)/)[1];const parts=p.split('source_id: ').slice(1);return {constraints:parts.map((x,i)=>({owner_id:own,condition:(x.match(/답: (.*)/)||[])[1]||"",flexibility:"preference",source_id:"q"+i,sharing_status:x.includes('UI 공유 동의: shared')?"shared":"private"})),clarification_needed:[]};}
 if(p.includes('[C4'))return {status:"ok",options:[{option_id:"o1",action:"12시까지는 방에서, 그 뒤엔 동방에서 과제",time_place:"평일 밤, 12시 전엔 방 / 그 뒤엔 동방",adjustments_by_person:{A:"12시 뒤엔 장소를 옮김",B:""},constraint_ids:["B0"],open_questions:[]},{option_id:"o2",action:"스탠드를 바다 침대 반대쪽으로 돌리고 방에서",time_place:"평일 밤 1시까지, 방",adjustments_by_person:{A:"스탠드 방향을 돌림",B:"1시까지 약한 불빛 감수"},constraint_ids:[],open_questions:[]},{option_id:"o3",action:"12시 넘으면 거실 스터디룸에서",time_place:"평일 밤 12시 뒤, 거실",adjustments_by_person:{A:"장소를 옮김",B:""},constraint_ids:[],open_questions:[]}]};
 if(p.includes('[C6'))return {status:"confirmed",agreement_text:"밤 12시까지는 A가 방에서 스탠드 켜고 과제, 그 뒤엔 동방에서",option_version:1,review_date:"",repeat:true,art:3};
 if(p.includes('[C7'))return {status:"no_proposal"};
 if(p.includes('[전달 말투')&&p.includes('3시쯤'))return {text:"혹시 오늘 술을 마시고 새벽 3시쯤 들어가도 괜찮을까? 최대한 조용히 들어갈게. 미안해."};
 if(p.includes('[전달 말투')&&p.includes('치이카와'))return {text:"토요일에 같이 치이카와 영화 보러 갈래? 예매는 내가 할게."};
 if(p.includes('[전달 말투'))return {text:p.includes('드라이기')?"혹시 평일 아침 7시 반엔 욕실에서 드라이기 써줄 수 있을까? 그때 소리 때문에 깨는 날이 있어.":p.includes('알림일 때')&&p.includes('11시')?"오늘 밤 11시까지 스탠드 켜고 과제할게.":"혹시 오늘 밤 12시 넘어서 스탠드 켜고 1시간쯤 과제해도 괜찮을까?"};
 return {};}};
window.claude={use:async(n)=>n==='db'?db:n==='sample'?sample:n==='downloads'?{save:async()=>{}}:null};
try{localStorage.clear()}catch(e){}
})();
