'use strict';
const logState={rows:[],visible:12};
const byId=id=>document.getElementById(id);
const htmlEscape=s=>String(s??'').replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
const flagName={red:'Previously raised as a red flag',green:'Previously acceptable or resolved',amber:'Required contextual judgement'};
const outcomeName={approve:'Accepted after review',reject:'Rejected',request_amendment:'Amendment requested',escalate:'Referred for closer review'};
const reviewName={T01:'Birchbridge',T02:'Brookside',T03:'Falcon',T04:'Elm',T05:'Moorland',T06:'Orchard'};
function matchingRows(){
  const review=byId('case-filter').value,flag=byId('flag-filter').value,query=byId('log-search').value.trim().toLowerCase();
  return logState.rows.filter(r=>(review==='all'||r.review_id===review)&&(flag==='all'||r.flag===flag)&&(!query||[r.id,r.issue,r.rationale,r.conditions,r.fictional_counterparty,r.review_id].join(' ').toLowerCase().includes(query)));
}
function renderRow(r){
  const source=r.related_fixed_example_id;
  const localBackend=location.hostname==='127.0.0.1'||location.hostname==='localhost';
  const sourceUrl=source?(localBackend?'/api/history/'+encodeURIComponent(source)+'/original':'/demo-data/originals/history/'+encodeURIComponent(source)+'.docx'):null;
  return '<article class="log-entry" data-flag="'+htmlEscape(r.flag)+'" aria-label="'+htmlEscape(r.id)+'">'+
    '<div class="log-entry-head"><span>'+htmlEscape(r.id)+' · '+htmlEscape(r.date)+' · '+htmlEscape(r.reviewer)+'</span><span>'+htmlEscape(flagName[r.flag])+'</span></div>'+
    '<h3>'+htmlEscape(r.issue)+'</h3>'+
    '<p class="outcome">'+htmlEscape(outcomeName[r.decision])+' · '+htmlEscape(r.fictional_counterparty)+'</p>'+
    '<p>'+htmlEscape(r.rationale)+'</p><p class="condition"><strong>Context or condition:</strong> '+htmlEscape(r.conditions)+'</p>'+
    '<div class="log-links"><a href="/#review/'+encodeURIComponent(r.review_id)+'/overview">Open '+htmlEscape(reviewName[r.review_id])+' review ('+htmlEscape(r.review_id)+') →</a>'+
    (source?'<a href="'+sourceUrl+'" download>Related fixed example '+htmlEscape(source)+' (not evidence for this log entry) ↗</a>':'')+
    '</div><p class="provenance">Fictional scenario analogue only · Not a verified source-backed decision or reusable precedent.</p></article>';
}
function render(){
  const matching=matchingRows(),show=matching.slice(0,logState.visible);
  const filter=byId('case-filter').value;
  byId('log-list').innerHTML=show.map(renderRow).join('')||'<p class="log-empty">No fictional decisions match these filters.</p>';
  byId('result-count').textContent=matching.length+' matching · '+show.length+' shown';
  byId('results-title').textContent=filter==='all'?'Decision history':reviewName[filter]+' · related earlier decisions';
  byId('load-more').hidden=show.length>=matching.length;
}
async function init(){
  try{
    const response=await fetch('/demo-data/decision-log.json',{cache:'no-store'});
    if(!response.ok)throw new Error('The fictional history data is not available on this deployment.');
    const data=await response.json();
    if(data.synthetic!==true||!Array.isArray(data.records)||data.records.length!==300||data.records.some(r=>r.synthetic!==true||r.record_status!=='illustrative_unverified'))throw new Error('The expected fictional history export is missing or invalid.');
    logState.rows=data.records.slice().sort((a,b)=>b.date.localeCompare(a.date)||b.id.localeCompare(a.id));
    const totals=logState.rows.reduce((acc,r)=>(acc[r.flag]++,acc),{red:0,green:0,amber:0});
    byId('log-stats').innerHTML='<strong>'+logState.rows.length+' invented decisions</strong> · '+totals.red+' previous red flags · '+totals.green+' earlier acceptable or resolved outcomes · '+totals.amber+' context-dependent outcomes';
    for(const id of ['case-filter','flag-filter','log-search'])byId(id).addEventListener(id==='log-search'?'input':'change',()=>{logState.visible=12;render()});
    byId('load-more').addEventListener('click',()=>{logState.visible+=12;render()});
    const requested=new URLSearchParams(location.search).get('review');
    if(requested&&reviewName[requested])byId('case-filter').value=requested;
    render();
  }catch(error){byId('log-stats').textContent='Demo data unavailable';byId('log-list').textContent=error.message;byId('result-count').textContent='';}
}
init();
