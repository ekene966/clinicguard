import os
import tempfile
import unittest
from unittest.mock import patch

from app import initialize_database, password_hash


class EHRDatabaseTests(unittest.TestCase):
    def test_database_seeds_roles_and_synthetic_patient(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "ehr.sqlite3")
            with patch("app.DEMO_PASSWORD", "test-password"):
                initialize_database(path)
            import sqlite3

            db = sqlite3.connect(path)
            try:
                self.assertEqual(db.execute("SELECT COUNT(*) FROM users").fetchone()[0], 3)
                self.assertEqual(db.execute("SELECT COUNT(*) FROM patients").fetchone()[0], 1)
            finally:
                db.close()

    def test_password_hash_is_salted(self):
        salt = b"0123456789abcdef"
        self.assertNotEqual(password_hash("secret", salt), password_hash("secret", b"fedcba9876543210"))
