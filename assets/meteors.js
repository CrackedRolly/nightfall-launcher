/* Nightfall meteor shower background. No libraries. */
(function(){
  if (window.__nfMeteors) return; window.__nfMeteors = 1;
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var c = document.createElement('canvas');
  c.setAttribute('aria-hidden','true');
  c.style.cssText='position:fixed;inset:0;width:100%;height:100%;z-index:-1;pointer-events:none';
  document.body.insertBefore(c, document.body.firstChild);
  var x = c.getContext('2d'), W=0, H=0, dpr=1, stars=[], ms=[], last=0, t0=0, run=true, raf=0;
  function size(){
    dpr=Math.min(window.devicePixelRatio||1, 2); W=innerWidth; H=innerHeight;
    c.width=W*dpr; c.height=H*dpr; x.setTransform(dpr,0,0,dpr,0,0);
    stars=[]; var n=Math.round(W*H/(W<700?9000:6000));
    for(var i=0;i<n;i++) stars.push([Math.random()*W,Math.random()*H,Math.random()*1.2+.3,Math.random()*6.28]);
    if(reduce) drawStatic();
  }
  function small(){return W<700}
  function spawn(fast){
    var ang=(Math.PI/4)+(Math.random()-.5)*0.25, sp=(fast?900:650)+Math.random()*500;
    ms.push({x:Math.random()*W*1.2-W*0.1, y:-20-Math.random()*H*0.3, vx:-Math.cos(ang)*sp*0.0+Math.cos(ang)*sp, vy:Math.sin(ang)*sp,
      len:(small()?90:160)+Math.random()*140, w:1+Math.random()*1.6, life:0, max:0.9+Math.random()*0.9});
  }
  function drawStars(t){
    for(var i=0;i<stars.length;i++){var s=stars[i];
      x.globalAlpha=reduce?.5:.35+.35*Math.sin(t*1.5+s[3]);
      x.fillStyle='#fff'; x.fillRect(s[0],s[1],s[2],s[2]);}
    x.globalAlpha=1;
  }
  function drawStatic(){x.clearRect(0,0,W,H); drawStars(0);
    for(var i=0;i<4;i++){var sx=W*(.2+.2*i),sy=H*(.1+.12*i),l=140;
      var g=x.createLinearGradient(sx,sy,sx-l*.7,sy-l*.7);g.addColorStop(0,'rgba(255,255,255,.7)');g.addColorStop(1,'rgba(255,255,255,0)');
      x.strokeStyle=g;x.lineWidth=1.5;x.beginPath();x.moveTo(sx,sy);x.lineTo(sx-l*.7,sy-l*.7);x.stroke();}}
  var nextBurst=8, acc=0;
  function frame(now){
    raf=requestAnimationFrame(frame);
    if(!last){last=now;t0=now}
    var dt=Math.min((now-last)/1000,.05); last=now; var t=(now-t0)/1000;
    var cap=small()?10:22;
    // intro shower first ~4s, then gentle
    var rate = t<4 ? (small()?6:12) : (small()?0.5:0.9);
    acc+=rate*dt; while(acc>1){acc--; if(ms.length<cap) spawn(t<4);}
    if(t>nextBurst){ var k=small()?3:6; for(var i=0;i<k&&ms.length<cap;i++) spawn(true); nextBurst=t+10+Math.random()*10; }
    x.clearRect(0,0,W,H); drawStars(t);
    x.lineCap='round';
    for(var j=ms.length-1;j>=0;j--){var m=ms[j]; m.life+=dt; m.x+=m.vx*dt; m.y+=m.vy*dt;
      var f=Math.min(1,m.life*4)*Math.max(0,1-m.life/m.max);
      if(f<=0||m.y>H+300||m.x>W+300){ms.splice(j,1);continue}
      var sp=Math.hypot(m.vx,m.vy), tx=m.x-m.vx/sp*m.len, ty=m.y-m.vy/sp*m.len;
      var g=x.createLinearGradient(m.x,m.y,tx,ty);
      g.addColorStop(0,'rgba(255,255,255,'+(.95*f)+')'); g.addColorStop(.3,'rgba(210,214,222,'+(.45*f)+')'); g.addColorStop(1,'rgba(160,165,175,0)');
      x.strokeStyle=g; x.lineWidth=m.w; x.beginPath(); x.moveTo(m.x,m.y); x.lineTo(tx,ty); x.stroke();
      x.fillStyle='rgba(255,255,255,'+f+')'; x.beginPath(); x.arc(m.x,m.y,m.w*1.1,0,6.283); x.fill();}
  }
  size(); addEventListener('resize', size);
  if(reduce) return;
  document.addEventListener('visibilitychange',function(){
    if(document.hidden){cancelAnimationFrame(raf);raf=0}else if(!raf){last=0;t0=performance.now()-5000;raf=requestAnimationFrame(frame)}});
  raf=requestAnimationFrame(frame);
})();
