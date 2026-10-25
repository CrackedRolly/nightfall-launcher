/* Nightfall meteor shower background. No libraries. Kept cheap:
   static stars are drawn once on their own canvas layer, only a few twinkle,
   frames drop to ~12 fps when no meteor is in flight, and it stops when the tab is hidden. */
(function(){
  if(window.__nfMeteors)return;window.__nfMeteors=1;
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  var c=document.createElement('canvas');c.setAttribute('aria-hidden','true');
  c.style.cssText='position:fixed;inset:0;width:100%;height:100%;z-index:-1;pointer-events:none';
  var L=c.cloneNode();document.body.insertBefore(c,document.body.firstChild);document.body.insertBefore(L,c);
  var x=c.getContext('2d'),lx=L.getContext('2d');
  var W=0,H=0,dpr=1,tw=[],ms=[],last=0,t0=0,raf=0,lastDraw=0,nextBurst=8,acc=0;
  function small(){return W<700}
  function size(){
    dpr=Math.min(window.devicePixelRatio||1,1.5);W=innerWidth;H=innerHeight;
    c.width=L.width=Math.round(W*dpr);c.height=L.height=Math.round(H*dpr);
    x.setTransform(dpr,0,0,dpr,0,0);lx.setTransform(dpr,0,0,dpr,0,0);
    lx.clearRect(0,0,W,H);lx.fillStyle='#fff';tw=[];
    var n=Math.round(W*H/(small()?9000:6500));
    for(var i=0;i<n;i++){var s=[Math.random()*W,Math.random()*H,Math.random()*1.2+.3,Math.random()*6.28];
      if(i%9===0)tw.push(s);else{lx.globalAlpha=.25+Math.random()*.4;lx.fillRect(s[0],s[1],s[2],s[2])}}
    lx.globalAlpha=1;draw(0);
  }
  function spawn(fast){
    var ang=Math.PI/4+(Math.random()-.5)*.25,sp=(fast?900:650)+Math.random()*500;
    ms.push({x:Math.random()*W*1.2-W*.1,y:-20-Math.random()*H*.3,vx:Math.cos(ang)*sp,vy:Math.sin(ang)*sp,
      len:(small()?90:160)+Math.random()*140,w:1+Math.random()*1.4,life:0,max:.9+Math.random()*.9});
  }
  function draw(t){
    x.clearRect(0,0,W,H);x.fillStyle='#fff';
    for(var i=0;i<tw.length;i++){var s=tw[i];x.globalAlpha=reduce?.5:.3+.4*Math.sin(t*1.4+s[3]);x.fillRect(s[0],s[1],s[2],s[2])}
    x.globalAlpha=1;
  }
  function frame(now){
    raf=requestAnimationFrame(frame);
    if(!last){last=now;t0=now}
    var dt=Math.min((now-last)/1000,.05);last=now;var t=(now-t0)/1000;
    var cap=small()?8:18,rate=t<4?(small()?5:10):(small()?.4:.8);
    acc+=rate*dt;while(acc>1){acc--;if(ms.length<cap)spawn(t<4)}
    if(t>nextBurst){for(var i=0,k=small()?3:5;i<k&&ms.length<cap;i++)spawn(true);nextBurst=t+12+Math.random()*10}
    if(!ms.length&&now-lastDraw<80)return; // idle sky: ~12 fps is plenty for twinkling
    lastDraw=now;draw(t);x.lineCap='round';
    for(var j=ms.length-1;j>=0;j--){var m=ms[j];m.life+=dt;m.x+=m.vx*dt;m.y+=m.vy*dt;
      var f=Math.min(1,m.life*4)*Math.max(0,1-m.life/m.max);
      if(f<=0||m.y>H+300||m.x>W+300){ms.splice(j,1);continue}
      var sp=Math.hypot(m.vx,m.vy),tx=m.x-m.vx/sp*m.len,ty=m.y-m.vy/sp*m.len;
      var g=x.createLinearGradient(m.x,m.y,tx,ty);
      g.addColorStop(0,'rgba(255,255,255,'+(.95*f)+')');g.addColorStop(.3,'rgba(210,212,218,'+(.4*f)+')');g.addColorStop(1,'rgba(160,162,170,0)');
      x.strokeStyle=g;x.lineWidth=m.w;x.beginPath();x.moveTo(m.x,m.y);x.lineTo(tx,ty);x.stroke();
      x.fillStyle='rgba(255,255,255,'+f+')';x.beginPath();x.arc(m.x,m.y,m.w*1.1,0,6.283);x.fill()}
  }
  var rt;addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(size,120)});
  size();
  if(reduce){for(var i=0;i<4;i++){var sx=W*(.2+.2*i),sy=H*(.1+.12*i),l=140,g=x.createLinearGradient(sx,sy,sx-l*.7,sy-l*.7);g.addColorStop(0,'rgba(255,255,255,.7)');g.addColorStop(1,'rgba(255,255,255,0)');x.strokeStyle=g;x.lineWidth=1.5;x.beginPath();x.moveTo(sx,sy);x.lineTo(sx-l*.7,sy-l*.7);x.stroke()}return}
  document.addEventListener('visibilitychange',function(){if(document.hidden){cancelAnimationFrame(raf);raf=0}else if(!raf){last=0;t0=performance.now()-5000;raf=requestAnimationFrame(frame)}});
  raf=requestAnimationFrame(frame);
})();
