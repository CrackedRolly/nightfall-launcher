/* Nightfall site i18n: English is baked into the HTML; other languages load from i18n/<lang>.json. */
(function(){
  var LANGS=['en','ro','es','pt-BR','de','fr','it','pl','ru','tr'];
  var root=document.documentElement;
  function pick(){
    var q=new URLSearchParams(location.search).get('lang');if(q&&LANGS.indexOf(q)>=0)return q;
    try{var s=localStorage.getItem('nf-lang');if(s&&LANGS.indexOf(s)>=0)return s}catch(e){}
    var nav=navigator.languages||[navigator.language||'en'];
    for(var i=0;i<nav.length;i++){var l=(nav[i]||'').toLowerCase();
      if(l.indexOf('pt')===0)return 'pt-BR';var b=l.split('-')[0];if(LANGS.indexOf(b)>=0)return b}
    return 'en';
  }
  var lang=pick(),dict=null,en={};
  window.NF={lang:lang,t:function(k,f){return (dict&&dict[k])||en[k]||f||k},ver:'0.1.1'};
  if(lang!=='en'){root.classList.add('i18n-wait');setTimeout(function(){root.classList.remove('i18n-wait')},1200)}
  function apply(){
    var els=document.querySelectorAll('[data-i18n]');
    for(var i=0;i<els.length;i++){var el=els[i],k=el.getAttribute('data-i18n');
      if(!(k in en))en[k]=el.innerHTML;
      var v=(dict&&dict[k])||en[k];if(el.hasAttribute('data-v'))v=v.replace('{v}',NF.ver).replace(/0\.1\.1/,NF.ver);
      el.innerHTML=v}
    var alts=document.querySelectorAll('[data-i18n-alt]');
    for(i=0;i<alts.length;i++){var a=alts[i],ak=a.getAttribute('data-i18n-alt');if(!(('alt:'+ak) in en))en['alt:'+ak]=a.alt;a.alt=(dict&&dict[ak])||en['alt:'+ak]}
    root.lang=lang;
    var tk=document.body.getAttribute('data-title-key');if(tk&&dict&&dict[tk])document.title=dict[tk];
    if(tk==='meta.title'){var m=document.querySelector('meta[name=description]');if(m){if(!en._d)en._d=m.content;m.content=(dict&&dict['meta.desc'])||en._d}}
    var sel=document.getElementById('lang');if(sel)sel.value=lang;
    root.classList.remove('i18n-wait');
    document.dispatchEvent(new CustomEvent('nf:lang',{detail:lang}));
  }
  function load(l,cb){if(l==='en'){dict=null;cb();return}
    fetch('i18n/'+l+'.json',{cache:'force-cache'}).then(function(r){return r.json()}).then(function(d){dict=d;cb()}).catch(function(){dict=null;lang='en';cb()})}
  NF.setLang=function(l){lang=l;NF.lang=l;try{localStorage.setItem('nf-lang',l)}catch(e){}load(l,apply)};
  NF.refresh=apply;
  function fitLabels(){var sel=document.getElementById('lang');if(!sel)return;var narrow=matchMedia('(max-width:760px)').matches;
    for(var i=0;i<sel.options.length;i++){var o=sel.options[i];if(!o.dataset.full)o.dataset.full=o.textContent;o.textContent=narrow?o.dataset.full.split(' (')[0]:o.dataset.full}}
  function init(){
    fitLabels();try{matchMedia('(max-width:760px)').addEventListener('change',fitLabels)}catch(e){}
    var sel=document.getElementById('lang');if(sel){sel.value=lang;sel.addEventListener('change',function(){NF.setLang(sel.value)})}
    load(lang,apply);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
