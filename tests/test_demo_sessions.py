"""HTTP and lifecycle tests for isolated public-demo sessions."""
from __future__ import annotations

import http.cookiejar
import json
import os
import tempfile
import threading
import unittest
from types import SimpleNamespace
from unittest.mock import patch
import urllib.error
import urllib.parse
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

from chugchug.demo_server import (
    DemoHandler, DemoSessions, IDLE_SECONDS, LIFETIME_SECONDS,
)

ROOT = Path(__file__).resolve().parents[1]


class DemoSessionTests(unittest.TestCase):
    def test_fresh_spaces_are_isolated_and_cleaned(self):
        now = [1000.]
        with tempfile.TemporaryDirectory() as temp:
            manager = DemoSessions(ROOT, password="long-unique-demo-passcode", clock=lambda: now[0])
            first_token, first = manager.create()
            second_token, second = manager.create()
            self.assertNotEqual(first_token, second_token)
            self.assertNotEqual(first.temporary.name, second.temporary.name)
            doc = first.app.detail("T03")
            first.app.ledger.append(
                doc["document"]["sha256"], doc["document"]["filename"],
                "Visitor one", "escalate", "Synthetic review decision.", [],
                reference_sha256=doc["reference"]["sha256"],
            )
            self.assertEqual(len(first.app.detail("T03")["history"]), 1)
            self.assertEqual(len(second.app.detail("T03")["history"]), 0)
            kept_path = Path(first.temporary.name)
            manager.discard(first_token)
            self.assertFalse(kept_path.exists())
            self.assertIsNone(manager.claim(first_token))
            self.assertIsNotNone(manager.claim(second_token))
            manager.release(second)
            now[0] += IDLE_SECONDS + 1
            self.assertIsNone(manager.claim(second_token))
            self.assertFalse(Path(second.temporary.name).exists())

    def test_absolute_lifetime_and_login_rate(self):
        now = [0.]
        manager = DemoSessions(ROOT, password="demo-long-passphrase", clock=lambda: now[0])
        token, session = manager.create()
        for i in range(6):
            self.assertTrue(manager.may_try_login("example"))
            manager.failed_login("example")
        self.assertFalse(manager.may_try_login("example"))
        now[0] = 601
        self.assertTrue(manager.may_try_login("example"))
        now[0] = LIFETIME_SECONDS + 1
        self.assertIsNone(manager.claim(token))
        self.assertFalse(Path(session.temporary.name).exists())


class DemoHTTPTests(unittest.TestCase):
    def setUp(self):
        self.sessions = DemoSessions(ROOT, password="this-is-only-a-test-demo-code")
        origin = "http://127.0.0.1"
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), self._handler_class(origin))
        self.origin = origin + ":" + str(self.server.server_port)
        # The origin includes the dynamically allocated port.
        self.server.RequestHandlerClass.origin = self.origin
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.a = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        self.b = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))

    def _handler_class(self, origin):
        class TestingHandler(DemoHandler):
            pass
        TestingHandler.sessions = self.sessions
        TestingHandler.origin = origin
        TestingHandler.secure_cookies = False
        return TestingHandler

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()

    def request(self, opener, path, body=None, csrf=None, origin=None, method=None):
        raw = json.dumps(body).encode("utf-8") if isinstance(body, dict) else body
        headers = {"Origin": self.origin if origin is None else origin}
        if isinstance(body, dict):
            headers["Content-Type"] = "application/json"
        if csrf:
            headers["X-ChugChug-CSRF"] = csrf
        req = urllib.request.Request(
            self.origin + path, data=raw, headers=headers,
            method=method or ("POST" if body is not None else "GET"),
        )
        return opener.open(req)

    def get_json(self, opener, path):
        return json.load(self.request(opener, path))

    def login(self, opener):
        raw = urllib.parse.urlencode({"password": "this-is-only-a-test-demo-code"}).encode()
        response = self.request(opener, "/demo/login", raw)
        self.assertIn("ChugChug", response.read().decode())
        return self.get_json(opener, "/demo/session")

    def test_visitor_decisions_isolation_reset_and_logout(self):
        with self.assertRaises(urllib.error.HTTPError) as missing:
            self.request(self.a, "/api/queue")
        self.assertEqual(missing.exception.code, 401)
        sign_in = self.request(self.a, "/demo/login")
        self.assertIn("Enter my demo workspace", sign_in.read().decode())
        a = self.login(self.a)
        b = self.login(self.b)
        self.assertEqual(len(self.get_json(self.a, "/api/queue")["items"]), 6)
        self.assertEqual(len(self.get_json(self.b, "/api/queue")["items"]), 6)
        detail = self.get_json(self.a, "/api/contracts/T03")
        ids = [finding["id"] for finding in detail["analysis"]["findings"]]
        decision = {
            "document_id": "T03", "reviewer": "Visitor A", "decision": "escalate",
            "rationale": "This fictional provision needs further review.", "finding_ids": ids,
        }
        self.assertEqual(json.load(self.request(self.a, "/api/decisions", decision, csrf=a["csrf"]))["decision"], "escalate")
        self.assertEqual(len(self.get_json(self.a, "/api/contracts/T03")["history"]), 1)
        self.assertEqual(len(self.get_json(self.b, "/api/contracts/T03")["history"]), 0)
        self.assertEqual(
            json.load(self.request(self.a, "/demo/add-sample", {"sample_id": "retention"}, csrf=a["csrf"]))["id"][:2], "U-"
        )
        self.assertEqual(len(self.get_json(self.a, "/api/queue")["items"]), 7)
        self.assertEqual(len(self.get_json(self.b, "/api/queue")["items"]), 6)
        replacement = json.load(self.request(self.a, "/demo/reset", body=b"", csrf=a["csrf"], method="POST"))
        self.assertTrue(replacement["reset"])
        self.assertNotEqual(replacement["csrf"], a["csrf"])
        self.assertEqual(len(self.get_json(self.a, "/api/queue")["items"]), 6)
        self.assertEqual(len(self.get_json(self.a, "/api/contracts/T03")["history"]), 0)
        with self.assertRaises(urllib.error.HTTPError) as stale:
            self.request(self.a, "/api/decisions", decision, csrf=a["csrf"])
        self.assertEqual(stale.exception.code, 403)
        new = self.get_json(self.a, "/demo/session")
        self.assertEqual(new["csrf"], replacement["csrf"])
        self.assertTrue(json.load(self.request(self.a, "/demo/logout", body=b"", csrf=new["csrf"], method="POST"))["signed_out"])
        with self.assertRaises(urllib.error.HTTPError) as logged_out:
            self.request(self.a, "/demo/session")
        self.assertEqual(logged_out.exception.code, 401)

    def test_uploads_model_calls_csrf_origin_and_sample_allowlist(self):
        a = self.login(self.a)
        with self.assertRaises(urllib.error.HTTPError) as upload:
            self.request(self.a, "/api/upload", body=b"sample bytes")
        self.assertEqual(upload.exception.code, 403)
        with self.assertRaises(urllib.error.HTTPError) as model:
            self.request(self.a, "/api/ai", {"document_id": "T03"}, csrf=a["csrf"])
        self.assertEqual(model.exception.code, 403)
        with self.assertRaises(urllib.error.HTTPError) as csrf:
            self.request(self.a, "/demo/add-sample", {"sample_id": "retention"})
        self.assertEqual(csrf.exception.code, 403)
        with self.assertRaises(urllib.error.HTTPError) as other:
            self.request(self.a, "/demo/add-sample", {"sample_id": "retention"}, csrf=a["csrf"], origin="https://evil.example")
        self.assertEqual(other.exception.code, 403)
        with self.assertRaises(urllib.error.HTTPError) as sample:
            self.request(self.a, "/demo/add-sample", {"sample_id": "not-a-sample"}, csrf=a["csrf"])
        self.assertEqual(sample.exception.code, 400)

    def test_cloudflare_verified_hostname_without_weakening_direct_mode(self):
        origin = "https://chugchug-preview.smooks.co.uk"
        fake = SimpleNamespace(
            origin=origin,
            headers={
                "Origin": origin,
                "Host": "container",
                "X-ChugChug-Public-Host": "chugchug-preview.smooks.co.uk",
            },
        )
        with patch.dict(os.environ, {"CHUGCHUG_CLOUDFLARE_PROXY": "1"}):
            self.assertTrue(DemoHandler._same_origin(fake))
            fake.headers["X-ChugChug-Public-Host"] = "attacker.example"
            self.assertFalse(DemoHandler._same_origin(fake))
        fake.headers["X-ChugChug-Public-Host"] = "chugchug-preview.smooks.co.uk"
        with patch.dict(os.environ, {"CHUGCHUG_CLOUDFLARE_PROXY": ""}):
            self.assertFalse(DemoHandler._same_origin(fake))

    def test_research_material_is_authenticated_and_unassessed(self):
        with self.assertRaises(urllib.error.HTTPError) as forbidden:
            self.request(self.a, "/demo-data/research.json")
        self.assertEqual(forbidden.exception.code, 401)
        self.login(self.a)
        research = self.get_json(self.a, "/demo-data/research.json")
        self.assertEqual(len(research["references"]), 8)
        self.assertEqual(len(research["routine_clients"]), 20)
        self.assertEqual(len(research["challenge_cases"]), 4)
        self.assertIn("not verified", research["routine_clients"][0]["status"])
        docx = self.request(self.a, research["routine_clients"][0]["download"])
        self.assertEqual(docx.read(2), b"PK")


if __name__ == "__main__":
    unittest.main()
