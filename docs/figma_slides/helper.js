// === 설정 (호출마다 바꿈) ===
// const SEC_ID="...", START=0, TOTAL=22, SPECS=[...];
const FOOT="The Third Roommate  ·  ID40018  ·  Step 2";
const hex=h=>({r:parseInt(h.slice(0,2),16)/255,g:parseInt(h.slice(2,4),16)/255,b:parseInt(h.slice(4,6),16)/255});
const C={bg:hex('FBF6EE'),card:hex('FFFFFF'),ink:hex('2B2420'),sub:hex('948A80'),acc:hex('EF6A2A'),soft:hex('FCE7D8'),line:hex('EFE6DA'),dark:hex('2B2420'),cream:hex('FBF1E4')};
const F={B:{family:"Noto Sans KR",style:"Bold"},M:{family:"Noto Sans KR",style:"Medium"},R:{family:"Noto Sans KR",style:"Regular"}};
await Promise.all(Object.values(F).map(f=>figma.loadFontAsync(f)));
const page=await figma.getNodeByIdAsync("85:2"); await figma.setCurrentPageAsync(page);
const sec=await figma.getNodeByIdAsync(SEC_ID);
const solid=c=>[{type:'SOLID',color:c}];
function vbox(par,W,o={}){const f=figma.createFrame();f.name=o.name||'col';f.layoutMode='VERTICAL';f.resize(W,10);f.counterAxisSizingMode='FIXED';f.primaryAxisSizingMode='AUTO';f.fills=o.fill?solid(o.fill):[];f.itemSpacing=o.gap||0;const p=o.pad||[0,0];f.paddingTop=f.paddingBottom=p[0];f.paddingLeft=f.paddingRight=p[1];if(o.r)f.cornerRadius=o.r;f.clipsContent=false;if(par)par.appendChild(f);return f}
function hbox(par,W,o={}){const f=figma.createFrame();f.name=o.name||'row';f.layoutMode='HORIZONTAL';f.resize(W,10);f.primaryAxisSizingMode='FIXED';f.counterAxisSizingMode='AUTO';f.fills=o.fill?solid(o.fill):[];f.itemSpacing=o.gap||0;const p=o.pad||[0,0];f.paddingTop=f.paddingBottom=p[0];f.paddingLeft=f.paddingRight=p[1];if(o.r)f.cornerRadius=o.r;if(o.align)f.counterAxisAlignItems=o.align;f.clipsContent=false;if(par)par.appendChild(f);return f}
function txt(par,s,size,font,color,W,o={}){const t=figma.createText();t.fontName=font;t.fontSize=size;t.characters=String(s);t.fills=solid(color);t.lineHeight={unit:'PERCENT',value:o.lh||150};if(o.ls)t.letterSpacing={unit:'PERCENT',value:o.ls};par.appendChild(t);if(W){t.resize(W,t.height);t.textAutoResize='HEIGHT'}if(o.align)t.textAlignHorizontal=o.align;return t}
function equalize(nodes){const m=Math.max(...nodes.map(n=>n.height));for(const n of nodes){n.primaryAxisSizingMode='FIXED';n.resize(n.width,m)}return m}
function widths(W,w,gap){const s=w.reduce((a,b)=>a+b,0);const av=W-gap*(w.length-1);return w.map(x=>Math.floor(av*x/s))}
const GROW=[];
function block(par,W,b){
  if(Array.isArray(b)){const v=vbox(par,W,{gap:16});for(const x of b)block(v,W,x);return v}
  if(b.k==='cards'||b.k==='flow'||b.k==='big'){
    const n=b.c.length,flow=b.k==='flow',aw=flow?34:0,gap=flow?0:20;
    const row=hbox(par,W,{gap,align:flow?'CENTER':'MIN',name:b.k});const cw=Math.floor((W-(flow?aw:gap)*(n-1))/n);const pad=n>=5?20:28;const cs=[];
    b.c.forEach((c,i)=>{
      if(flow&&i)txt(row,'→',20,F.B,C.acc,aw,{align:'CENTER'});
      const cd=vbox(row,cw,{fill:b.soft?C.soft:C.card,r:24,pad:[pad,pad],gap:10,name:'card'});const tw=cw-pad*2;
      if(b.k==='big'){txt(cd,c[0],54,F.B,C.acc,tw,{lh:120});txt(cd,c[1],16,F.R,C.ink,tw,{lh:160})}
      else{if(c[0])txt(cd,c[0],13,F.B,C.acc,tw,{ls:4});if(c[1])txt(cd,c[1],n>=5?18:21,F.B,C.ink,tw,{lh:135});if(c[2])txt(cd,c[2],n>=5?14:15.5,F.R,C.ink,tw,{lh:165});if(c[3])txt(cd,c[3],13.5,F.M,C.sub,tw,{lh:155})}
      cs.push(cd)});
    equalize(cs);if(b.g)GROW.push(cs);return row}
  if(b.k==='table'){
    const wrap=vbox(par,W,{fill:C.card,r:24,pad:[10,28],name:'table'});const iw=W-56,gap=24,ws=widths(iw,b.w,gap);
    const hr=hbox(wrap,iw,{gap,pad:[12,0]});b.h.forEach((h,i)=>txt(hr,h,13,F.B,C.sub,ws[i],{ls:3}));
    hr.strokes=solid(C.line);hr.strokeTopWeight=0;hr.strokeLeftWeight=0;hr.strokeRightWeight=0;hr.strokeBottomWeight=1.5;
    b.r.forEach((r,ri)=>{const rr=hbox(wrap,iw,{gap,pad:[b.tight?10:13,0]});r.forEach((c,i)=>txt(rr,c,b.fs||15,i===0?F.B:F.R,i===0&&b.accent?C.acc:C.ink,ws[i],{lh:155}));
      if(ri<b.r.length-1){rr.strokes=solid(C.line);rr.strokeTopWeight=0;rr.strokeLeftWeight=0;rr.strokeRightWeight=0;rr.strokeBottomWeight=1}});
    return wrap}
  if(b.k==='code'){const cd=vbox(par,W,{fill:C.dark,r:20,pad:[22,26],gap:8,name:'code'});if(b.h)txt(cd,b.h,13,F.B,C.acc,W-52,{ls:4});txt(cd,b.t,b.fs||13.5,F.R,C.cream,W-52,{lh:165});return cd}
  if(b.k==='shots'){const n=b.c.length,gap=24,cw=Math.floor((W-gap*(n-1))/n);const row=hbox(par,W,{gap,name:'shots'});
    b.c.forEach(c=>{const v=vbox(row,cw,{gap:10});const ph=figma.createFrame();ph.name='IMAGE · '+c[0];ph.layoutMode='VERTICAL';ph.resize(cw,b.h||380);ph.primaryAxisSizingMode='FIXED';ph.counterAxisSizingMode='FIXED';ph.primaryAxisAlignItems='CENTER';ph.counterAxisAlignItems='CENTER';ph.fills=solid(C.soft);ph.cornerRadius=24;ph.strokes=solid(C.acc);ph.strokeWeight=1.5;ph.dashPattern=[6,6];v.appendChild(ph);txt(ph,c[0],13,F.M,C.acc,cw-40,{align:'CENTER'});
      if(c[1])txt(v,c[1],16,F.B,C.ink,cw,{lh:140});if(c[2])txt(v,c[2],14,F.R,C.ink,cw,{lh:160})});return row}
  if(b.k==='text'){return txt(par,b.t,b.fs||15,b.bold?F.B:F.R,b.sub?C.sub:C.ink,W,{lh:b.lh||170})}
  if(b.k==='cols'){const gap=24,ws=widths(W,b.w,gap);const row=hbox(par,W,{gap,align:'MIN',name:'cols'});b.c.forEach((x,i)=>{const v=vbox(row,ws[i],{gap:16});for(const y of (Array.isArray(x)?x:[x]))block(v,ws[i],y)});return row}
  throw new Error('unknown block '+b.k)}
const out=[];
for(let si=0;si<SPECS.length;si++){
  const s=SPECS[si],idx=START+si,W=1424;GROW.length=0;
  const f=figma.createFrame();f.name=String(idx+1).padStart(2,'0')+' · '+(s.name||s.t).slice(0,40);f.resize(1600,900);f.layoutMode='VERTICAL';f.primaryAxisSizingMode='FIXED';f.counterAxisSizingMode='FIXED';f.paddingLeft=f.paddingRight=88;f.paddingTop=60;f.paddingBottom=40;f.fills=solid(C.bg);f.clipsContent=true;
  sec.appendChild(f);f.x=48;f.y=64+idx*964;
  const el=figma.createEllipse();el.resize(1000,1000);el.fills=[{type:'GRADIENT_RADIAL',gradientTransform:[[1,0,0],[0,1,0]],gradientStops:[{position:0,color:{r:0.99,g:0.82,b:0.68,a:s.k==='cover'?0.75:0.45}},{position:1,color:{r:0.99,g:0.82,b:0.68,a:0}}]}];f.appendChild(el);el.layoutPositioning='ABSOLUTE';el.x=s.k==='cover'?820:980;el.y=s.k==='cover'?-200:-520;el.name='bg-glow';
  if(s.k==='cover'){
    txt(f,s.s,16,F.M,C.sub,W,{ls:6});const sp0=vbox(f,W);sp0.resize(W,150);sp0.primaryAxisSizingMode='FIXED';
    txt(f,s.t,92,F.B,C.acc,W,{lh:120});txt(f,s.t2,34,F.M,C.ink,W,{lh:150});const sp1=vbox(f,W);sp1.resize(W,28);sp1.primaryAxisSizingMode='FIXED';
    txt(f,s.l,21,F.R,C.ink,900,{lh:165});const sp=vbox(f,W);sp.layoutGrow=1;
    const row=hbox(f,W,{gap:40,align:'MAX'});txt(row,s.team,15,F.R,C.ink,560,{lh:170});txt(row,s.url,16,F.B,C.acc,520,{lh:170});txt(row,s.date,15,F.M,C.sub,264,{align:'RIGHT'});
    out.push({i:idx+1,id:f.id});continue}
  const head=vbox(f,W,{gap:8,name:'header'});txt(head,s.s,15,F.M,C.sub,W,{ls:5});txt(head,s.t,s.ts||36,F.B,C.acc,W,{lh:132});if(s.l)txt(head,s.l,18,F.R,C.ink,1180,{lh:160});
  const gapA=vbox(f,W);gapA.resize(W,28);gapA.primaryAxisSizingMode='FIXED';
  const body=vbox(f,W,{gap:18,name:'body'});for(const b of s.b)block(body,W,b);
  const sp=vbox(f,W,{name:'spacer'});sp.layoutGrow=1;
  if(s.n){const nb=vbox(f,W,{fill:C.soft,r:18,pad:[16,24],name:'note'});txt(nb,s.n,15.5,F.M,C.ink,W-48,{lh:160})}
  const g2=vbox(f,W);g2.resize(W,18);g2.primaryAxisSizingMode='FIXED';
  const ft=hbox(f,W,{name:'footer'});ft.primaryAxisAlignItems='SPACE_BETWEEN';txt(ft,FOOT,12,F.M,C.sub,600);txt(ft,String(idx+1).padStart(2,'0')+' / '+TOTAL,12,F.M,C.sub,120,{align:'RIGHT'});
  let used=100;for(const ch of f.children){if(ch!==el&&ch!==sp)used+=ch.height}
  const left=900-used;
  if(left>24&&GROW.length){const add=Math.min(left-8,200);for(const cs of GROW)for(const n of cs)n.resize(n.width,n.height+add)}
  out.push({i:idx+1,id:f.id,left:Math.round(left)});
}
return out;
