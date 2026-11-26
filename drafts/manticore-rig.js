/* Ten style drafts of the manticore, all drawn in canvas code (so any of them can run in the game).
   One anatomy (lion body, man's face in a mane, folded bat wings, scorpion tail), ten renderers. */
const TAU=Math.PI*2;
const rng=s=>()=>{s=(s*16807)%2147483647;return s/2147483647};
function mk(W,H){const c=document.createElement('canvas');c.width=W;c.height=H;return c}
function sm(g,P,closed=true){g.beginPath();const n=P.length;if(P.sharp){P.forEach((p,i)=>i?g.lineTo(...p):g.moveTo(...p));if(closed)g.closePath();return}if(!closed){g.moveTo(...P[0]);for(let i=1;i<n-1;i++){const m=[(P[i][0]+P[i+1][0])/2,(P[i][1]+P[i+1][1])/2];g.quadraticCurveTo(P[i][0],P[i][1],m[0],m[1])}g.lineTo(...P[n-1]);return}
 for(let i=0;i<=n;i++){const a=P[i%n],b=P[(i+1)%n],m=[(a[0]+b[0])/2,(a[1]+b[1])/2];i?g.quadraticCurveTo(a[0],a[1],m[0],m[1]):g.moveTo(m[0],m[1])}g.closePath()}
function hx(c){const n=parseInt(c.slice(1),16);return[n>>16,n>>8&255,n&255]}
function rgb(a){return'#'+a.map(v=>Math.max(0,Math.min(255,Math.round(v))).toString(16).padStart(2,'0')).join('')}
const mixc=(a,b,t)=>{const A=hx(a),B=hx(b);return rgb(A.map((v,i)=>v+(B[i]-v)*t))},lt=(c,t)=>mixc(c,'#ffffff',t),dk=(c,t)=>mixc(c,'#000000',t);
const desat=(c,t)=>{const A=hx(c),m=(A[0]+A[1]+A[2])/3;return rgb(A.map(v=>v+(m-v)*t))};

/* ---------- the rig: a posable manticore skeleton. Each style sets its own proportions, pose and shapes. ----------
   Units: ground y = 0, facing left (the front is -x). build() returns px shapes in draw order. */
const RIG0={len:.78,shoulderH:.66,hipH:.64,chest:.34,belly:.25,rump:.3,hump:.02,sag:.02,legW:1,paw:.065,head:1,headX:0,headY:0,chin:.3,
 mane:{type:'flow',size:1},wing:{spread:.15,size:1,tatter:0},tail:{thick:1,h:1,n:13},
 fore:[],foreFar:[[0,0],[.03,0],[.06,0],[.07,0]],hind:[],hindFar:[[0,0],[-.03,0],[-.07,0],[-.06,0]],lean:0,ribs:0,straight:0,poly:0};
function rigOf(o){const r=JSON.parse(JSON.stringify(RIG0));for(const k in o)r[k]=(typeof o[k]==='object'&&!Array.isArray(o[k]))?Object.assign(r[k]||{},o[k]):o[k];return r}
function cr(J,n){const out=[];for(let i=0;i<J.length-1;i++){const p0=J[Math.max(0,i-1)],p1=J[i],p2=J[i+1],p3=J[Math.min(J.length-1,i+2)];for(let k=0;k<n;k++){const t=k/n,t2=t*t,t3=t2*t;out.push([0,1].map(d=>.5*((2*p1[d])+(-p0[d]+p2[d])*t+(2*p0[d]-5*p1[d]+4*p2[d]-p3[d])*t2+(-p0[d]+3*p1[d]-3*p2[d]+p3[d])*t3)).concat([i+t]))}}const L=J[J.length-1];out.push([L[0],L[1],J.length-1]);return out}
function limb(J,Wd,bulge){const S=cr(J,8),Lf=[],Rt=[];S.forEach((p,k)=>{const a=S[Math.max(0,k-1)],b=S[Math.min(S.length-1,k+1)],dx=b[0]-a[0],dy=b[1]-a[1],l=Math.hypot(dx,dy)||1,i=Math.min(Wd.length-2,Math.floor(p[2])),f=p[2]-i;
  let w=(Wd[i]+(Wd[i+1]-Wd[i])*f)/2;const mus=bulge&&i===bulge[0]?Math.sin(f*Math.PI)*bulge[1]:0;const nx=-dy/l,ny=dx/l;Lf.push([p[0]+nx*(w+(bulge&&bulge[2]>0?mus:0)),p[1]+ny*(w+(bulge&&bulge[2]>0?mus:0))]);Rt.push([p[0]-nx*(w+(bulge&&bulge[2]<0?mus:0)),p[1]-ny*(w+(bulge&&bulge[2]<0?mus:0))])});return Lf.concat(Rt.reverse())}
const add2=(J,O)=>J.map((p,i)=>O&&O[i]?[p[0]+O[i][0],p[1]+O[i][1]]:p.slice());
function ellPts(c,rx,ry,n,f){const o=[];for(let i=0;i<n;i++){const a=i/n*TAU;o.push([c[0]+Math.cos(a)*rx*(f?f(a,i):1),c[1]+Math.sin(a)*ry*(f?f(a,i):1)])}return o}
function rigShapes(r){const S=[],add=(name,pts,col,o)=>S.push(Object.assign({name,pts,col},o||{})),L=r.len,Ws=r.shoulderH,Hh=r.hipH,x0=-L/2,x1=L/2,lw=r.legW,pw=r.paw;
 /* legs */
 const foreJ=r.straight?[[x0,-Ws+r.chest*.35],[x0+.01,-Ws+r.chest+.03],[x0+.01,-pw*1.6-.05],[x0,-pw*.5]]:[[x0,-Ws+r.chest*.35],[x0+.05,-Ws+r.chest+.03],[x0,-pw*1.6-.06],[x0-.02,-pw*.5]];
 const hindJ=r.straight?[[x1-.02,-Hh+r.rump*.35],[x1-.05,-Hh+r.rump+.05],[x1-.03,-.14],[x1-.03,-pw*.5]]:[[x1-.02,-Hh+r.rump*.35],[x1-.14,-Hh+r.rump+.06],[x1+.06,-Math.max(.12,Hh*.28)],[x1,-pw*.5]];
 const fw=[.19,.12,.07,.07].map(v=>v*lw),hw=[.27,.14,.075,.075].map(v=>v*lw);
 const paw=(p,big)=>{const c=[p[0]-pw*.35,-pw*.55*big];return ellPts(c,pw*1.25*big,pw*.6*big,16,(a)=>a>Math.PI?1:1.04)};
 const toes=[];const legShape=(name,J,Wd,col,o,bul)=>{add(name,limb(J,Wd,bul),col,o);const P=J[J.length-1];add(name+'Paw',paw(P,1),col,Object.assign({paw:1},o));if(!o.far)for(let k=0;k<3;k++){const tx=P[0]-pw*1.1+k*pw*.55;toes.push([[tx,-.003],[tx+.004,-pw*.45]])}};
 legShape('farHind',add2(hindJ,r.hindFar),hw.map(v=>v*.92),'#a8783e',{far:1,fur:1},[0,.03*lw,-1]);legShape('farFore',add2(foreJ,r.foreFar),fw.map(v=>v*.92),'#a8783e',{far:1,fur:1},[0,.02*lw,1]);
 /* wing */
 const ws=[x0+.13,-Ws-.02],W=r.wing,e=W.spread,lerp=(a,b)=>a+(b-a)*e,a1=lerp(-.75,-1.85),L1=lerp(.26,.34)*W.size,wr=[ws[0]+Math.cos(a1)*L1,ws[1]+Math.sin(a1)*L1];
 const fa=[[-.25,-1.1],[.2,-.55],[.65,-.05]].map(([f,sp])=>f+(sp-f)*e),fl=[[.26,.48],[.3,.56],[.24,.46]].map(([f,sp])=>(f+(sp-f)*e)*W.size),tips=fa.map((a,i)=>[wr[0]+Math.cos(a)*fl[i],wr[1]+Math.sin(a)*fl[i]]);
 const att=[x1-lerp(.05,.15),-Hh+lerp(.03,0)],pull=(a,b,k)=>{const m=[(a[0]+b[0])/2,(a[1]+b[1])/2];return[m[0]+(wr[0]-m[0])*k,m[1]+(wr[1]-m[1])*k]};
 const notch=(a,b)=>{const pts=[pull(a,b,lerp(.28,.4))];if(W.tatter){const R=rng(Math.round(a[0]*1e4)+7);for(let q=1;q<4;q++){const t=q/4,m=[a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t];pts.push([m[0]+(wr[0]-m[0])*(.18+R()*.2*W.tatter),m[1]+(wr[1]-m[1])*(.18+R()*.2*W.tatter)])}}return pts};
 const memb=[ws,[(ws[0]+wr[0])/2,(ws[1]+wr[1])/2-.02],wr,tips[0],...notch(tips[0],tips[1]),tips[1],...notch(tips[1],tips[2]),tips[2],...notch(tips[2],att),att,[(att[0]+ws[0])/2,(att[1]+ws[1])/2+.02]];
 const bones=[[ws,wr],...tips.map(t=>[wr,t])];
 if(e>.4)add('wingFar',memb.map(([x,y])=>[x+.05,y-.04]),'#4c3a42',{far:1,wing:1,sharp:!!W.tatter});
 /* tail */
 const tb=[x1+.09,-Hh+.04],T0=[[0,0],[.12,-.1],[.2,-.28],[.17,-.46],[.06,-.56],[-.07,-.54],[-.14,-.47]].map(([x,y])=>[tb[0]+x*r.tail.h,tb[1]+y*r.tail.h]);
 /* torso */
 const tor=[[x0-.13,-Ws+r.chest*.45],[x0-.1,-Ws+.07],[x0+.02,-Ws-.01-r.hump],[0,-(Ws+Hh)/2+r.sag],[x1-.02,-Hh-.01],[x1+.1,-Hh+.06],[x1+.13,-Hh+r.rump*.5],[x1+.05,-Hh+r.rump],[x1-.14,-Hh+r.rump*.92],[0,-(Ws+Hh)/2+r.belly+.02],[x0+.12,-Ws+r.chest],[x0-.02,-Ws+r.chest+.01],[x0-.12,-Ws+r.chest*.8]];
 add('torso',tor,'#c08a48',{fur:1,torso:1});
 legShape('hind',add2(hindJ,r.hind),hw,'#c08a48',{fur:1},[0,.05*lw,-1]);legShape('fore',add2(foreJ,r.fore),fw,'#c08a48',{fur:1},[0,.03*lw,1]);
 add('wing',memb,'#5a4450',{wing:1,sharp:!!W.tatter});
 /* head: mane and face */
 const hk=r.head,F=[x0-.17+r.headX,-Ws-.05+r.headY],mc=[F[0]+.03*hk,F[1]+.02*hk],R=.22*r.mane.size*hk,M=r.mane.type,Rn=rng(5);let mane,sharp=false;
 if(M==='flow')mane=ellPts(mc,R,R,80,(a)=>{const b=Math.max(0,Math.cos(a)),d=Math.max(0,Math.sin(a));return(1+.07*Math.sin(a*11)+.03*Math.sin(a*23))*(1+b*.6*(1-Math.abs(Math.sin(a))*.3))*(1+d*.35)});
 else if(M==='spiky'){mane=ellPts(mc,R,R*1.05,30,(a,i)=>(i%2?1.35:.95)*(1+Math.max(0,Math.cos(a))*.5));sharp=true}
 else if(M==='clump')mane=ellPts(mc,R,R,60,(a)=>(1+.13*Math.abs(Math.sin(a*4.5)))*(1+Math.max(0,Math.cos(a))*.25));
 else if(M==='shag')mane=ellPts(mc,R,R*1.05,40,(a,i)=>(i%2?1.22:.98)*(1+Math.max(0,Math.cos(a))*.45)*(1+Math.max(0,Math.sin(a))*.2));
 else if(M==='round')mane=ellPts(mc,R,R,48,(a)=>1+.04*Math.sin(a*8));
 else if(M==='tatter'){mane=ellPts(mc,R,R*1.1,44,(a,i)=>(.85+Rn()*.5)*(1+Math.max(0,Math.cos(a))*.55)*(1+Math.max(0,Math.sin(a))*.4));sharp=true}
 else if(M==='geo'){mane=ellPts(mc,R,R*1.1,11,(a)=>(.95+Rn()*.15)*(1+Math.max(0,Math.cos(a))*.4));sharp=true}
 add('mane',mane,'#7e4a22',{mane:1,fur:1,sharp});
 const face=ellPts([0,0],.1,.13,40,()=>1).map(([x,y])=>{const t=y/.13,k=t>0?1-r.chin*t*t:1-.08*t*t;return[-.49+x*k,-.735+y]});
 return{S,T0,toes,bones,F,hk,mc,R,ribs:r.ribs?[[[x0+.12,-Ws+r.chest*.55],[x0+.2,-Ws+r.chest*.95]],[[x0+.2,-Ws+r.chest*.5],[x0+.28,-Ws+r.chest*.9]],[[x0+.28,-Ws+r.chest*.48],[x0+.35,-Ws+r.chest*.85]],[[x0+.36,-Ws+r.chest*.47],[x0+.42,-Ws+r.chest*.8]]]:[],face}}
function build(W,H,s,ox,oy,rig){const r=rig||rigOf({}),Q=rigShapes(r),pv=[ (r.len/2), 0],cl=Math.cos(r.lean),sl=Math.sin(r.lean);
 const U=([x,y])=>{const dx=x-pv[0],dy=y-pv[1];return[pv[0]+dx*cl-dy*sl,pv[1]+dx*sl+dy*cl]},T=p=>{const o=p.map(q=>{const u=U(q);return[ox+u[0]*s,oy+u[1]*s]});if(p.sharp||r.poly)o.sharp=true;return o};
 const FT=p=>T(p.map(([x,y])=>[Q.F[0]+(x+.49)*Q.hk,Q.F[1]+(y+.735)*Q.hk])),FS=s*Q.hk;
 const tp=T(Q.T0),seg=[],n=r.tail.n,samp=cr(tp,6);
 for(let i=0;i<n;i++){const u=i/(n-1),k=Math.min(samp.length-2,Math.round(u*(samp.length-2))),a=samp[k],b=samp[k+1],ang=Math.atan2(b[1]-a[1],b[0]-a[0]),rr=s*(.058-.03*u)*r.tail.thick,P=[];
  for(let q=0;q<16;q++){const t=q/16*TAU,ex=Math.cos(t)*rr*1.1,ey=Math.sin(t)*rr*.85;P.push([a[0]+ex*Math.cos(ang)-ey*Math.sin(ang),a[1]+ex*Math.sin(ang)+ey*Math.cos(ang)])}if(r.poly)P.sharp=true;seg.push({name:'tail',P,col:i%2?'#7a3e22':'#8a4a2a',seg:1})}
 const e=samp[samp.length-1],d=samp[samp.length-3],ang=Math.atan2(e[1]-d[1],e[0]-d[0]),ss=s*r.tail.thick,rot=(x,y)=>[e[0]+x*Math.cos(ang)-y*Math.sin(ang),e[1]+x*Math.sin(ang)+y*Math.cos(ang)];
 const sting={name:'sting',P:[rot(-.01*ss,-.025*ss),rot(.06*ss,-.02*ss),rot(.11*ss,.03*ss),rot(.12*ss,.08*ss),rot(.08*ss,.025*ss),rot(-.01*ss,.025*ss)],col:'#2e1e18',sting:1};
 const list=[];Q.S.forEach(sh=>{let P=T(sh.pts);if(sh.sharp)P.sharp=true;if(sh.name==='torso')list.push(...seg.slice().reverse(),sting);if(sh.name==='face')return;list.push({...sh,P})});
 const fP=FT(Q.face);if(r.poly)fP.sharp=true;list.push({name:'face',P:r.poly?fP.filter((_,i)=>i%3===0).concat([]).map(p=>p):fP,col:'#d9a37c',face:1});if(r.poly)list[list.length-1].P.sharp=true;
 if(r.poly)list.forEach(sh=>{if(sh.P.length>14){const k=Math.ceil(sh.P.length/12),P=sh.P.filter((_,i)=>i%k===0);P.sharp=true;sh.P=P}});
 return{list,T,FT,FS,maneC:T([Q.mc])[0],maneR:Q.R*s,bones:Q.bones.map(b=>T(b)),toes:Q.toes.map(t=>T(t)),ribs:Q.ribs.map(t=>T(t)),rig:r}}
function fit(rig,W,H){const B=build(W,H,1,0,0,rig);let x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;B.list.forEach(sh=>sh.P.forEach(([x,y])=>{x0=Math.min(x0,x);y0=Math.min(y0,y);x1=Math.max(x1,x);y1=Math.max(y1,y)}));
 const s=Math.min((W*.86)/(x1-x0),(H*.84)/(Math.max(-y0,y1-y0)));return{s,ox:W/2-(x0+x1)/2*s,oy:H*.94}}

/* ---------- shading helpers (px) ---------- */
function shapeCanvas(W,H,P,fill){const c=mk(W,H),g=c.getContext('2d');g.fillStyle=fill;sm(g,P);g.fill();return c}
function maskShift(W,H,P,dx,dy,blur){const c=mk(W,H),g=c.getContext('2d');if(blur)g.filter=`blur(${blur}px)`;g.fillStyle='#000';sm(g,P);g.fill();g.globalCompositeOperation='destination-out';g.translate(dx,dy);sm(g,P);g.fill();
 const o=mk(W,H),q=o.getContext('2d');q.drawImage(c,0,0);q.globalCompositeOperation='destination-in';sm(q,P);q.fill();return o}
function tint(W,H,mask,col,alpha,ctx,op){const c=mk(W,H),g=c.getContext('2d');g.fillStyle=col;g.fillRect(0,0,W,H);g.globalCompositeOperation='destination-in';g.drawImage(mask,0,0);ctx.save();ctx.globalAlpha=alpha;if(op)ctx.globalCompositeOperation=op;ctx.drawImage(c,0,0);ctx.restore()}
function bbox(P){let a=1e9,b=1e9,c=-1e9,d=-1e9;P.forEach(([x,y])=>{a=Math.min(a,x);b=Math.min(b,y);c=Math.max(c,x);d=Math.max(d,y)});return{x0:a,y0:b,x1:c,y1:d,w:c-a,h:d-b}}
/* smooth form shading: highlight upper left, core shadow lower right, bounce light at the very bottom edge */
function smooth(ctx,W,H,P,col,s,o={}){const B=bbox(P);ctx.save();sm(ctx,P);ctx.clip();const g=ctx.createLinearGradient(B.x0,B.y0,B.x0+B.w*.35,B.y1);g.addColorStop(0,lt(col,o.hi??.28));g.addColorStop(.55,col);g.addColorStop(1,dk(col,o.lo??.45));ctx.fillStyle=g;ctx.fillRect(B.x0-2,B.y0-2,B.w+4,B.h+4);ctx.restore();
 tint(W,H,maskShift(W,H,P,-s*.07,-s*.09,s*(o.soft??.05)),o.shadow||dk(col,.55),o.shadowA??.6,ctx);
 if(o.bounce)tint(W,H,maskShift(W,H,P,0,s*.03,s*.01),o.bounce,.25,ctx,'lighter')}
function rimLight(ctx,W,H,P,col,s,a,dir=[1,-.4],blur=.01){tint(W,H,maskShift(W,H,P,-dir[0]*s*.022,-dir[1]*s*.022,s*blur),col,a,ctx,'lighter')}
function strokes(ctx,P,n,len,col,w,flow,seed,o={}){const R=rng(seed),B=bbox(P),p=new Path2D();sm({beginPath(){},moveTo:(...a)=>p.moveTo(...a),lineTo:(...a)=>p.lineTo(...a),quadraticCurveTo:(...a)=>p.quadraticCurveTo(...a),closePath:()=>p.closePath()},P);
 ctx.save();ctx.lineCap='round';for(let i=0;i<n;i++){const x=B.x0+R()*B.w,y=B.y0+R()*B.h;if(!ctx.isPointInPath(p,x,y))continue;const a=flow(x,y,B)+(R()-.5)*.5,L=len*(.6+R()*.8);ctx.strokeStyle=typeof col==='function'?col(x,y,B,R):col;ctx.globalAlpha=o.alpha??(.35+R()*.4);ctx.lineWidth=w*(.6+R()*.8);ctx.beginPath();ctx.moveTo(x,y);ctx.quadraticCurveTo(x+Math.cos(a)*L*.5+(R()-.5)*L*.3,y+Math.sin(a)*L*.5,x+Math.cos(a)*L,y+Math.sin(a)*L);ctx.stroke()}ctx.restore()}
function outline(ctx,P,w,col,closed=true){ctx.save();ctx.strokeStyle=col;ctx.lineWidth=w;ctx.lineJoin='round';ctx.lineCap='round';sm(ctx,P,closed);ctx.stroke();ctx.restore()}
/* ---------- the face (shared; each style passes its own look) ---------- */
function face(ctx,T,s,o){const L=(pts,w,c)=>{ctx.save();ctx.strokeStyle=c||o.ink;ctx.lineCap='round';ctx.lineJoin='round';ctx.lineWidth=w*s;sm(ctx,T(pts),false);ctx.stroke();ctx.restore()};const es=o.eye||1;
 for(const sx of[-1,1]){const ex=-.49+sx*.038,ey=-.758,ew=.024*es,eh=.011*es*(o.tall||1);
  ctx.save();ctx.beginPath();const E=T([[ex-ew,ey],[ex-ew*.3,ey-eh*1.1],[ex+ew*.5,ey-eh*1.05],[ex+ew,ey+eh*.1],[ex+ew*.3,ey+eh*.9],[ex-ew*.4,ey+eh*.8]]);sm(ctx,E);ctx.fillStyle=o.white;ctx.fill();ctx.clip();
  const ir=T([[ex-sx*.003,ey]])[0],r=.0105*s*es*(o.iris_r||1);if(o.glow){ctx.restore();ctx.save();const g=ctx.createRadialGradient(ir[0],ir[1],0,ir[0],ir[1],r*4);g.addColorStop(0,o.glow);g.addColorStop(1,o.glow.replace(/[\d.]+\)$/,'0)'));ctx.fillStyle=g;ctx.fillRect(ir[0]-r*4,ir[1]-r*4,r*8,r*8);ctx.restore();ctx.save();sm(ctx,E);ctx.clip()}
  const gi=ctx.createRadialGradient(ir[0],ir[1]-r*.3,0,ir[0],ir[1],r);gi.addColorStop(0,lt(o.iris,.35));gi.addColorStop(1,dk(o.iris,.35));ctx.fillStyle=gi;ctx.beginPath();ctx.arc(ir[0],ir[1],r,0,TAU);ctx.fill();
  if(o.pupil!==false){ctx.fillStyle=o.pupilCol||'#0e0806';ctx.beginPath();if(o.slit)ctx.ellipse(ir[0],ir[1],r*.22,r*.85,0,0,TAU);else ctx.arc(ir[0],ir[1],r*.45,0,TAU);ctx.fill()}
  if(o.shine!==false){ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(ir[0]-r*.35,ir[1]-r*.4,r*(o.bigShine?.38:.22),0,TAU);ctx.fill();if(o.bigShine){ctx.beginPath();ctx.arc(ir[0]+r*.35,ir[1]+r*.35,r*.14,0,TAU);ctx.fill()}}
  if(o.lidShade){ctx.fillStyle='rgba(60,30,20,.35)';ctx.fillRect(E[0][0]-5,E[1][1]-5,ew*s*3,eh*s*.9)}ctx.restore();
  L([[ex-ew*1.05,ey+.001],[ex-ew*.3,ey-eh*1.15],[ex+ew*.6,ey-eh*1.05],[ex+ew*1.05,ey+eh*.2]],o.lid||.0045);
  L([[ex-sx*.03,ey-.026-(o.angry?sx*-.008:0)],[ex,ey-.034],[ex+sx*.03,ey-.024+(o.angry?.008:0)]].sort((a,b)=>a[0]-b[0]),o.brow||.007,o.browCol)}
 if(o.noseShade){const N=T([[-.49,-.75],[-.5,-.712],[-.485,-.706]]);ctx.save();ctx.strokeStyle=o.noseShade;ctx.lineWidth=.012*s;ctx.globalAlpha=.4;ctx.lineCap='round';sm(ctx,N,false);ctx.stroke();ctx.restore()}
 L([[-.487,-.752],[-.492,-.718],[-.504,-.705],[-.49,-.699],[-.476,-.705]],o.nose||.004);
 const J=(o.open||0)*.034,M=T([[-.545,-.674],[-.49,-.684],[-.435,-.674],[-.442,-.66+J*.7],[-.49,-.652+J],[-.538,-.66+J*.7]]);ctx.fillStyle=o.mouth;sm(ctx,M);ctx.fill();if(J){ctx.save();sm(ctx,M);ctx.clip();ctx.fillStyle='#b04848';const tg=T([[-.49,-.652+J*.9]])[0];ctx.beginPath();ctx.ellipse(tg[0],tg[1],.03*s,.012*s,0,0,TAU);ctx.fill();ctx.fillStyle=o.teeth;for(let k=0;k<9;k++){const x=-.535+k*.0105,y=-.652+J*.95-.001;const P=T([[x,y],[x+.005,y-.009],[x+.01,y]]);ctx.beginPath();ctx.moveTo(...P[0]);ctx.lineTo(...P[1]);ctx.lineTo(...P[2]);ctx.fill()}ctx.restore()}
 ctx.save();sm(ctx,M);ctx.clip();ctx.fillStyle=o.teeth;for(let r=0;r<3;r++)for(let k=0;k<11;k++){const x=-.54+k*.0095+(r%2)*.004,y=-.68+r*.007;const P=T([[x,y],[x+.0045,y+.0075],[x+.009,y]]);ctx.beginPath();ctx.moveTo(...P[0]);ctx.lineTo(...P[1]);ctx.lineTo(...P[2]);ctx.fill()}ctx.restore();
 ctx.save();ctx.strokeStyle=o.ink;ctx.lineWidth=(o.lip||.004)*s;sm(ctx,M);ctx.stroke();ctx.restore();
 if(o.lines!==false){L([[-.552,-.69],[-.545,-.674]],.003);L([[-.428,-.69],[-.435,-.674]],.003);L([[-.512,-.634],[-.49,-.627],[-.468,-.634]],.003)}}
function extras(ctx,BR,col,w,o={}){ctx.save();ctx.strokeStyle=col;ctx.lineCap='round';ctx.lineWidth=w;BR.toes.forEach(t=>{ctx.beginPath();ctx.moveTo(...t[0]);ctx.lineTo(...t[1]);ctx.stroke()});
 BR.ribs.forEach(t=>{ctx.lineWidth=w*1.6;ctx.beginPath();ctx.moveTo(...t[0]);ctx.quadraticCurveTo(t[0][0]+(t[1][0]-t[0][0])*.2+6,(t[0][1]+t[1][1])/2,t[1][0],t[1][1]);ctx.stroke();if(o.ribLight){ctx.save();ctx.strokeStyle=o.ribLight;ctx.lineWidth=w;ctx.beginPath();ctx.moveTo(t[0][0]-3,t[0][1]);ctx.quadraticCurveTo(t[0][0]+(t[1][0]-t[0][0])*.2+3,(t[0][1]+t[1][1])/2,t[1][0]-3,t[1][1]);ctx.stroke();ctx.restore()}});ctx.restore()}
/* ---------- the ten styles ---------- */
const STY=[];const def=(id,title,sub,fn)=>STY.push({id,title,sub,fn});
const groundShadow=(ctx,x,y,rx,ry,a,blur)=>{ctx.save();ctx.filter=`blur(${blur}px)`;ctx.fillStyle=`rgba(0,0,0,${a})`;ctx.beginPath();ctx.ellipse(x,y,rx,ry,0,0,TAU);ctx.fill();ctx.restore()};
const furFlow=(x,y,B)=>Math.PI*.55+((x-B.x0)/B.w-.5)*.3;
const maneFlow=c=>(x,y)=>Math.atan2(y-c[1],x-c[0]);

/* 1. PHOTOREALISTIC: smooth form shading, thousands of fur strokes, glossy chitin, translucent membrane, depth-of-field background */
def('photoreal','1 · Photorealistic','fur strand by strand, real light and shadow, blurred background (as close as code-drawing gets)',(ctx,W,H,s,ox,oy,rig)=>{
 const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#2e2a24');bg.addColorStop(.62,'#5a4a36');bg.addColorStop(1,'#3a3024');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);
 ctx.save();ctx.filter='blur(14px)';const R=rng(4);for(let i=0;i<26;i++){ctx.fillStyle=`rgba(${200+R()*55|0},${150+R()*60|0},90,${.08+R()*.12})`;ctx.beginPath();ctx.arc(R()*W,R()*H*.6,10+R()*40,0,TAU);ctx.fill()}ctx.fillStyle='rgba(90,70,40,.5)';ctx.fillRect(0,oy-10,W,H);ctx.restore();
 groundShadow(ctx,ox+s*.08,oy,s*.62,s*.05,.65,8);groundShadow(ctx,ox+s*.08,oy,s*.5,s*.02,.8,2);
 const BR=build(W,H,s,ox,oy,rig),{list,T,FT,FS}=BR;const mc=BR.maneC;
 list.forEach((sh,i)=>{const P=sh.P,c=sh.far?dk(sh.col,.28):sh.col;
  if(sh.wing){smooth(ctx,W,H,P,c,s,{hi:.25,lo:.5,soft:.04});ctx.save();sm(ctx,P);ctx.clip();ctx.strokeStyle='rgba(140,90,100,.35)';ctx.lineWidth=1;const R=rng(i+9);for(let k=0;k<40;k++){const a=bbox(P);ctx.beginPath();let x=a.x0+R()*a.w,y=a.y0+R()*a.h;ctx.moveTo(x,y);for(let q=0;q<5;q++){x+=(R()-.3)*10;y+=(R()-.5)*8;ctx.lineTo(x,y)}ctx.stroke()}ctx.restore();rimLight(ctx,W,H,P,'#d8a8a0',s,.35);if(!sh.far)BR.bones.forEach(Q=>{ctx.save();ctx.strokeStyle=dk(c,.35);ctx.lineWidth=s*.012;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(...Q[0]);ctx.lineTo(...Q[1]);ctx.stroke();ctx.strokeStyle='rgba(255,220,210,.25)';ctx.lineWidth=s*.004;ctx.beginPath();ctx.moveTo(Q[0][0]-1,Q[0][1]-1);ctx.lineTo(Q[1][0]-1,Q[1][1]-1);ctx.stroke();ctx.restore()});return}
  if(sh.seg||sh.sting){smooth(ctx,W,H,P,c,s,{hi:.15,lo:.6,soft:.01,shadowA:.4});const B=bbox(P);ctx.save();ctx.fillStyle='rgba(255,240,220,.55)';ctx.beginPath();ctx.ellipse(B.x0+B.w*.35,B.y0+B.h*.3,B.w*.14,B.h*.08,-.5,0,TAU);ctx.fill();ctx.restore();return}
  if(sh.face){smooth(ctx,W,H,P,c,s,{hi:.18,lo:.35,soft:.06,shadow:'#8a4a3a',shadowA:.45});ctx.save();sm(ctx,P);ctx.clip();const B=bbox(P);for(const[x,y,r,col,a]of[[.3,.62,.25,'#d06a5a',.18],[.7,.62,.25,'#d06a5a',.18],[.5,.85,.3,'#6a4a3a',.15]]){const g=ctx.createRadialGradient(B.x0+B.w*x,B.y0+B.h*y,0,B.x0+B.w*x,B.y0+B.h*y,B.w*r);g.addColorStop(0,col);g.addColorStop(1,col+'00');ctx.globalAlpha=a*3;ctx.fillStyle=g;ctx.fillRect(B.x0,B.y0,B.w,B.h)}ctx.restore();
   strokes(ctx,P.filter((_,k)=>k>2&&k<18).concat([[B.x1-B.w*.15,B.y1-B.h*.35],[B.x0+B.w*.15,B.y1-B.h*.35]]),300,s*.012,'#5a3a2a',.6,()=>Math.PI/2,7,{alpha:.25});
   face(ctx,FT,FS,{ink:'#3a2016',white:'#e8dccb',iris:'#6a4a22',mouth:'#3a1410',teeth:'#e6dcc4',noseShade:'#8a4a3a',lidShade:1});return}
  smooth(ctx,W,H,P,c,s,{hi:.3,lo:.55,soft:.07,shadowA:.55,bounce:'#e0b070'});
  const flow=sh.mane?maneFlow(mc):furFlow,n=sh.mane?2600:Math.min(2600,bbox(P).w*bbox(P).h/10),L=sh.mane?s*.06:s*.018;
  const colF=(x,y,B,R)=>{const t=((x-B.x0)/B.w*.4+(y-B.y0)/B.h*.6);return R()<.5?lt(c,.35-t*.3):dk(c,.1+t*.5)};
  strokes(ctx,P,n,L,colF,sh.mane?1.1:.8,flow,i*31+5);if(!sh.far)rimLight(ctx,W,H,P,'#ffd9a0',s,.25)});extras(ctx,BR,'rgba(40,20,10,.55)',1.2);
});
/* 2. ANIME: clean thin line, two-tone cel shading with a hard edge, big glossy eyes, spiky mane clumps, bright sky */
def('anime','2 · Anime','clean line, hard two-tone cel shading, big glossy eyes, bright colour',(ctx,W,H,s,ox,oy,rig)=>{
 const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#7ec4f2');bg.addColorStop(.7,'#d4eefc');bg.addColorStop(1,'#9fd08a');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);ctx.fillStyle='#8cc472';ctx.fillRect(0,oy-6,W,H);ctx.fillStyle='rgba(255,255,255,.85)';for(const[x,y,r]of[[.15,.18,30],[.22,.16,22],[.8,.12,26],[.86,.14,18]]){ctx.beginPath();ctx.arc(W*x,H*y,r,0,TAU);ctx.fill()}
 ctx.fillStyle='rgba(40,80,60,.35)';ctx.beginPath();ctx.ellipse(ox+s*.08,oy,s*.55,s*.04,0,0,TAU);ctx.fill();
 const BR=build(W,H,s,ox,oy,rig),{list,T,FT,FS}=BR;
 list.forEach((sh,i)=>{let P=sh.P;const c={'#c08a48':'#f0b45a','#a8783e':'#d89a48','#7e4a22':'#e2653a','#d9a37c':'#ffd8b8','#5a4450':'#7a5aa0','#4c3a42':'#5e4684','#7a3e22':'#c0503a','#8a4a2a':'#d8603e','#2e1e18':'#3a2a50'}[sh.col]||sh.col;
  if(sh.mane&&BR.rig.mane.type==="spiky"){const M=[],cx=BR.maneC,mr=BR.maneR;for(let k=0;k<26;k++){const a=k/26*TAU,b=Math.max(0,Math.cos(a)),r1=mr*(1+b*.6)*(k%2?1.15:1),r0=mr*.72;M.push([cx[0]+Math.cos(a-.12)*r0,cx[1]+Math.sin(a-.12)*r0*1.15],[cx[0]+Math.cos(a)*r1,cx[1]+Math.sin(a)*r1*1.12])}
   ctx.fillStyle=c;ctx.beginPath();M.forEach((p,k)=>k?ctx.lineTo(...p):ctx.moveTo(...p));ctx.closePath();ctx.fill();P=M;const m=maskShift(W,H,P,-s*.05,-s*.06,0);tint(W,H,m,'#a83a2a',.9,ctx);ctx.save();ctx.strokeStyle='#4a1e14';ctx.lineWidth=1.6;ctx.lineJoin='miter';ctx.beginPath();M.forEach((p,k)=>k?ctx.lineTo(...p):ctx.moveTo(...p));ctx.closePath();ctx.stroke();ctx.restore();return}
  ctx.fillStyle=c;sm(ctx,P);ctx.fill();tint(W,H,maskShift(W,H,P,-s*.05,-s*.065,0),sh.face?'#f0a890':mixc(dk(c,.3),'#5a4ab0',.25),.95,ctx);
  if(!sh.face&&!sh.far){const m=maskShift(W,H,P,s*.025,s*.03,0);tint(W,H,m,'#ffffff',.35,ctx)}
  outline(ctx,P,sh.far?1.2:1.8,'#3a2018');
  if(sh.wing&&!sh.far)BR.bones.forEach(Q=>outline(ctx,Q,1.5,'#2e1e40',false));
  if(sh.face){ctx.save();ctx.fillStyle='rgba(255,120,120,.45)';for(const sx of[-1,1]){const p=T([[-.49+sx*.05,-.72]])[0];ctx.beginPath();ctx.ellipse(p[0],p[1],s*.016,s*.006,0,0,TAU);ctx.fill()}ctx.restore();
   face(ctx,FT,FS,{ink:'#2a1410',white:'#ffffff',iris:'#d2452a',eye:1.55,tall:1.8,iris_r:1.25,bigShine:1,mouth:'#8a2a2a',teeth:'#ffffff',lid:.007,brow:.006,lines:false,angry:1})}});extras(ctx,BR,'#3a2018',1.4);
});
/* 3. 3D ANIMATED: soft round 3-D shading, saturated warm subsurface shadows, blue rim light, big expressive eyes */
def('cgi','3 · 3D animated film','smooth 3-D shading, warm glowing shadows, rim light, appealing big eyes',(ctx,W,H,s,ox,oy,rig)=>{
 const bg=ctx.createRadialGradient(W*.5,H*.4,10,W*.5,H*.5,W*.75);bg.addColorStop(0,'#f4d9a8');bg.addColorStop(1,'#b06a4a');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);
 groundShadow(ctx,ox+s*.08,oy,s*.6,s*.05,.4,10);const BR=build(W,H,s,ox,oy,rig),{list,T,FT,FS}=BR;
 list.forEach(sh=>{const P=sh.P,c=sh.far?dk(sh.col,.22):mixc(sh.col,'#ff9a40',.12);
  smooth(ctx,W,H,P,c,s,{hi:.4,lo:.35,soft:.09,shadow:mixc(dk(c,.35),'#c02010',.3),shadowA:.65,bounce:'#ffcf80'});
  if(!sh.far)rimLight(ctx,W,H,P,'#9ad0ff',s,.55,[1,-.6],.012);
  if(sh.seg||sh.sting){const B=bbox(P);ctx.fillStyle='rgba(255,255,255,.6)';ctx.beginPath();ctx.ellipse(B.x0+B.w*.35,B.y0+B.h*.3,B.w*.12,B.h*.08,-.4,0,TAU);ctx.fill()}
  if(sh.wing&&!sh.far)BR.bones.forEach(Q=>{ctx.save();ctx.strokeStyle=dk(c,.3);ctx.lineWidth=s*.013;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(...Q[0]);ctx.lineTo(...Q[1]);ctx.stroke();ctx.restore()});
  if(sh.mane)strokes(ctx,P,500,s*.06,(x,y,B,R)=>R()<.5?'#c86a30':'#5a2a10',2.2,maneFlow(BR.maneC),3,{alpha:.45});
  if(sh.face)face(ctx,FT,FS,{ink:'#4a2418',white:'#fffaf0',iris:'#3a8a5a',eye:1.35,tall:1.4,iris_r:1.15,bigShine:1,mouth:'#5a1a14',teeth:'#fffaf0',noseShade:'#c06a4a',lid:.006})});extras(ctx,BR,'rgba(90,40,20,.5)',1.6);
});
/* 4. PIXEL ART: the anime draft drawn at a fifth of the size, cut to a 20-colour palette, outlined, scaled up with no smoothing */
const PAL=['#1a1220','#3a2430','#5e3a2a','#8a4a2a','#b86a30','#e09a48','#f4c878','#fff0c8','#ffd0b0','#e0907a','#a84a3a','#6a5aa0','#4a3a78','#2a2a50','#5a8a4a','#9ac46a','#d0ec98','#7ec4f2','#cde8f8','#ffffff'].map(hx);
def('pixel','4 · Pixel art','16-bit sprite: low resolution, 20-colour palette, 1-pixel outline (like Stardew Valley)',(ctx,W,H,s,ox,oy,rig)=>{const k=5,w=Math.ceil(W/k),h=Math.ceil(H/k),c=mk(w,h),g=c.getContext('2d');
 STY.find(x=>x.id==='anime').fn(g,w,h,s/k,ox/k,oy/k,rig);const im=g.getImageData(0,0,w,h),d=im.data;
 for(let i=0;i<d.length;i+=4){let best=0,bd=1e9;for(let j=0;j<PAL.length;j++){const p=PAL[j],e=(d[i]-p[0])**2+(d[i+1]-p[1])**2+(d[i+2]-p[2])**2;if(e<bd){bd=e;best=j}}d[i]=PAL[best][0];d[i+1]=PAL[best][1];d[i+2]=PAL[best][2]}g.putImageData(im,0,0);
 ctx.imageSmoothingEnabled=false;ctx.drawImage(c,0,0,w*k,h*k);ctx.strokeStyle='rgba(0,0,0,.06)';for(let x=0;x<W;x+=k){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,H);ctx.stroke()}for(let y=0;y<H;y+=k){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke()}});
/* 5. LOW-POLY: every shape cut into flat-lit triangles, like a faceted 3-D model */
def('lowpoly','5 · Low-poly 3D','flat-shaded facets, like a stylised 3-D game model',(ctx,W,H,s,ox,oy,rig)=>{
 const bg=ctx.createLinearGradient(0,0,W,H);bg.addColorStop(0,'#2a3a5a');bg.addColorStop(1,'#6a4a6a');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);const R0=rng(2);for(let i=0;i<40;i++){ctx.fillStyle=`rgba(255,255,255,${R0()*.05})`;ctx.beginPath();const x=R0()*W,y=R0()*H;ctx.moveTo(x,y);ctx.lineTo(x+R0()*120,y+R0()*60);ctx.lineTo(x-R0()*60,y+R0()*120);ctx.fill()}
 ctx.fillStyle='rgba(0,0,0,.35)';ctx.beginPath();ctx.moveTo(ox-s*.5,oy);ctx.lineTo(ox+s*.7,oy-s*.02);ctx.lineTo(ox+s*.6,oy+s*.04);ctx.lineTo(ox-s*.4,oy+s*.04);ctx.fill();
 const BR=build(W,H,s,ox,oy,rig),{list,T,FT,FS}=BR,Ld=[-.5,-.7,.5];
 list.forEach((sh,i)=>{const P=sh.P,B=bbox(P),cx=B.x0+B.w/2,cy=B.y0+B.h/2,c=sh.far?dk(sh.col,.25):sh.col,R=rng(i+3);
  const ring=P.filter((_,k)=>k%Math.max(1,Math.floor(P.length/14))===0),inner=ring.map(([x,y])=>[cx+(x-cx)*.55+(R()-.5)*4,cy+(y-cy)*.55+(R()-.5)*4]);
  const tri=[];for(let k=0;k<ring.length;k++){const a=ring[k],b=ring[(k+1)%ring.length],a2=inner[k],b2=inner[(k+1)%ring.length];tri.push([a,b,a2],[b,b2,a2],[a2,b2,[cx,cy]])}
  ctx.save();sm(ctx,P);ctx.clip();ctx.fillStyle=c;ctx.fillRect(B.x0,B.y0,B.w,B.h);
  tri.forEach(t=>{const mx=(t[0][0]+t[1][0]+t[2][0])/3,my=(t[0][1]+t[1][1]+t[2][1])/3,nx=(mx-cx)/(B.w/2+1),ny=(my-cy)/(B.h/2+1),nz=Math.sqrt(Math.max(.05,1-nx*nx-ny*ny)),l=Math.max(0,(nx*Ld[0]+ny*Ld[1]+nz*Ld[2]+.4)/1.4);
   ctx.fillStyle=l>.5?lt(c,(l-.5)*.7):dk(c,(.5-l)*1.1);ctx.strokeStyle=ctx.fillStyle;ctx.lineWidth=.6;ctx.beginPath();ctx.moveTo(...t[0]);ctx.lineTo(...t[1]);ctx.lineTo(...t[2]);ctx.closePath();ctx.fill();ctx.stroke()});ctx.restore();
  if(sh.face)face(ctx,FT,FS,{ink:'#2a1810',white:'#f0e8d8',iris:'#c88a20',mouth:'#2a0e0a',teeth:'#f0e8d8',shine:false,lines:false,slit:1})});
});
/* 6. COMIC BOOK: heavy black inks, spot blacks, halftone dots, bold flat colour, action burst */
def('comic','6 · Comic book','heavy inks, solid black shadows, halftone dots, bold colour',(ctx,W,H,s,ox,oy,rig)=>{
 ctx.fillStyle='#ffd23a';ctx.fillRect(0,0,W,H);ctx.save();ctx.translate(W*.45,H*.45);for(let k=0;k<28;k++){ctx.rotate(TAU/28);ctx.fillStyle=k%2?'#ff9a2a':'#ffd23a';ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(W,-40);ctx.lineTo(W,40);ctx.fill()}ctx.restore();
 const dots=(ctx,P,col,step,r)=>{ctx.save();sm(ctx,P);ctx.clip();ctx.fillStyle=col;const B=bbox(P);for(let y=B.y0;y<B.y1;y+=step)for(let x=B.x0+((y/step|0)%2)*step/2;x<B.x1;x+=step){ctx.beginPath();ctx.arc(x,y,r,0,TAU);ctx.fill()}ctx.restore()};
 ctx.fillStyle='#111';ctx.beginPath();ctx.ellipse(ox+s*.08,oy,s*.55,s*.035,0,0,TAU);ctx.fill();
 const BR=build(W,H,s,ox,oy,rig),{list,T,FT,FS}=BR;
 list.forEach((sh,i)=>{const P=sh.P,c={'#c08a48':'#f2a83a','#a8783e':'#c4802a','#7e4a22':'#c0281e','#d9a37c':'#f8c6a0','#5a4450':'#5a3a9a','#4c3a42':'#3a2470','#7a3e22':'#a8201a','#8a4a2a':'#d03020','#2e1e18':'#111'}[sh.col]||sh.col;
  ctx.fillStyle=c;sm(ctx,P);ctx.fill();const m1=maskShift(W,H,P,-s*.07,-s*.09,0);const tmp=mk(W,H),tg=tmp.getContext('2d');dots(tg,P,'rgba(0,0,0,.55)',5,1.6);tg.globalCompositeOperation='destination-in';tg.drawImage(m1,0,0);ctx.drawImage(tmp,0,0);
  tint(W,H,maskShift(W,H,P,-s*.025,-s*.03,0),'#111',1,ctx);outline(ctx,P,sh.far?2.5:3.6,'#111');
  if(sh.wing&&!sh.far)BR.bones.forEach(Q=>outline(ctx,Q,3,'#111',false));
  if(sh.mane)strokes(ctx,P,90,s*.07,'#111',2,maneFlow(BR.maneC),4,{alpha:1});
  if(sh.fur&&!sh.mane&&!sh.far)strokes(ctx,P,25,s*.03,'#111',1.6,furFlow,i,{alpha:1});
  if(sh.face)face(ctx,FT,FS,{ink:'#111',white:'#fff',iris:'#e02a1a',mouth:'#111',teeth:'#fff',lid:.008,brow:.012,lip:.007,angry:1,shine:false,open:1})});extras(ctx,BR,'#111',2.4);
});
/* 7. PAINTERLY CONCEPT ART: the photoreal render repainted in visible brush dabs over a loose painted background */
def('paint','7 · Painterly concept art','visible brush strokes, loose painted background, like a game\'s concept painting',(ctx,W,H,s,ox,oy,rig)=>{const c=mk(W,H),g=c.getContext('2d');STY[0].fn(g,W,H,s,ox,oy,rig);const d=g.getImageData(0,0,W,H).data,R=rng(8);
 ctx.fillStyle='#4a3a2a';ctx.fillRect(0,0,W,H);ctx.lineCap='round';for(const[n,sz]of[[3500,14],[9000,6],[14000,2.6]])for(let i=0;i<n;i++){const x=R()*W|0,y=R()*H|0,k=(y*W+x)*4;ctx.strokeStyle=`rgb(${d[k]},${d[k+1]},${d[k+2]})`;ctx.globalAlpha=.75;ctx.lineWidth=sz*(.6+R()*.8);const a=-.6+(R()-.5)*.6,L=sz*(1+R()*1.5);ctx.beginPath();ctx.moveTo(x-Math.cos(a)*L/2,y-Math.sin(a)*L/2);ctx.lineTo(x+Math.cos(a)*L/2,y+Math.sin(a)*L/2);ctx.stroke()}ctx.globalAlpha=1});
/* 8. DARK FANTASY: desaturated, grim, inked shadows, red rim light, glowing eyes, fog */
def('dark','8 · Dark fantasy','grim and gritty: drained colour, heavy inked shadow, red rim light, glowing eyes',(ctx,W,H,s,ox,oy,rig)=>{
 const bg=ctx.createRadialGradient(W*.55,H*.55,10,W*.5,H*.5,W*.7);bg.addColorStop(0,'#3a2a26');bg.addColorStop(1,'#080606');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);ctx.save();ctx.globalCompositeOperation='lighter';const g=ctx.createRadialGradient(W*.85,H*.5,0,W*.85,H*.5,W*.5);g.addColorStop(0,'rgba(200,40,20,.35)');g.addColorStop(1,'rgba(200,40,20,0)');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);ctx.restore();
 groundShadow(ctx,ox+s*.08,oy,s*.6,s*.05,.8,6);const BR=build(W,H,s,ox,oy,rig),{list,T,FT,FS}=BR;
 list.forEach((sh,i)=>{const P=sh.P,c=desat(sh.far?dk(sh.col,.4):dk(sh.col,.15),.55);smooth(ctx,W,H,P,c,s,{hi:.12,lo:.7,soft:.02,shadow:'#0a0606',shadowA:.85});
  const tmp=mk(W,H),tg=tmp.getContext('2d');tg.strokeStyle='#0a0606';tg.lineWidth=1;const R=rng(i);for(let d=-W;d<W*2;d+=4+R()*3){tg.beginPath();tg.moveTo(d,0);tg.lineTo(d-H*.6,H);tg.stroke()}tg.globalCompositeOperation='destination-in';tg.drawImage(maskShift(W,H,P,-s*.11,-s*.13,0),0,0);ctx.globalAlpha=.7;ctx.drawImage(tmp,0,0);ctx.globalAlpha=1;
  rimLight(ctx,W,H,P,'#ff3a1a',s,.9,[1,-.1],.004);outline(ctx,P,1.2,'#050303');
  if(sh.mane)strokes(ctx,P,700,s*.07,(x,y,B,R)=>R()<.3?'#5a3a2a':'#120a08',1.2,maneFlow(BR.maneC),5,{alpha:.7});
  if(sh.fur&&!sh.mane)strokes(ctx,P,400,s*.02,'#0e0806',.8,furFlow,i+2,{alpha:.4});
  if(sh.face){tint(W,H,maskShift(W,H,P,-s*.04,-s*.05,s*.01),'#0a0606',.6,ctx);face(ctx,FT,FS,{ink:'#0a0404',white:'#3a2a20',iris:'#ff6a20',glow:'rgba(255,120,30,.9)',mouth:'#0a0303',teeth:'#b8a890',pupil:false,lid:.006,brow:.01,angry:1,shine:false,open:1})}});extras(ctx,BR,'#050303',1.4,{ribLight:'rgba(255,90,50,.55)'});
 ctx.save();for(let i=0;i<6;i++){const fg=ctx.createLinearGradient(0,oy-60-i*10,0,H);fg.addColorStop(0,'rgba(60,50,50,0)');fg.addColorStop(1,'rgba(60,50,50,.25)');ctx.fillStyle=fg;ctx.fillRect(0,oy-60-i*10,W,H)}ctx.restore()});
/* 9. SILHOUETTE: a black shape against mist, lit from behind by a pale moon: only the rim and the eyes show */
def('silhouette','9 · Silhouette and rim light','a black shape in the mist, back-lit; only the rim and eyes glow',(ctx,W,H,s,ox,oy,rig)=>{
 const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#0e2030');bg.addColorStop(.6,'#5a8aa0');bg.addColorStop(1,'#1a2a30');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);const m=ctx.createRadialGradient(W*.62,H*.42,0,W*.62,H*.42,H*.55);m.addColorStop(0,'rgba(230,250,255,.95)');m.addColorStop(.18,'rgba(200,235,250,.7)');m.addColorStop(1,'rgba(200,235,250,0)');ctx.fillStyle=m;ctx.fillRect(0,0,W,H);
 ctx.fillStyle='#0a1418';ctx.fillRect(0,oy-2,W,H);const R=rng(3);for(let i=0;i<9;i++){ctx.fillStyle=`rgba(10,20,24,${.4+R()*.4})`;const x=R()*W;ctx.beginPath();ctx.moveTo(x,oy);ctx.lineTo(x+4,oy-30-R()*120);ctx.lineTo(x+8,oy);ctx.fill()}
 const BR=build(W,H,s,ox,oy,rig),{list,T,FT,FS}=BR;list.forEach((sh,i)=>{const P=sh.P;ctx.fillStyle='#05090b';sm(ctx,P);ctx.fill();if(!sh.far)rimLight(ctx,W,H,P,'#c8f0ff',s,.95,[1.2,-.8],.006)});
 const F=FT([[-.527,-.758],[-.453,-.758]]);F.forEach(p=>{const g=ctx.createRadialGradient(p[0],p[1],0,p[0],p[1],FS*.035);g.addColorStop(0,'rgba(255,230,120,1)');g.addColorStop(.25,'rgba(255,180,60,.8)');g.addColorStop(1,'rgba(255,180,60,0)');ctx.fillStyle=g;ctx.fillRect(p[0]-s*.04,p[1]-s*.04,s*.08,s*.08)});
 const fg=ctx.createLinearGradient(0,oy-50,0,oy+10);fg.addColorStop(0,'rgba(160,200,215,0)');fg.addColorStop(1,'rgba(160,200,215,.5)');ctx.fillStyle=fg;ctx.fillRect(0,oy-50,W,60)});
/* 10. FLAT VECTOR: simple geometric shapes, flat colour, one tone of shadow, no outline, long shadow (modern mobile games) */
def('flat','10 · Flat vector','clean geometric shapes, flat colour, one shadow tone, no outlines',(ctx,W,H,s,ox,oy,rig)=>{
 ctx.fillStyle='#f3e6d0';ctx.fillRect(0,0,W,H);ctx.fillStyle='#e8d4b4';ctx.beginPath();ctx.arc(W*.62,H*.42,H*.36,0,TAU);ctx.fill();ctx.fillStyle='#d8bf96';ctx.fillRect(0,oy,W,H);
 ctx.fillStyle='rgba(120,80,40,.25)';ctx.beginPath();ctx.moveTo(ox-s*.45,oy);ctx.lineTo(ox+s*.62,oy);ctx.lineTo(ox+s*1.1,oy+s*.12);ctx.lineTo(ox,oy+s*.12);ctx.fill();
 const BR=build(W,H,s,ox,oy,rig),{list,T,FT,FS}=BR;
 list.forEach(sh=>{const P=sh.P,c={'#c08a48':'#e3a24a','#a8783e':'#c98a3c','#7e4a22':'#b8542e','#d9a37c':'#f2c49c','#5a4450':'#6b4f7a','#4c3a42':'#54405f','#7a3e22':'#9a3f2c','#8a4a2a':'#b44c32','#2e1e18':'#3a2a3a'}[sh.col]||sh.col;
  ctx.fillStyle=c;sm(ctx,P);ctx.fill();tint(W,H,maskShift(W,H,P,-s*.06,-s*.08,0),dk(c,.18),1,ctx);
  if(sh.face)face(ctx,FT,FS,{ink:'#3a2420',white:'#ffffff',iris:'#3a2420',mouth:'#7a2a22',teeth:'#ffffff',shine:false,lines:false,pupil:false,lid:.003,brow:.008})})});

/* each style's own shape: proportions, pose and mane */
const RIGS={
 photoreal:rigOf({}),
 anime:rigOf({len:.84,shoulderH:.78,hipH:.75,chest:.3,belly:.17,rump:.26,legW:.85,paw:.055,head:1.3,chin:.6,mane:{type:'spiky',size:1.1},wing:{spread:.8,size:1.3},tail:{thick:.8,h:1.25,n:15},fore:[[0,0],[0,0],[-.03,0],[-.05,0]],foreFar:[[0,0],[.06,-.03],[.1,-.07],[.12,-.06]]}),
 cgi:rigOf({len:.6,shoulderH:.56,hipH:.5,chest:.38,belly:.33,rump:.3,hump:.03,legW:1.55,paw:.1,head:1.25,headY:.03,chin:.12,mane:{type:"clump",size:.95},wing:{spread:.1,size:.62},tail:{thick:1.45,h:.85,n:9}}),
 pixel:rigOf({len:.5,shoulderH:.44,hipH:.42,chest:.3,belly:.28,rump:.26,legW:1.7,paw:.1,head:1.45,chin:.1,mane:{type:"clump",size:.9},wing:{spread:.55,size:.6},tail:{thick:1.6,h:.8,n:7},straight:1}),
 lowpoly:rigOf({legW:1.1,mane:{type:'geo',size:1.05},poly:1,wing:{spread:.3,size:1}}),
 comic:rigOf({len:.8,shoulderH:.7,hipH:.6,chest:.48,belly:.2,rump:.3,hump:.06,legW:1.35,paw:.085,head:1.1,mane:{type:'flow',size:1.3},wing:{spread:1,size:1.3},tail:{thick:1.2,h:1.15},lean:.2,
   fore:[[0,0],[.02,-.06],[-.1,-.14],[-.2,-.12]],foreFar:[[0,0],[.07,-.03],[-.02,-.1],[-.07,-.09]]}),
 paint:rigOf({shoulderH:.58,hipH:.64,chest:.32,headY:.13,headX:-.04,mane:{type:'flow',size:1.05},wing:{spread:.05,size:.95},
   fore:[[0,0],[0,.03],[-.07,0],[-.12,0]],foreFar:[[0,0],[.05,0],[.03,-.09],[-.01,-.08]],hind:[[0,0],[0,.04],[.03,.03],[0,0]]}),
 dark:rigOf({len:.9,shoulderH:.8,hipH:.7,chest:.36,belly:.13,rump:.24,hump:.12,sag:-.07,legW:.6,paw:.07,head:1,headY:.12,chin:.55,mane:{type:'tatter',size:1.2},wing:{spread:.55,size:1.3,tatter:1},tail:{thick:.72,h:1.35,n:18},ribs:1}),
 silhouette:rigOf({len:.86,shoulderH:.84,hipH:.8,chest:.32,belly:.16,rump:.24,hump:.04,legW:.58,paw:.05,mane:{type:'spiky',size:1.35},wing:{spread:1,size:1.55,tatter:.5},tail:{thick:.8,h:1.5,n:16}}),
 flat:rigOf({len:.7,shoulderH:.58,hipH:.56,chest:.34,belly:.3,rump:.3,legW:1.3,paw:.08,head:1.3,chin:.2,mane:{type:'round',size:1.05},wing:{spread:.25,size:.8},tail:{thick:1.25,h:.95,n:8},straight:1})};
/* HOUSE STYLE (25 Nov 2026): style 1's photorealistic rendering on style 9's proportions, lit like 9 (back-lit by a pale moon through mist) */
def('house','House style · 1 + 9','photoreal fur and form (1) on the tall spidery body (9), back-lit by moonlight with a cool rim and glowing eyes (9)',(ctx,W,H,s,ox,oy,rig)=>{
 const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#0e1c28');bg.addColorStop(.6,'#4e7486');bg.addColorStop(1,'#18242a');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);
 const m=ctx.createRadialGradient(W*.64,H*.4,0,W*.64,H*.4,H*.6);m.addColorStop(0,'rgba(230,248,255,.9)');m.addColorStop(.2,'rgba(190,225,240,.55)');m.addColorStop(1,'rgba(190,225,240,0)');ctx.fillStyle=m;ctx.fillRect(0,0,W,H);
 ctx.save();ctx.filter='blur(3px)';const R0=rng(3);for(let i=0;i<9;i++){ctx.fillStyle=`rgba(12,22,26,${.35+R0()*.35})`;const x=R0()*W;ctx.beginPath();ctx.moveTo(x,oy);ctx.lineTo(x+5,oy-40-R0()*130);ctx.lineTo(x+10,oy);ctx.fill()}ctx.restore();ctx.fillStyle='#0c1418';ctx.fillRect(0,oy-2,W,H);
 groundShadow(ctx,ox+s*.02,oy,s*.6,s*.04,.7,6);
 const BR=build(W,H,s,ox,oy,rig),{list,T,FT,FS}=BR,mc=BR.maneC,cool=c=>mixc(desat(c,.35),'#2a3a48',.42);
 const RIM=(P,a)=>{tint(W,H,maskShift(W,H,P,-s*.009,s*.006,s*.003),'#cdeeff',a,ctx,'lighter')};
 const fuzz=(P,c)=>{const R=rng(P.length*13),n=P.length;ctx.save();ctx.lineCap='round';for(let k=0;k<n*9;k++){const i=Math.floor(R()*n),a=P[i],b=P[(i+1)%n],t=R(),x=a[0]+(b[0]-a[0])*t,y=a[1]+(b[1]-a[1])*t,nx=b[1]-a[1],ny=-(b[0]-a[0]),l=Math.hypot(nx,ny)||1,L=s*(.01+R()*.02),out=(nx/l)*.6+.4,up=-(ny/l);
   const lit=(nx/l)>.1||(ny/l)<-.2;ctx.strokeStyle=lit?'rgba(215,240,255,.75)':dk(c,.3);ctx.globalAlpha=.6;ctx.lineWidth=.8;ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x+nx/l*L+(R()-.5)*L*.6,y+ny/l*L+(R()-.5)*L*.6);ctx.stroke()}ctx.restore()};
 list.forEach((sh,i)=>{const P=sh.P,c=cool(sh.far?dk(sh.col,.35):sh.col);
  if(sh.wing){smooth(ctx,W,H,P,c,s,{hi:.12,lo:.55,soft:.04,shadow:'#0a1014',shadowA:.7});ctx.save();sm(ctx,P);ctx.clip();const B=bbox(P),g=ctx.createRadialGradient(B.x1,B.y0,0,B.x1,B.y0,B.w*.9);g.addColorStop(0,'rgba(200,160,170,.35)');g.addColorStop(1,'rgba(200,160,170,0)');ctx.fillStyle=g;ctx.fillRect(B.x0,B.y0,B.w,B.h);ctx.strokeStyle='rgba(140,110,120,.3)';ctx.lineWidth=1;const R=rng(i+9);for(let k=0;k<40;k++){ctx.beginPath();let x=B.x0+R()*B.w,y=B.y0+R()*B.h;ctx.moveTo(x,y);for(let q=0;q<5;q++){x+=(R()-.3)*10;y+=(R()-.5)*8;ctx.lineTo(x,y)}ctx.stroke()}ctx.restore();
   if(!sh.far)BR.bones.forEach(Q=>{ctx.save();ctx.strokeStyle=dk(c,.4);ctx.lineWidth=s*.011;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(...Q[0]);ctx.lineTo(...Q[1]);ctx.stroke();ctx.restore()});RIM(P,.9);return}
  if(sh.seg||sh.sting){smooth(ctx,W,H,P,c,s,{hi:.1,lo:.6,soft:.01,shadowA:.45});const B=bbox(P);ctx.fillStyle='rgba(220,240,255,.55)';ctx.beginPath();ctx.ellipse(B.x0+B.w*.65,B.y0+B.h*.25,B.w*.14,B.h*.08,.5,0,TAU);ctx.fill();RIM(P,.7);return}
  if(sh.face){smooth(ctx,W,H,P,mixc(sh.col,'#3e4a56',.5),s,{hi:.04,lo:.5,soft:.06,shadow:'#3a2a2a',shadowA:.5});RIM(P,.45);
   face(ctx,FT,FS,{ink:'#1e1410',white:'#8a8a80',iris:'#ffb040',glow:'rgba(255,190,80,.85)',mouth:'#150a08',teeth:'#b8b4a4',noseShade:'#2a1a18',lidShade:1,brow:.008,angry:1});return}
  smooth(ctx,W,H,P,c,s,{hi:.12,lo:.6,soft:.07,shadow:'#0a1216',shadowA:.65});
  const flow=sh.mane?maneFlow(mc):furFlow,B=bbox(P),n=sh.mane?2600:Math.min(2600,B.w*B.h/10),L=sh.mane?s*.06:s*.018;
  strokes(ctx,P,n,L,(x,y,B,R)=>{const t=(x-B.x0)/B.w*.5+(B.y1-y)/B.h*.5;return R()<.45?lt(c,.1+t*.35):dk(c,.25+(1-t)*.4)},sh.mane?1.1:.8,flow,i*31+5);
  if(!sh.far){RIM(P,.85);fuzz(P,c)}});
 extras(ctx,BR,'rgba(10,16,20,.6)',1.2);
 const fg=ctx.createLinearGradient(0,oy-60,0,oy+10);fg.addColorStop(0,'rgba(150,190,205,0)');fg.addColorStop(1,'rgba(150,190,205,.45)');ctx.fillStyle=fg;ctx.fillRect(0,oy-60,W,70)});
RIGS.house=rigOf({len:.86,shoulderH:.84,hipH:.8,chest:.32,belly:.16,rump:.24,hump:.04,legW:.62,paw:.055,mane:{type:'shag',size:1.3},wing:{spread:1,size:1.5,tatter:.5},tail:{thick:1.05,h:1.5,n:24}});
/* HOUSE STYLE v2: accurate proportions (draft 1's rig), draft 9's lighting. One merged silhouette, back-lit by a pale moon:
   only the outer edge catches a cool rim, hair breaks the edge, faint inner contours keep the parts readable, the eyes glow. */
def('house2','House style','accurate proportions (1), back-lit silhouette lighting (9)',(ctx,W,H,s,ox,oy,rig)=>{
 const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#0e1c28');bg.addColorStop(.6,'#56808f');bg.addColorStop(1,'#18242a');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);
 const m=ctx.createRadialGradient(W*.62,H*.42,0,W*.62,H*.42,H*.6);m.addColorStop(0,'rgba(232,248,255,.95)');m.addColorStop(.18,'rgba(196,230,244,.6)');m.addColorStop(1,'rgba(196,230,244,0)');ctx.fillStyle=m;ctx.fillRect(0,0,W,H);
 ctx.fillStyle='#0a1216';ctx.fillRect(0,oy-1,W,H);
 const BR=build(W,H,s,ox,oy,rig),{list,FT,FS}=BR;HOUSE_PAINT(ctx,W,H,s,BR);
 const fg=ctx.createLinearGradient(0,oy-60,0,oy+10);fg.addColorStop(0,'rgba(150,190,205,0)');fg.addColorStop(1,'rgba(150,190,205,.4)');ctx.fillStyle=fg;ctx.fillRect(0,oy-60,W,70)});
function HOUSE_PAINT(ctx,W,H,s,BR){const {list,FT,FS}=BR,u=mk(W,H),g=u.getContext('2d'),body='#070c0f';
 g.fillStyle=body;list.forEach(sh=>{sm(g,sh.P);g.fill()});
 /* hair breaking the edge: mane strands outward, short fuzz on furred parts */
 const R=rng(9);g.strokeStyle=body;g.lineCap='round';list.forEach(sh=>{if(!sh.fur)return;const P=sh.P,n=P.length,mane=sh.mane,c=mane?BR.maneC:null;for(let k=0;k<n*(mane?14:4);k++){const i=Math.floor(R()*n),a=P[i],b=P[(i+1)%n],t=R(),x=a[0]+(b[0]-a[0])*t,y=a[1]+(b[1]-a[1])*t;let nx,ny;if(mane){nx=x-c[0];ny=y-c[1]}else{nx=b[1]-a[1];ny=-(b[0]-a[0])}const l=Math.hypot(nx,ny)||1,L=s*(mane?.02+R()*.045:.006+R()*.012);
  g.lineWidth=mane?1.4+R()*1.6:1;g.beginPath();g.moveTo(x-nx/l*L*.3,y-ny/l*L*.3);g.quadraticCurveTo(x+nx/l*L*.5+(R()-.5)*L*.4,y+ny/l*L*.5,x+nx/l*L+(R()-.5)*L*.5,y+ny/l*L+(R()-.3)*L*.4);g.stroke()}});
 /* faint inner contours: where a near part overlaps a far one, its lit edge shows a little */
 g.save();g.globalCompositeOperation='source-atop';list.forEach(sh=>{if(sh.far||sh.name==='torso')return;g.strokeStyle='rgba(90,130,150,.22)';g.lineWidth=1.2;g.save();g.translate(1,-1);sm(g,sh.P);g.stroke();g.restore()});
 BR.bones.forEach(Q=>{g.strokeStyle='rgba(110,150,170,.25)';g.lineWidth=1.4;g.beginPath();g.moveTo(...Q[0]);g.lineTo(...Q[1]);g.stroke()});
 /* a whisper of form: the moon behind lifts the top edge of each shape */
 const lg=g.createLinearGradient(0,0,W*.3,H);lg.addColorStop(0,'rgba(60,90,105,.25)');lg.addColorStop(1,'rgba(0,0,0,0)');g.fillStyle=lg;g.fillRect(0,0,W,H);g.restore();
 ctx.drawImage(u,0,0);
 /* the rim: the silhouette minus itself moved away from the moon (left and down), lit cool; a softer glow beyond */
 const rim=(d,blur,col,a)=>{const r=mk(W,H),q=r.getContext('2d');q.drawImage(u,0,0);q.globalCompositeOperation='destination-out';q.drawImage(u,-d,d*.7);q.globalCompositeOperation='source-in';q.fillStyle=col;q.fillRect(0,0,W,H);ctx.save();ctx.globalCompositeOperation='lighter';ctx.globalAlpha=a;if(blur)ctx.filter=`blur(${blur}px)`;ctx.drawImage(r,0,0);ctx.restore()};
 rim(Math.max(1.2,s*.005),0,'#d6f2ff',.95);rim(Math.max(2,s*.012),Math.max(1,s*.006),'#9fd8f0',.45);
 /* glowing eyes */
 FT([[-.527,-.758],[-.453,-.758]]).forEach(p=>{const r=FS*.03,gr=ctx.createRadialGradient(p[0],p[1],0,p[0],p[1],r);gr.addColorStop(0,'rgba(255,236,150,1)');gr.addColorStop(.25,'rgba(255,180,60,.85)');gr.addColorStop(1,'rgba(255,170,60,0)');ctx.fillStyle=gr;ctx.fillRect(p[0]-r,p[1]-r,2*r,2*r)})}
RIGS.house2=RIGS.photoreal;
