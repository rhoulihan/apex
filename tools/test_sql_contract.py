"""Text-level contract tests for helpdesk-schema.sql (DB execution is a manual gate).
Run: python3 test_sql_contract.py -v
"""
import re
import unittest
from pathlib import Path

SQL_PATH = Path(__file__).resolve().parent.parent / "ai-helpdesk-agent/2-data-model-ai/files/helpdesk-schema.sql"


class TestSchemaScript(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sql = SQL_PATH.read_text(encoding="utf-8")
        cls.low = cls.sql.lower()

    def test_drop_and_recreate_semantics(self):
        for t in ("tickets", "kb_articles", "team_members"):
            self.assertIn(f"create table {t}", self.low, t)
        # state-reset: a drop loop over all three tables
        self.assertIn("drop table", self.low)
        for t in ("'TICKETS'", "'KB_ARTICLES'", "'TEAM_MEMBERS'"):
            self.assertIn(t, self.sql)

    def test_fixed_rows_present(self):
        self.assertRegex(self.sql, r"insert into tickets[^;]*\(42,[^;]*error 812", "ticket 42 VPN row")
        self.assertRegex(self.sql, r"insert into kb_articles[^;]*VPN Error 812")

    def test_seed_counts(self):
        self.assertEqual(len(re.findall(r"insert into tickets", self.sql, re.I)), 50)
        self.assertEqual(len(re.findall(r"insert into kb_articles", self.sql, re.I)), 30)
        self.assertEqual(len(re.findall(r"insert into team_members", self.sql, re.I)), 8)

    def test_identity_start_1000(self):
        self.assertEqual(self.low.count("identity (start with 1000"), 3)

    def test_ticket_42_is_open_high_network(self):
        m = re.search(r"insert into tickets[^;]*\(42,.*?;", self.sql, re.S)
        self.assertIsNotNone(m)
        row = m.group(0)
        for v in ("'Open'", "'High'", "'Network'"):
            self.assertIn(v, row)

    def test_no_real_domains(self):
        self.assertNotIn("@oracle.com", self.low)
        self.assertIn("@example.com", self.low)

    def test_commit_present(self):
        self.assertIn("commit;", self.low)


if __name__ == "__main__":
    unittest.main()
