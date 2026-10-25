(function(){
  var nav=document.getElementById('nav'),menu=document.getElementById('menu');
  function onScroll(){nav&&nav.classList.toggle('scrolled',scrollY>8)}addEventListener('scroll',onScroll,{passive:true});onScroll();
  if(menu)menu.addEventListener('click',function(){var o=nav.classList.toggle('open');menu.setAttribute('aria-expanded',o)});
  document.querySelectorAll('#links a').forEach(function(a){a.addEventListener('click',function(){nav.classList.remove('open');menu&&menu.setAttribute('aria-expanded','false')})});
  // reveal
  var rv=document.querySelectorAll('.rv');
  if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});rv.forEach(function(e){io.observe(e)})}
  else rv.forEach(function(e){e.classList.add('in')});
  // lightbox
  var lb=document.getElementById('lb');
  document.querySelectorAll('.shots img,.strip img').forEach(function(img){img.addEventListener('click',function(){lb.querySelector('img').src=img.src;lb.querySelector('img').alt=img.alt;lb.classList.add('on')})});
  if(lb){lb.addEventListener('click',function(){lb.classList.remove('on')});addEventListener('keydown',function(e){if(e.key==='Escape')lb.classList.remove('on')})}
  // latest release -> download link + version
  var API='https://api.github.com/repos/CrackedRolly/nightfall-launcher/releases';
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  fetch(API+'/latest').then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(rel){
    var v=(rel.tag_name||'').replace(/^v/,'');var exe=(rel.assets||[]).filter(function(a){return /\.exe$/i.test(a.name)})[0];
    if(v){window.NF&&(NF.ver=v);document.querySelectorAll('.ver').forEach(function(e){e.textContent=v})}
    if(exe)document.querySelectorAll('.dl-link').forEach(function(a){a.href=exe.browser_download_url});
    var app=(rel.assets||[]).filter(function(a){return /\.AppImage$/i.test(a.name)})[0];
    if(app)document.querySelectorAll('.linux-link').forEach(function(a){a.href=app.browser_download_url});
    window.NF&&NF.refresh&&NF.refresh();
  }).catch(function(){});
  // changelog
  var box=document.getElementById('releases');if(!box)return;
  var st=document.getElementById('log-status');
  function md(s){ // tiny markdown: headings, lists, bold, code, links
    var out=[],list=false;esc(s).split(/\r?\n/).forEach(function(l){
      l=l.replace(/\*\*(.+?)\*\*/g,'<b>$1</b>').replace(/`([^`]+)`/g,'<code>$1</code>').replace(/(^|[^*])\*([^*\s][^*]*?)\*/g,'$1<em>$2</em>').replace(/\[([^\]]+)\]\((https?:[^)\s]+)\)/g,'<a href="$2" rel="noopener">$1</a>');
      var m=l.match(/^\s*[-*]\s+(.*)/);
      if(m){if(!list){out.push('<ul>');list=true}out.push('<li>'+m[1]+'</li>');return}
      if(list){out.push('</ul>');list=false}
      var h=l.match(/^#{1,4}\s+(.*)/);if(h){out.push('<h3>'+h[1]+'</h3>');return}
      if(l.trim())out.push('<p>'+l+'</p>')});if(list)out.push('</ul>');return out.join('')}
  var T=function(k,f){return f};
  fetch(API+'?per_page=30').then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(list){
    list=list.filter(function(r){return !r.draft});if(!list.length)throw 0;
    box.innerHTML=list.map(function(r,i){
      var d=new Date(r.published_at||r.created_at);var ds=isNaN(d)?'':d.toLocaleDateString(document.documentElement.lang||'en',{year:'numeric',month:'long',day:'numeric'});
      var exe=(r.assets||[]).filter(function(a){return /\.exe$/i.test(a.name)})[0];
      return '<article class="rel"><div class="when"><div class="v">'+esc(r.tag_name)+(i===0&&!r.prerelease?'<span class="pill" data-i18n="log.latest">'+T('log.latest','Latest')+'</span>':'')+(r.prerelease?'<span class="pill" data-i18n="log.pre">'+T('log.pre','Pre-release')+'</span>':'')+'</div><div class="mono d">'+esc(ds)+'</div></div>'+
        '<div class="notes"><div class="body">'+md(r.body||'')+'</div><div class="dl">'+(exe?'<a class="btn sm primary" href="'+esc(exe.browser_download_url)+'"><span data-i18n="log.download">'+T('log.download','Download')+'</span></a>':'')+
        '<a class="btn sm" href="'+esc(r.html_url)+'" rel="noopener"><span data-i18n="log.github">'+T('log.github','View on GitHub')+'</span></a></div></div></article>'}).join('');
    st.style.display='none';window.NF&&NF.refresh&&NF.refresh();
  }).catch(function(){st.setAttribute('data-i18n','log.error');st.textContent="Couldn't reach GitHub right now. Showing the releases we know about.";window.NF&&NF.refresh()});
})();
