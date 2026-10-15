import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import {test} from "node:test";
import vm from "node:vm";

const source = readFileSync(new URL("../cloudflare/worker.js", import.meta.url), "utf8")
  .replace(/import \{ DurableObject \} from "cloudflare:workers";/, "")
  .replace("export class ChugChugContainer", "class ChugChugContainer")
  .replace("export default {", "const worker = {") +
  "\nglobalThis.edge={ChugChugContainer,worker};\n";
const context = vm.createContext({
  DurableObject: class {constructor(ctx,env){this.ctx=ctx;this.env=env;}},
  URL, Request, Response, AbortSignal, Error,
  scheduler: {wait: async()=>{}},
});
vm.runInContext(source, context);
const {ChugChugContainer, worker}=context.edge;
const origin="https://chugchug-preview.smooks.co.uk";

test("Cloudflare Worker refuses unexpected hostname before reaching container",async()=>{
  let calls=0;
  const env={PUBLIC_ORIGIN:origin,CHUGCHUG_CONTAINER:{getByName:()=>{calls++; return {fetch:async()=>new Response("ok")}}}};
  const bad=await worker.fetch(new Request("https://attacker.example/api/queue"),env);
  assert.equal(bad.status,404);
  assert.equal(calls,0);
  const good=await worker.fetch(new Request(origin+"/api/queue"),env);
  assert.equal(good.status,200);
  assert.equal(calls,1);
});

test("Worker injects trustworthy public hostname and passes configured secret only to container",async()=>{
  const intercepted=[], env={PUBLIC_ORIGIN:origin,CHUGCHUG_DEMO_PASSWORD:"secret-for-test-only"};
  let started;
  const container={
    running:false,
    images:{base:"demo-image"},
    start:args=>{started=args;container.running=true},
    setInactivityTimeout:async()=>{},
    getTcpPort:()=>({fetch:async request=>{
      intercepted.push(request);
      return new Response("ok");
    }}),
  };
  const ctx={container,blockConcurrencyWhile:async callback=>callback()};
  const instance=new ChugChugContainer(ctx,env);
  const request=new Request(origin+"/demo/login",{
    method:"POST",headers:{
      "content-type":"application/x-www-form-urlencoded",
      "origin":origin,
      "x-chugchug-public-host":"attacker.example",
    },body:"password=example",
  });
  const response=await instance.fetch(request);
  assert.equal(response.status,200);
  assert.equal(started.env.CHUGCHUG_DEMO_ORIGIN,origin);
  assert.equal(started.env.CHUGCHUG_DEMO_PASSWORD,"secret-for-test-only");
  assert.equal(started.env.CHUGCHUG_CLOUDFLARE_PROXY,"1");
  assert.equal(started.enableInternet,false);
  assert.equal(intercepted.length,2);
  assert.equal(new URL(intercepted[1].url).host,"container");
  assert.equal(intercepted[1].headers.get("x-chugchug-public-host"),"chugchug-preview.smooks.co.uk");
  assert.equal(intercepted[1].headers.get("origin"),origin);
});
