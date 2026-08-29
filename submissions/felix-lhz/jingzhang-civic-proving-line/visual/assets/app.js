(() => {
  const data=window.V15_DATA;
  if(!data)return;
  const params=()=>new URLSearchParams(location.hash.slice(1));
  const save=(key,value)=>{const h=params();h.set(key,value);history.replaceState(null,'','#'+h)};
  function setAlt(id){
    document.querySelectorAll('[data-alt]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.alt===id)));
    document.getElementById('altGraphic').innerHTML=data.graphics[id];
    document.getElementById('altReason').textContent=data.reasons[id];
    save('alt',id);
  }
  function setState(state){
    document.querySelectorAll('[data-state]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.state===state)));
    document.body.dataset.state=state;
    const image=document.getElementById('evidenceImage');
    image.src=state==='OPEN'?data.detail:data.axon;
    image.alt='S7 '+state+' architectural state';
    save('state',state);
  }
  document.querySelectorAll('[data-alt]').forEach(b=>b.addEventListener('click',()=>setAlt(b.dataset.alt)));
  document.querySelectorAll('[data-state]').forEach(b=>b.addEventListener('click',()=>setState(b.dataset.state)));
  const h=params();
  setAlt(h.get('alt')||'ALT-C');
  setState(h.get('state')||'OPEN');
})();
