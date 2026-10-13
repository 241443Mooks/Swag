import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {test} from 'node:test';
import vm from 'node:vm';

const source=readFileSync(new URL('../web/app.js',import.meta.url),'utf8').split("loadQueue().then(async()=>")[0];

function harness(items){
  const elements=new Map();
  const node=id=>{
    if(!elements.has(id))elements.set(id,{innerHTML:'',textContent:'',value:'',className:'',querySelectorAll:()=>[],querySelector:()=>null});
    return elements.get(id);
  };
  const location={hash:'#home'};
  const storage=new Map();
  const context=vm.createContext({
    document:{getElementById:node,querySelectorAll:()=>[],addEventListener:()=>{},title:''},
    location,
    sessionStorage:{getItem:key=>storage.get(key)||null,setItem:(key,value)=>storage.set(key,value)},
    window:{history:{pushState:(_state,_title,hash)=>{location.hash=hash},replaceState:(_state,_title,hash)=>{location.hash=hash}},addEventListener:()=>{}},
    fetch:async url=>({ok:true,json:async()=>url==='/api/queue'?{items}:null}),
    requestAnimationFrame:()=>{},
    setTimeout,clearTimeout,
  });
  vm.runInContext(source,context);
  return {context,node,location,storage,run:code=>vm.runInContext(code,context)};
}

const items=[
  {id:'T03',display_name:'Falcon',route:'escalate',findings_count:3,reason:'Broad rights',latest_decision:null},
  {id:'T04',display_name:'Elm',route:'escalate',findings_count:1,reason:'Missing protection',latest_decision:{decision:'escalate'}},
  {id:'T02',display_name:'Brookside',route:'review_required',findings_count:1,reason:'Changed term',latest_decision:null},
  {id:'T01',display_name:'Birchbridge',route:'routine_candidate',findings_count:0,reason:'No material change',latest_decision:null},
];

test('Home counts pending work and each category opens its filtered queue',async()=>{
  const h=harness(items);
  h.run('state.queue = '+JSON.stringify(items));
  const home=h.run('homeView()');
  assert.match(home,/data-filter="escalate"><strong>1<\/strong>/);
  assert.match(home,/data-filter="review_required"><strong>1<\/strong>/);
  assert.match(home,/data-filter="routine_candidate"><strong>1<\/strong>/);
  assert.match(home,/Start reviewing/);
  await h.run("navigate('queue','escalate')");
  assert.equal(h.location.hash,'#queue/escalate');
  assert.equal(h.node('filter').value,'escalate');
  assert.match(h.node('queue').innerHTML,/Falcon/);
  assert.doesNotMatch(h.node('queue').innerHTML,/Elm|Brookside/);
  assert.equal(h.storage.get('chugchug.queueFilter'),'escalate');
  await h.run("navigate('queue','review_required')");
  assert.match(h.node('queue').innerHTML,/Brookside/);
  assert.doesNotMatch(h.node('queue').innerHTML,/Falcon/);
  await h.run("navigate('queue','routine_candidate')");
  assert.match(h.node('queue').innerHTML,/Birchbridge/);
});

test('decision controls retain human outcomes, rationale and finding selection',()=>{
  const h=harness(items);
  const html=h.run("decisionView({analysis:{findings:[{id:'finding-1',title:'Broad rights'}]}})");
  for(const outcome of ['approve','request_amendment','reject','escalate'])assert.match(html,new RegExp(`value="${outcome}"`));
  assert.match(html,/name="reviewer" required/);
  assert.match(html,/name="rationale" required/);
  assert.match(html,/name="finding" value="finding-1"/);
  assert.match(html,/Recording a decision does not publish it as precedent/);
});

test('Start reviewing carries the next contract category back to the queue',async()=>{
  const h=harness(items);
  h.run('state.queue = '+JSON.stringify(items));
  h.run("state.page='home'; select=async id=>{globalThis.selectedId=id}");
  await h.run('startReviewing()');
  assert.equal(h.context.selectedId,'T03');
  assert.equal(h.run('state.filter'),'escalate');
  assert.equal(h.storage.get('chugchug.queueFilter'),'escalate');
});
