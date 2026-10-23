(()=>{const list=[...document.querySelectorAll('.kb')],q=document.getElementById('q'),count=document.getElementById('count');let cat='';
const run=()=>{const s=q.value.trim().toLowerCase();let n=0;for(const d of list){const hit=(!cat||d.dataset.cat===cat)&&(!s||d.textContent.toLowerCase().includes(s));d.hidden=!hit;if(hit)n++}count.textContent=n};
q.addEventListener('input',run);
document.querySelectorAll('.chip').forEach(b=>b.onclick=()=>{cat=b.dataset.cat;document.querySelectorAll('.chip').forEach(x=>x.classList.toggle('on',x===b));run()});
const open=()=>{const d=document.getElementById(decodeURIComponent(location.hash.slice(1)));if(d&&d.tagName==='DETAILS'){d.open=true;d.hidden=false;d.scrollIntoView({block:'start'})}};addEventListener('hashchange',open);open();
let kb;document.getElementById('chk').onclick=async()=>{const c=document.getElementById('checker');c.hidden=!c.hidden;if(!c.hidden)document.getElementById('log').focus();kb=kb||await (await fetch('data/crash-kb.json')).json()};
let tm;const res=document.getElementById('res');document.getElementById('log').addEventListener('input',e=>{clearTimeout(tm);tm=setTimeout(()=>{if(!kb)return;const t=e.target.value,m=t.match(/exit code:?\s*(-?\d+)/i)||t.match(/^\s*(-?\d+)\s*$/),hay=t+(m?'\n[Nightfall] exit code: '+m[1]:'');
const hits=kb.entries.map((x,i)=>({x,n:x.sig.filter(r=>new RegExp(r,'im').test(hay)).length,i})).filter(h=>h.n).sort((a,b)=>(b.n*10+(b.x.prio||0)-b.i/1000)-(a.n*10+(a.x.prio||0)-a.i/1000)).slice(0,4);
res.innerHTML=t.trim()?(hits.length?'<p class="note">'+res.dataset.likely+'</p>'+hits.map(h=>'<a href="#'+h.x.id+'">'+h.x.title.replace(/</g,'&lt;')+'</a>').join(''):'<p class="note">'+res.dataset.none+'</p>'):''},200)});})();
