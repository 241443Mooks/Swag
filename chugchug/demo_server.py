"""Opt-in, isolated, ephemeral interactive demo for the *synthetic* ChugChug library.

Run behind a TLS reverse proxy on loopback, never directly on the public interface.
Every demo sign-in gets a fresh App, temporary state, decisions and corrections.
This is not a multi-tenant legal service or a place to upload confidential files.
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import html
import json
import os
import re
import secrets
import tempfile
import threading
import time
from dataclasses import dataclass, field
from http.cookies import CookieError, SimpleCookie
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse, unquote

from .server import App, Handler

ROOT = Path(__file__).resolve().parent.parent
SAMPLES = {
    "retention": ("dataset/learning/L01-audit-retention.docx", "Maple Metrics — audit retention"),
    "analytics": ("dataset/learning/L02-analytics-retention.docx", "Harbour Analytics — commercial analytics"),
    "regulatory": ("dataset/learning/L03-regulatory-records.docx", "Regulatory Records — restricted archive"),
}
IDLE_SECONDS = 60 * 60
LIFETIME_SECONDS = 4 * 60 * 60
MAX_SESSIONS = 32
MAX_WRITES = 80
COOKIE_PROD = "__Host-chugchug-demo"
COOKIE_LOCAL = "chugchug_demo_local"


@dataclass
class DemoSession:
    app: App
    temporary: tempfile.TemporaryDirectory
    csrf: str
    created: float
    touched: float
    active: int = 0
    retired: bool = False
    writes: int = 0
    request_lock: threading.RLock = field(default_factory=threading.RLock)


class DemoSessions:
    """In-process single-worker session store; no shared state across browsers."""

    def __init__(self, root: Path = ROOT, password: str = "", *, clock=time.monotonic):
        if len(password) < 12:
            raise ValueError("Set CHUGCHUG_DEMO_PASSWORD to a non-trivial secret (12+ characters)")
        self.root = root
        self.password = password
        self.clock = clock
        self.lock = threading.RLock()
        self.entries: dict[str, DemoSession] = {}
        self.failures: dict[str, list[float]] = {}

    def authenticated(self, value: str) -> bool:
        return hmac.compare_digest(value.encode("utf-8"), self.password.encode("utf-8"))

    def may_try_login(self, address: str) -> bool:
        with self.lock:
            now = self.clock()
            recent = [value for value in self.failures.get(address, []) if now - value < 600]
            self.failures[address] = recent
            return len(recent) < 6

    def failed_login(self, address: str) -> None:
        with self.lock:
            self.failures.setdefault(address, []).append(self.clock())

    def _retire(self, key: str) -> None:
        entry = self.entries.pop(key, None)
        if entry:
            entry.retired = True
            if entry.active == 0:
                entry.temporary.cleanup()

    def _prune(self) -> None:
        now = self.clock()
        for key, session in list(self.entries.items()):
            if now - session.touched > IDLE_SECONDS or now - session.created > LIFETIME_SECONDS:
                self._retire(key)
        for address, attempts in list(self.failures.items()):
            newer = [value for value in attempts if now - value < 600]
            if newer:
                self.failures[address] = newer
            else:
                self.failures.pop(address, None)

    def create(self) -> tuple[str, DemoSession]:
        with self.lock:
            self._prune()
            if len(self.entries) >= MAX_SESSIONS:
                raise ValueError("All demonstration spaces are in use")
            temporary = tempfile.TemporaryDirectory(prefix="chugchug-visitor-")
            try:
                app = App(self.root, Path(temporary.name))
            except Exception:
                temporary.cleanup()
                raise
            token = secrets.token_urlsafe(32)
            session = DemoSession(
                app=app, temporary=temporary, csrf=secrets.token_urlsafe(32),
                created=self.clock(), touched=self.clock(),
            )
            self.entries[hashlib.sha256(token.encode("ascii")).hexdigest()] = session
            return token, session

    def claim(self, token: str | None) -> DemoSession | None:
        if not token or len(token) > 256:
            return None
        key = hashlib.sha256(token.encode("utf-8")).hexdigest()
        with self.lock:
            self._prune()
            session = self.entries.get(key)
            if session:
                session.touched = self.clock()
                session.active += 1
            return session

    def release(self, session: DemoSession) -> None:
        with self.lock:
            session.active -= 1
            if session.retired and session.active == 0:
                session.temporary.cleanup()

    def discard(self, token: str | None) -> None:
        if token:
            with self.lock:
                self._retire(hashlib.sha256(token.encode("utf-8")).hexdigest())


class DemoHandler(Handler):
    """Protect every API, original, and HTML path with a per-visitor session."""

    sessions: DemoSessions
    origin: str
    secure_cookies: bool = True

    @property
    def cookie_name(self):
        return COOKIE_PROD if self.secure_cookies else COOKIE_LOCAL

    def send_response(self, code, message=None):
        super().send_response(code, message)
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'")
        if self.secure_cookies:
            self.send_header("Strict-Transport-Security", "max-age=31536000")

    def _cookie_token(self) -> str | None:
        try:
            cookies = SimpleCookie()
            cookies.load(self.headers.get("Cookie", ""))
            entry = cookies.get(self.cookie_name)
            return entry.value if entry else None
        except CookieError:
            return None

    def _session_cookie(self, token: str | None):
        flags = "; Path=/; HttpOnly; SameSite=Strict"
        if self.secure_cookies:
            flags += "; Secure"
        if token is None:
            return self.cookie_name + "=; Max-Age=0" + flags
        return self.cookie_name + "=" + token + flags

    def _redirect(self, path: str, token: str | None = None, set_cookie: bool = False):
        self.send_response(303)
        self.send_header("Location", path)
        if set_cookie:
            self.send_header("Set-Cookie", self._session_cookie(token))
        self.send_header("Content-Length", "0")
        self.end_headers()

    def _login_page(self, warning: str = "", status: int = 200):
        content = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ChugChug · Private demonstration</title>
<style>
:root{font-family:system-ui,sans-serif;color:#233044;background:#f7f7f5}
body{min-height:100vh;margin:0;display:grid;place-items:center}
main{width:min(92vw,410px);padding:2.25rem;background:white;border:1px solid #dae0e6;border-radius:16px;box-shadow:0 12px 32px #27374712}
h1{font-size:1.9rem;margin:.1rem 0 1rem}p{line-height:1.55;color:#49586c}
label{display:block;margin:1.4rem 0 .5rem;font-weight:600}
input{box-sizing:border-box;width:100%;padding:.8rem;border:1px solid #91a0b2;border-radius:8px;font-size:1rem}
button{width:100%;padding:.9rem;background:#213a5f;color:white;border:0;border-radius:8px;font-size:1rem;margin-top:1rem;cursor:pointer}
small{display:block;margin-top:1.2rem;color:#536273;line-height:1.55}
.notice{color:#9f2c24}
</style></head><body><main><h1>ChugChug</h1><p>Explore a fictional legal team's contract review process. Every visit gets an independent workspace, with its own decisions and corrections.</p>
""" + ('<p class="notice" role="alert">' + html.escape(warning) + '</p>' if warning else '') + """
<form method="post" action="/demo/login"><label for="code">Demo access code</label>
<input id="code" type="password" name="password" autocomplete="off" required maxlength="256">
<button type="submit">Enter my demo workspace</button></form>
<small>Only fictional documents. Activity is temporary and resets after an hour of inactivity (four hours maximum), or when you choose Reset. This demonstration is not a secure place for real contracts or personal information.</small>
</main></body></html>"""
        body = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _same_origin(self) -> bool:
        # Cloudflare Containers forward traffic internally as Host: container.
        # Trust the public-host value ONLY when running behind our single
        # Cloudflare Worker, which verifies the hostname and overwrites this
        # request header before forwarding. The container must not be reachable
        # directly from the public Internet.
        forwarded = (
            self.headers.get("X-ChugChug-Public-Host")
            if os.getenv("CHUGCHUG_CLOUDFLARE_PROXY") == "1"
            else None
        )
        host = forwarded or self.headers.get("Host")
        return (
            self.headers.get("Origin") == self.origin
            and host == urlparse(self.origin).netloc
        )

    def _with_session(self, operation, *, write=False):
        token = self._cookie_token()
        session = self.sessions.claim(token)
        if not session:
            return self._error(401, "Demo session expired. Return to the login page to start afresh.")
        try:
            if write:
                if not self._same_origin():
                    return self._error(403, "Untrusted origin")
                if not hmac.compare_digest(self.headers.get("X-ChugChug-CSRF", ""), session.csrf):
                    return self._error(403, "Invalid demo session request")
                with self.sessions.lock:
                    if session.writes >= MAX_WRITES:
                        return self._error(429, "This demo has reached its write limit. Reset to start again.")
                    session.writes += 1
            with session.request_lock:
                self.app = session.app  # Per-request instance; never mutate Handler.app globally.
                return operation(session, token)
        finally:
            self.sessions.release(session)

    def do_GET(self):
        path = unquote(urlparse(self.path).path)
        if path == "/healthz":
            return self._json({"status": "ok"})
        if path == "/demo/login":
            return self._login_page()
        if path == "/" or path == "/index.html":
            if not self._cookie_token():
                return self._login_page()
            session = self.sessions.claim(self._cookie_token())
            if not session:
                return self._login_page("Your session expired. Enter the access code for a fresh workspace.")
            try:
                self.app = session.app
                return super().do_GET()
            finally:
                self.sessions.release(session)
        return self._with_session(lambda session, token: self._authenticated_get(path, session))

    def _authenticated_get(self, path: str, session: DemoSession):
        if path == "/demo/session":
            return self._json({
                "active": True, "csrf": session.csrf, "temporary": True,
                "idle_minutes": IDLE_SECONDS // 60, "lifetime_hours": LIFETIME_SECONDS // 3600,
                "samples": [{"id": key, "name": value[1]} for key, value in SAMPLES.items()],
            })
        if path == "/demo-data/research.json" or re.fullmatch(r"/demo-data/originals/research/[A-Za-z0-9_-]+\.docx", path):
            target = (ROOT / "web" / path.lstrip("/")).resolve()
            subtree = (ROOT / "web" / "demo-data").resolve()
            if not target.is_relative_to(subtree) or not target.is_file():
                return self._error(404, "Demo specimen not available")
            if path.endswith(".json"):
                return self._json(json.loads(target.read_text(encoding="utf-8")))
            data = target.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            self.send_header("Content-Disposition", 'attachment; filename="fictional-specimen.docx"')
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            return self.wfile.write(data)
        return super().do_GET()

    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/demo/login":
            if not self._same_origin():
                return self._error(403, "Untrusted login origin")
            address = self.client_address[0]
            if not self.sessions.may_try_login(address):
                return self._login_page("Too many attempts. Try again later.", 429)
            try:
                params = parse_qs(self._body(4096).decode("utf-8"), strict_parsing=True)
                password = params.get("password", [""])[0]
            except (ValueError, UnicodeDecodeError):
                return self._login_page("Enter a valid access code.", 400)
            if not self.sessions.authenticated(password):
                self.sessions.failed_login(address)
                return self._login_page("That access code isn't recognised.", 403)
            self.sessions.discard(self._cookie_token())  # Every fresh login is a clean room.
            try:
                token, _ = self.sessions.create()
            except ValueError:
                return self._login_page("All demonstration spaces are currently in use.", 503)
            return self._redirect("/", token, set_cookie=True)

        # Never accept arbitrary DOCX uploads or third-party model calls on the public demo.
        if path in ("/api/upload", "/api/reference/upload", "/api/ai"):
            return self._error(403, "Public demo accepts only its bundled fictional samples; no arbitrary uploads or model calls")
        return self._with_session(lambda session, token: self._authenticated_post(path, session, token), write=True)

    def _authenticated_post(self, path, session, token):
        if path == "/demo/logout":
            self.sessions.discard(token)
            self.send_response(200)
            self.send_header("Set-Cookie", self._session_cookie(None))
            self.send_header("Content-Type", "application/json")
            body = b'{"signed_out":true}'
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            return self.wfile.write(body)
        if path == "/demo/reset":
            self.sessions.discard(token)
            try:
                replacement_token, replacement = self.sessions.create()
            except ValueError:
                return self._error(503, "Could not create a fresh demonstration")
            self.send_response(200)
            self.send_header("Set-Cookie", self._session_cookie(replacement_token))
            body = json.dumps({"reset": True, "csrf": replacement.csrf}).encode()
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            return self.wfile.write(body)
        if path == "/demo/add-sample":
            try:
                body = json.loads(self._body(4096))
                sample_id = body.get("sample_id") if isinstance(body, dict) else None
                if sample_id not in SAMPLES:
                    raise ValueError("Choose a listed fictional sample")
                path = ROOT / SAMPLES[sample_id][0]
                document_id = session.app.upload(path.read_bytes(), path.name)
                return self._json({"id": document_id}, 201)
            except (ValueError, UnicodeDecodeError, json.JSONDecodeError) as exc:
                return self._error(400, str(exc))
        return super().do_POST()


def main():
    parser = argparse.ArgumentParser(description="Ephemeral interactive ChugChug demonstration")
    parser.add_argument("--port", type=int, default=8772)
    parser.add_argument("--origin", default=os.getenv("CHUGCHUG_DEMO_ORIGIN", ""))
    parser.add_argument("--local-http", action="store_true", help="Only for local browser testing, not public deployment")
    parser.add_argument("--container-bind", action="store_true", help="Bind inside a container only; host port must remain loopback-only")
    args = parser.parse_args()
    password = os.getenv("CHUGCHUG_DEMO_PASSWORD", "")
    sessions = DemoSessions(password=password)
    if not args.origin:
        if args.local_http:
            args.origin = "http://127.0.0.1:" + str(args.port)
        else:
            parser.error("Set --origin https://your-demo-domain (or CHUGCHUG_DEMO_ORIGIN)")
    parsed = urlparse(args.origin)
    if parsed.path not in ("", "/") or parsed.query or parsed.fragment or not parsed.netloc:
        parser.error("Origin must be a scheme and host only")
    if args.container_bind and args.local_http:
        parser.error("Container binding requires the HTTPS reverse-proxy configuration")
    if args.local_http:
        if args.origin != "http://127.0.0.1:" + str(args.port):
            parser.error("--local-http is only for the loopback origin")
    elif parsed.scheme != "https":
        parser.error("The public demo requires an HTTPS origin and TLS reverse proxy")

    class ConfiguredHandler(DemoHandler):
        pass

    ConfiguredHandler.sessions = sessions
    ConfiguredHandler.origin = args.origin.rstrip("/")
    ConfiguredHandler.secure_cookies = not args.local_http
    # Only use 0.0.0.0 inside a container with the published HOST port restricted
    # to 127.0.0.1 and an HTTPS reverse proxy in front.
    bind_address = "0.0.0.0" if args.container_bind else "127.0.0.1"
    server = ThreadingHTTPServer((bind_address, args.port), ConfiguredHandler)
    print("ChugChug interactive demo listening on loopback port " + str(args.port), flush=True)
    try:
        server.serve_forever()
    finally:
        server.server_close()
        with sessions.lock:
            for token in list(sessions.entries):
                sessions._retire(token)


if __name__ == "__main__":
    main()
