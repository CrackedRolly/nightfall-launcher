(function(){
  var nav=document.getElementById('nav'),menu=document.getElementById('menu');
  if(menu)menu.addEventListener('click',function(){var o=nav.classList.toggle('open');menu.setAttribute('aria-expanded',o);document.body.style.overflow=o?'hidden':''});
  document.querySelectorAll('#links a').forEach(function(a){a.addEventListener('click',function(){nav.classList.remove('open');menu&&menu.setAttribute('aria-expanded','false');document.body.style.overflow=''})});
  addEventListener('keydown',function(e){if(e.key==='Escape'&&nav.classList.contains('open')){nav.classList.remove('open');menu.setAttribute('aria-expanded','false');document.body.style.overflow='';menu.focus()}});
  // reveal
  var rv=document.querySelectorAll('.rv');
  if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -6% 0px'});rv.forEach(function(e){io.observe(e)})}
  else rv.forEach(function(e){e.classList.add('in')});
  // lightbox
  var lb=document.getElementById('lb');
  document.querySelectorAll('.strip img').forEach(function(img){img.addEventListener('click',function(){lb.querySelector('img').src=img.src;lb.querySelector('img').alt=img.alt;lb.classList.add('on')})});
  if(lb){lb.addEventListener('click',function(){lb.classList.remove('on')});addEventListener('keydown',function(e){if(e.key==='Escape')lb.classList.remove('on')})}
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function mb(n){return n?Math.round(n/1048576)+' MB':'—'}
  // OS detection
  var ua=navigator.userAgent||'',plat=((navigator.userAgentData&&navigator.userAgentData.platform)||navigator.platform||'').toLowerCase();
  var mobile=/android|iphone|ipad|ipod|mobile/i.test(ua),os=mobile?'other':/win/.test(plat)||/windows/i.test(ua)?'win':/mac/.test(plat)||/mac os/i.test(ua)?'other':/linux|x11|cros/i.test(plat+ua)?'linux':'win';
  if(os==='linux')document.querySelectorAll('.os-win').forEach(function(e){e.hidden=true}),document.querySelectorAll('.os-linux').forEach(function(e){e.hidden=false});
  if(os==='other')document.querySelectorAll('.elsewhere').forEach(function(e){e.hidden=false});
  var files=document.getElementById('files');
  if(files){var rec=files.querySelector('[data-kind="'+(os==='other'?'win':os)+'"]');if(rec&&os!=='other'){rec.classList.add('rec');rec.querySelector('.badge').hidden=false;files.insertBefore(rec,files.firstChild);var b=rec.querySelector('.dlb');if(b)b.classList.replace('sm','primary')}
    files.addEventListener('click',function(e){var b=e.target.closest('.copy');if(!b)return;var s=b.parentNode.querySelector('.sha').textContent.trim();
      (navigator.clipboard?navigator.clipboard.writeText(s):Promise.reject()).then(function(){var o=b.textContent;b.textContent=b.dataset.done;setTimeout(function(){b.textContent=o},1500)}).catch(function(){var r=document.createRange();r.selectNodeContents(b.parentNode.querySelector('.sha'));getSelection().removeAllRanges();getSelection().addRange(r)})})}
  // latest release -> buttons, version, spec sheet, download cards
  var API='https://api.github.com/repos/CrackedRolly/nightfall-launcher/releases';
  fetch(API+'/latest').then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(rel){
    var v=(rel.tag_name||'').replace(/^v/,''),as=rel.assets||[];
    function find(rx){return as.filter(function(a){return rx.test(a.name)})[0]}
    var exe=find(/\.exe$/i),app=find(/\.AppImage$/i),zip=find(/win.*\.zip$/i);
    if(v)window.NF&&(NF.ver=v);
    document.querySelectorAll('.dl-main').forEach(function(a){var f=os==='linux'?app:exe;if(os==='other')a.href='download.html';else if(f)a.href=f.browser_download_url});
    var d=new Date(rel.published_at);document.querySelectorAll('.rel-date').forEach(function(e){e.textContent=isNaN(d)?'':d.toISOString().slice(0,10)});
    if(exe)document.querySelectorAll('.rel-size').forEach(function(e){e.textContent=mb(exe.size)});
    if(files){[['win',exe],['linux',app],['zip',zip]].forEach(function(p){var c=files.querySelector('[data-kind="'+p[0]+'"]'),a=p[1];if(!c||!a)return;
      var fn=c.querySelector('.fn');if(fn)fn.textContent=a.name;var sz=c.querySelector('.sz');if(sz)sz.textContent=mb(a.size);
      var sh=c.querySelector('.sha');if(sh)sh.textContent=(a.digest||'').replace('sha256:','')||'—';var b=c.querySelector('.dlb');if(b)b.href=a.browser_download_url})}
    window.NF&&NF.refresh&&NF.refresh();
  }).catch(function(){});
  // Discord live counts
  var dc=document.getElementById('dc-count');
  if(dc)fetch('https://discord.com/api/v9/invites/PGanscBPUt?with_counts=true').then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(j){
    if(!j.approximate_member_count)return;document.getElementById('dc-on').textContent=j.approximate_presence_count||0;document.getElementById('dc-all').textContent=j.approximate_member_count;dc.hidden=false}).catch(function(){});
  // Modrinth live data
  var packs=document.querySelectorAll('.pack[data-slug]');
  if(packs.length){var ids=[].map.call(packs,function(p){return p.dataset.slug});
    fetch('https://api.modrinth.com/v2/projects?ids='+encodeURIComponent(JSON.stringify(ids))).then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(list){
      var by={};list.forEach(function(p){by[p.slug]=p});
      packs.forEach(function(el){var p=by[el.dataset.slug];if(!p)return;var n=p.downloads;
        el.querySelector('.dls').textContent=n>=1e6?(n/1e6).toFixed(1)+'M':Math.round(n/1e3)+'K';
        var gv=p.game_versions||[];if(gv.length)el.querySelector('.gv').textContent=gv[gv.length-1]})}).catch(function(){})}
  // changelog
  var box=document.getElementById('releases');if(!box)return;
  var st=document.getElementById('log-status'),jump=document.getElementById('jump');
  function md(s){var out=[],list=false;esc(s).split(/\r?\n/).forEach(function(l){
      l=l.replace(/\*\*(.+?)\*\*/g,'<b>$1</b>').replace(/`([^`]+)`/g,'<code>$1</code>').replace(/(^|[^*])\*([^*\s][^*]*?)\*/g,'$1<em>$2</em>').replace(/\[([^\]]+)\]\((https?:[^)\s]+)\)/g,'<a href="$2" rel="noopener">$1</a>');
      var m=l.match(/^\s*[-*]\s+(.*)/);
      if(m){if(!list){out.push('<ul>');list=true}out.push('<li>'+m[1]+'</li>');return}
      if(list){out.push('</ul>');list=false}
      var h=l.match(/^#{1,4}\s+(.*)/);if(h){out.push('<h3>'+h[1]+'</h3>');return}
      if(l.trim())out.push('<p>'+l+'</p>')});if(list)out.push('</ul>');return out.join('')}
  function T(k,f){return f}
  fetch(API+'?per_page=40').then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(list){
    list=list.filter(function(r){return !r.draft});if(!list.length)throw 0;
    box.innerHTML=list.map(function(r,i){
      var d=new Date(r.published_at||r.created_at);var ds=isNaN(d)?'':d.toLocaleDateString(document.documentElement.lang||'en',{year:'numeric',month:'long',day:'numeric'});
      var exe=(r.assets||[]).filter(function(a){return /\.exe$/i.test(a.name)})[0];
      return '<article class="rel" id="'+esc(r.tag_name)+'"><div class="when"><div class="v">'+esc(r.tag_name)+(i===0&&!r.prerelease?'<span class="pill" data-i18n="log.latest">'+T('log.latest','Latest')+'</span>':'')+(r.prerelease?'<span class="pill" data-i18n="log.pre">'+T('log.pre','Pre-release')+'</span>':'')+'</div><div class="mono d">'+esc(ds)+'</div></div>'+
        '<div class="notes"><div class="body">'+md(r.body||'')+'</div><div class="dl">'+(exe?'<a class="btn sm primary" href="'+esc(exe.browser_download_url)+'"><span data-i18n="log.download">'+T('log.download','Download')+'</span></a>':'')+
        '<a class="btn sm" href="'+esc(r.html_url)+'" rel="noopener"><span data-i18n="log.github">'+T('log.github','View on GitHub')+'</span></a></div></div></article>'}).join('');
    if(jump)jump.innerHTML=list.map(function(r){return '<a href="#'+esc(r.tag_name)+'">'+esc(r.tag_name)+'</a>'}).join('');
    st.style.display='none';window.NF&&NF.refresh&&NF.refresh();
    if(location.hash){var t=document.getElementById(decodeURIComponent(location.hash.slice(1)));if(t)t.scrollIntoView()}
  }).catch(function(){st.setAttribute('data-i18n','log.error');st.textContent="Couldn't reach GitHub right now. Showing the releases we know about.";window.NF&&NF.refresh()});
})();
