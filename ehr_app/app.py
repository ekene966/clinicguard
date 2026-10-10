#!/usr/bin/env python3
"""Small authenticated synthetic EHR service for the ClinicGuard lab."""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets
import sqlite3
import threading
import time
from contextlib import contextmanager
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs


DB_PATH = os.environ.get("EHR_DB_PATH", "/var/lib/clinicguard/ehr.sqlite3")
DEMO_PASSWORD = os.environ.get("EHR_DEMO_PASSWORD", "clinicguard-demo")
SESSION_TTL = 3600
SESSIONS: dict[str, tuple[str, str, float]] = {}
SESSION_LOCK = threading.Lock()


@contextmanager
def database(path: str = DB_PATH):
    db = sqlite3.connect(path)
    try:
        yield db
        db.commit()
    finally:
        db.close()


def password_hash(password: str, salt: bytes) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 120_000).hex()


def initialize_database(path: str = DB_PATH) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with database(path) as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                role TEXT NOT NULL CHECK (role IN ('admin', 'doctor', 'nurse')),
                salt BLOB NOT NULL,
                password_hash TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                birth_year INTEGER NOT NULL,
                summary TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS audit_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                action TEXT NOT NULL,
                resource TEXT NOT NULL,
                created_at INTEGER NOT NULL
            );
            """
        )
        users = [("admin", "admin"), ("doctor", "doctor"), ("nurse", "nurse")]
        for username, role in users:
            salt = secrets.token_bytes(16)
            db.execute(
                "INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?)",
                (username, role, salt, password_hash(DEMO_PASSWORD, salt)),
            )
        if not db.execute("SELECT 1 FROM patients LIMIT 1").fetchone():
            db.execute(
                "INSERT INTO patients (name, birth_year, summary) VALUES (?, ?, ?)",
                ("Synthetic Patient", 1985, "Synthetic record for security testing."),
            )


def authenticate(username: str, password: str) -> tuple[str, str] | None:
    with database() as db:
        row = db.execute(
            "SELECT username, role, salt, password_hash FROM users WHERE username = ?",
            (username,),
        ).fetchone()
    if row is None:
        return None
    if not hmac.compare_digest(password_hash(password, row[2]), row[3]):
        return None
    return row[0], row[1]


def audit(username: str, action: str, resource: str) -> None:
    with database() as db:
        db.execute(
            "INSERT INTO audit_events (username, action, resource, created_at) VALUES (?, ?, ?, ?)",
            (username, action, resource, int(time.time())),
        )


class EHRHandler(BaseHTTPRequestHandler):
    server_version = "ClinicGuard-EHR/0.3"

    def send_json(self, status: HTTPStatus, payload: dict, cookie: str | None = None) -> None:
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        if cookie:
            self.send_header("Set-Cookie", cookie)
        self.end_headers()
        self.wfile.write(body)

    def read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        return json.loads(self.rfile.read(length) or b"{}")

    def session(self) -> tuple[str, str] | None:
        token = self.headers.get("Cookie", "").removeprefix("clinicguard_session=")
        with SESSION_LOCK:
            current = SESSIONS.get(token)
        if not token or current is None or current[2] <= time.time():
            return None
        return current[0], current[1]

    def require_role(self, roles: set[str]) -> tuple[str, str] | None:
        current = self.session()
        if current is None:
            self.send_json(HTTPStatus.UNAUTHORIZED, {"error": "authentication required"})
            return None
        if current[1] not in roles:
            self.send_json(HTTPStatus.FORBIDDEN, {"error": "insufficient role"})
            return None
        return current

    def do_GET(self) -> None:
        if self.path == "/healthz":
            self.send_json(HTTPStatus.OK, {"status": "ok"})
            return
        if self.path == "/":
            self.send_json(HTTPStatus.OK, {"service": "ClinicGuard synthetic EHR", "version": "0.3.0"})
            return
        if self.path == "/api/patients":
            current = self.require_role({"admin", "doctor", "nurse"})
            if current is None:
                return
            with database() as db:
                rows = db.execute("SELECT id, name, birth_year, summary FROM patients").fetchall()
            audit(current[0], "read", "patients")
            self.send_json(
                HTTPStatus.OK,
                {"patients": [dict(zip(("id", "name", "birth_year", "summary"), row)) for row in rows]},
            )
            return
        if self.path == "/api/audit":
            current = self.require_role({"admin"})
            if current is None:
                return
            with database() as db:
                rows = db.execute(
                    "SELECT username, action, resource, created_at FROM audit_events ORDER BY id DESC LIMIT 100"
                ).fetchall()
            self.send_json(HTTPStatus.OK, {"events": [dict(zip(("username", "action", "resource", "created_at"), row)) for row in rows]})
            return
        self.send_json(HTTPStatus.NOT_FOUND, {"error": "not found"})

    def do_POST(self) -> None:
        if self.path != "/api/login":
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "not found"})
            return
        try:
            body = self.read_json()
            identity = authenticate(str(body.get("username", "")), str(body.get("password", "")))
        except (ValueError, json.JSONDecodeError):
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": "invalid JSON"})
            return
        if identity is None:
            self.send_json(HTTPStatus.UNAUTHORIZED, {"error": "invalid credentials"})
            return
        token = secrets.token_urlsafe(32)
        with SESSION_LOCK:
            SESSIONS[token] = (identity[0], identity[1], time.time() + SESSION_TTL)
        audit(identity[0], "login", "session")
        self.send_json(
            HTTPStatus.OK,
            {"username": identity[0], "role": identity[1], "expires_in": SESSION_TTL},
            f"clinicguard_session={token}; HttpOnly; Secure; SameSite=Strict; Max-Age={SESSION_TTL}",
        )


def main() -> None:
    initialize_database()
    ThreadingHTTPServer(("10.10.30.11", 8080), EHRHandler).serve_forever()


if __name__ == "__main__":
    main()
