# Cloudflare Workers + Containers deployment (interactive ChugChug)

**Status: code prepared on draft PR #24; Cloudflare account not connected; no live deployment or verified Cloudflare runtime yet.** This uses the **Workers Paid** plan, which starts at USD $5/month and includes limited compute usage. Usage above allowances is billed. Check the current Cloudflare dashboard before enabling a paid feature.

## Why not just Pages?

The current static Pages website does not run the Python server and answers /api/queue with its HTML shell. Pages Functions run on Workers rather than as a long-running Python HTTP server. The separate Cloudflare Containers service supports a real Linux/Python filesystem and Docker image.

This proposed architecture uses:
- `cloudflare/worker.js` to verify the exact public HTTPS origin, route all requests to a *single named* container and assert the public hostname to the container.
- `wrangler.jsonc` for Cloudflare Container/Durable Object bindings and one staging-origin configuration.
- `Dockerfile.demo` to package synthetic documents, the existing Python comparison service and the interactive session/login server **without** evaluator ground-truth files or local .env/private ledgers.
- `chugchug/demo_server.py` for password-controlled entry, CSRF/Origin checks and separate temporary ledgers per visitor.

The Worker passes its securely stored demo password to the container **at startup**, not into front-end JavaScript or a Docker build argument. Requests only reach ChugChug through the Worker/container binding. The container has no external Internet access, live AI calls are blocked, and arbitrary DOCX uploads are disabled.

The Worker uses one container rather than random routing: user data is currently held in temporary local files and session memory. Requests from a visitor **must** hit the same process. Cloudflare may still restart/replace the container, which immediately invalidates temporary demo sessions. Never imply durable persistence.

## Preconditions

1. Confirm the account has **Workers Paid / Containers**. The existing Pages plan alone does not imply Containers are enabled.
2. Approve source PRs in dependency order: #20 research fixture files, #22 read-only data baseline, then #24 interactive sessions, keeping #21 separate.
3. Review and configure a long random **CHUGCHUG_DEMO_PASSWORD** as a Cloudflare Worker secret, minimum 12 characters; do not commit the value or paste it into messages.
4. Create/use an *independent staging hostname* such as `chugchug-preview.smooks.co.uk` for initial testing. **This address is proposed, not currently provisioned.** Do not replace `chugchug.smooks.co.uk` until live functional and security tests pass.
5. Set `vars.PUBLIC_ORIGIN` in `wrangler.jsonc` to the exact HTTPS staging hostname; it must match the browser-visible Origin and Host. The Worker fails closed on any different hostname.

## Deploy staging (only after the owner authorises a paid deployment)

A GitHub-connected **Cloudflare Workers Builds** project can build Containers directly. Cloudflare documents a Dockerfile build in Workers Builds, using the production deploy command `npx wrangler deploy`. Unlike a Pages static deployment, this builds and publishes the Worker and Docker image together.

Alternatively, from a workstation with Docker running and Node/Wrangler installed:

```sh
npx wrangler login
npx wrangler secret put CHUGCHUG_DEMO_PASSWORD
npx wrangler deploy
```

Both approaches require a Workers Paid account. For initial login tests on the staging hostname, configure a Cloudflare **Worker Custom Domain** for the staging hostname, and verify its associated DNS. The Worker code checks the configured hostname and intentionally refuses all other domains including workers.dev aliases.

Do **not** put the password in the `wrangler.jsonc` vars object, GitHub Actions secrets visible to builds, or image build arguments. The Cloudflare Worker secret must exist in the same account/environment as the Worker.

If using Workers Builds, create a separate staging Worker/deployment; preview branch uploads do **not** necessarily rebuild or deploy Containers. Cloudflare docs explicitly recommend a dedicated staging environment/Worker for testing container changes, not deploying unreviewed feature branches over a live application.

## Test before switching the original domain

- Staging login page and access-code form work over HTTPS, including CSRF and exact-origin protection on POST.
- Fresh browser A and independent browser B start with the same six *fictional* cases but with **zero shared review events**.
- Review, decision, publication/withdrawal and correction/lesson reuse are visible **only inside the originating session**.
- Add one of the three safe fictional learning documents to A and verify B still has six contracts. Reset A and confirm a clean six-contract queue; sign out and ensure its cookie no longer works.
- Check source-linked evidence, original DOCX downloads and the 8+20+4 browse-only research library; no supposed automated multi-family legal match.
- Ensure `/api/queue` and research originals require a valid session. Cross-origin forged writes, POST without CSRF, arbitrary DOCX and live AI requests must fail.
- Test mobile and desktop layouts, high/low traffic and container wake-up after inactivity. A container restart may lose sessions; its initial loading UX needs review.
- Confirm Cloudflare bills/usage after the test. The basic container size has 1 GiB memory and 4 GB disk, and Cloudflare charges for its active runtime; adjust only after capacity measurements.

After owner acceptance, remove `chugchug.smooks.co.uk` from the old Pages project's custom domains (keeping its pages.dev rollback URL) before binding the new Worker to that same hostname. Update PUBLIC_ORIGIN to `https://chugchug.smooks.co.uk` and redeploy; rotate or confirm the demo secret in that environment. Roll back to the original Pages custom domain if needed.

**Do not** make the Python backend publicly reachable without the Worker/proxy. The server trusts a Worker-set header only when `CHUGCHUG_CLOUDFLARE_PROXY=1`, which is intentionally set by the controlled Worker. Direct public access bypasses that trust boundary.

## Documentation consulted (13 October 2026)

- https://developers.cloudflare.com/containers/
- https://developers.cloudflare.com/containers/configuration/wrangler/
- https://developers.cloudflare.com/containers/examples/env-vars-and-secrets/
- https://developers.cloudflare.com/containers/guides/deploy/
- https://developers.cloudflare.com/containers/platform/pricing/
- https://developers.cloudflare.com/pages/configuration/custom-domains/
