# Interactive visitor demo (synthetic only)

This optional mode gives each visitor a fresh, private-to-their-session instance of the existing working review engine. The existing loopback development server and public **read-only** static snapshot are unchanged.

This is a **demo-access gate and temporary isolation**, not user accounts, a production identity system or a service suitable for confidential agreements.

## Visitor journey

1. Visit the HTTPS demo address, enter the shared access code, and start with six fictional reviewed mutual NDA cases.
2. Review original and reference passages, record a fictional human decision, explicitly publish or withdraw a demo precedent, and use the correction → share → reuse/withdraw workflow.
3. Select a bundled learning sample to add a new fictional contract. Choose from Maple Metrics (retention), Harbour Analytics (analytics), or Regulatory Records (restricted archive).
4. Open Reference to browse eight unapproved standard specimens, 20 ordinary-looking client examples and four challenge documents. They are research assets, **not** analysed or approved by the current NDA engine.
5. Choose **Reset my demo** to throw away your decisions, sample uploads, corrections, reference selection and publication events. **Sign out** to delete the visitor's state.

Each **new sign-in** starts from a clean workspace. Refreshing the page keeps your current workspace while the session is alive. Other browsers have separate spaces; tabs within the same browser normally share the same session cookie (and therefore share one workspace). Sessions expire after 60 minutes without activity or a hard maximum of four hours. State is held only on the single running server and is removed on reset, sign-out or expiry cleanup; restarting the process also invalidates sessions.

**Limits:** at most 32 live workspaces and 80 write actions per workspace. This is an intentional demonstration guardrail, not production capacity planning. Idle expiry cleanup is opportunistic (triggered on later session activity); transient files can remain until a request causes cleanup or the process exits. State may temporarily occupy the host filesystem under its temp directory. Do not submit real documents, real reviewer identities or sensitive information.

## Security boundary

- Session cookie uses a cryptographically random bearer token, HttpOnly, SameSite=Strict and Secure on HTTPS, with a __Host- prefix. The server stores a SHA-256 digest of the token, not the token.
- POSTs require an exact configured Origin/Host match and a per-session CSRF header. Any new login invalidates the previous workspace for that browser. Password guesses are rate-limited per connecting IP.
- Every request for queue, contract, historical source, research specimen and static application files is session-gated. Visitors cannot inspect one another's review events.
- Local Python demo state, references, uploaded *bundled* learning samples, decisions and corrections are separate per visitor. The server accepts **no arbitrary DOCX upload** and blocks live AI calls outright.
- The container explicitly omits the held-out answer key, adversarial evaluator material, secret files and local workspace state.
- TLS termination, reverse proxy limits, access logging, infrastructure security, resource quotas, backups (not needed for ephemeral data), availability and abuse protection remain **deployment responsibilities**. This is not a production security certification.

The access code is a shared entry passphrase. Anyone who knows it can create their own temporary session. It is not proof of personal identity; for a private invited audience, distribute it privately and rotate it when appropriate. An external identity/access gateway can replace the shared passphrase later.

## Running locally

Requires Python 3.9+. No third-party Python dependencies.

    CHUGCHUG_DEMO_PASSWORD='use-a-different-long-secret' \
      python3 -m chugchug.demo_server --port 8772 --local-http

Open http://127.0.0.1:8772. This flag is for localhost only and cannot be combined with container binding. The ordinary local development server remains:

    python3 -m chugchug.server --port 8771

## Public deployment through HTTPS

The current static web hosting arrangement alone **cannot run interactive sessions**. The domain must point to, or reverse-proxy to, a continuously running single-process Python app. Do not simply expose the existing unauthenticated local server.

An example Docker deployment on a server with an HTTPS reverse proxy:

1. Create a **private, root-readable** environment file, outside the repository, such as /etc/chugchug/demo.env:

       CHUGCHUG_DEMO_PASSWORD=<long-random-secret>
       CHUGCHUG_DEMO_ORIGIN=https://chugchug.smooks.co.uk

   Replace the placeholder locally. Never paste the secret in a GitHub issue, commit, CI log or chat.

2. Build from the reviewed branch/commit after all dependent PRs are approved:

       docker build -f Dockerfile.demo -t chugchug-demo:reviewed .

3. Start **one worker/container** with no persistent state volume and a read-only filesystem; only the HOST loopback port is published:

       docker run -d --name chugchug-demo --restart unless-stopped \
         --env-file /etc/chugchug/demo.env \
         --read-only --tmpfs /tmp:rw,nosuid,nodev,size=256m,mode=1777 \
         --memory=1g --cpus=1 --pids-limit=128 \
         -p 127.0.0.1:8772:8772 chugchug-demo:reviewed

4. Point the HTTPS virtual host to **127.0.0.1:8772**. For example, with Caddy on the same host:

       chugchug.smooks.co.uk {
           reverse_proxy 127.0.0.1:8772
       }

   Ensure your reverse proxy preserves the public Host header and forwards TLS HTTPS requests; the app intentionally checks that login and write requests came from CHUGCHUG_DEMO_ORIGIN. Configure upstream request size and rate limits. Do not set an unsanitised X-Forwarded-For as the trusted client identity.

5. Stop serving the old public static copy as an independently accessible route. In particular, do not leave /demo-data, /api, /originals, or a second legacy host bypassing the login and proxy.

If the current hosting platform is static-only, choose a suitable Python/container application host or a server that supports this reverse proxy. **Do not publish this feature until the owner confirms the target hosting setup and authorises the deployment.**

The service binds loopback by default. The explicit --container-bind flag changes the binding to 0.0.0.0 **inside the container only**; the docker -p line above must continue to publish the HOST port on 127.0.0.1. A different publish configuration may expose the app without the intended proxy.

## Verification checklist

Run on a clean checkout:

    python3 -m unittest discover -s tests -p 'test_*.py'
    node --check web/app.js
    node --test tests/test_web_ui.mjs
    python3 -m tests.adversarial_audit

Then confirm these behaviours against the live HTTPS hostname:

- An unauthenticated request for /api/queue returns 401, not a queue or fallback HTML; unauthenticated references and original files are also unavailable.
- One demo login opens six NDA scenarios; the browser shows **Your private demo workspace**.
- Record a decision in visitor A, then sign in through an independent private window as visitor B. B still has an untouched review.
- Add Maple Metrics via sample picker. This adds a seventh entry for A, not B. Practise decisions, corrections, publishing and withdrawal, then reset A and verify six pristine entries return.
- Logout and attempt to reuse the old cookie and CSRF token: the session must be rejected.
- Try a POST from an incorrect Origin and a POST without CSRF: both fail; arbitrary document upload and AI endpoint are blocked.
- The research catalogue shows 8 + 20 + 4 unassessed fictional specimens. Do not describe them as the same thing as a tested contract-matching workflow.
- Check desktop and narrow mobile layouts, and verify session expiry, HTTPS, cookie attributes and no console errors.

## What is intentionally not supplied by this feature

This work does **not** add new supported agreement families, verified matching of the twenty client contracts, autonomous review/approval, real employer integrations, production RBAC, a persistent user database, real-document intake, live AI model calls or a security penetration test. Issue #21 is the separate track for proposed reference applicability and source-linked comparison of additional supported families.

Source: chugchug/demo_server.py, tests/test_demo_sessions.py, web/app.js and the existing review engine.
