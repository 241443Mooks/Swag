// Cloudflare Workers -> one stateful, synthetic-only ChugChug Container.
// All requests pass through the Python demo login/session gate. Do not
// split the API across random instances: sessions live in the container.
import { DurableObject } from "cloudflare:workers";

const PORT = 8772;
const INACTIVITY_MS = 70 * 60 * 1000; // longer than Python's 60-min visitor idle expiry
const INSTANCE = "single-temporary-demo";
const READY_TRIES = 100;

export class ChugChugContainer extends DurableObject {
  starting = undefined;

  constructor(ctx, env) {
    super(ctx, env);
    if (ctx.container?.running) {
      void ctx.blockConcurrencyWhile(() => ctx.container.setInactivityTimeout(INACTIVITY_MS));
    }
  }

  async ready() {
    const container = this.ctx.container;
    if (!container) throw new Error("Cloudflare Container binding is unavailable");
    if (!container.running) {
      if (!this.env.CHUGCHUG_DEMO_PASSWORD || !this.env.PUBLIC_ORIGIN) {
        throw new Error("Set the demo password secret and HTTPS public origin before starting");
      }
      container.start({
        image: container.images.base,
        instance: "basic",
        enableInternet: false,
        env: {
          CHUGCHUG_DEMO_PASSWORD: this.env.CHUGCHUG_DEMO_PASSWORD,
          CHUGCHUG_DEMO_ORIGIN: this.env.PUBLIC_ORIGIN,
          CHUGCHUG_CLOUDFLARE_PROXY: "1",
        },
      });
    }
    await container.setInactivityTimeout(INACTIVITY_MS);
    const port = container.getTcpPort(PORT);
    let lastError;
    for (let i = 0; i < READY_TRIES; i++) {
      try {
        const response = await port.fetch("http://container/healthz", {
          signal: AbortSignal.timeout(1000),
        });
        await response.body?.cancel();
        if (response.ok) return;
        lastError = new Error("Unexpected health status");
      } catch (error) {
        lastError = error;
      }
      await scheduler.wait(200);
    }
    throw new Error("ChugChug container did not become healthy", { cause: lastError });
  }

  async fetch(request) {
    this.starting ??= this.ready().finally(() => { this.starting = undefined; });
    await this.starting;

    const original = new URL(request.url);
    const target = new URL(request.url);
    target.protocol = "http:";
    target.host = "container";
    const forwarded = new Request(target, request);
    forwarded.headers.delete("host");
    // Discard any visitor-provided value: only the Worker asserts public host.
    forwarded.headers.delete("x-chugchug-public-host");
    forwarded.headers.set("x-chugchug-public-host", original.host);
    return this.ctx.container.getTcpPort(PORT).fetch(forwarded);
  }
}

export default {
  async fetch(request, env) {
    // This is an app deployment with a deliberate, single HTTPS hostname.
    // Do not allow arbitrary *.workers.dev or other host aliases to share a
    // cookie/session origin with the custom hostname.
    if (!env.PUBLIC_ORIGIN || new URL(request.url).origin !== env.PUBLIC_ORIGIN) {
      return new Response("Demo hostname not configured", {
        status: 404,
        headers: { "Cache-Control": "no-store" },
      });
    }
    return env.CHUGCHUG_CONTAINER.getByName(INSTANCE).fetch(request);
  },
};
