import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "src" / "nova_marketing" / "run_analysis.py"


class PipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(SCRIPT)], check=True, capture_output=True, text=True)

    def test_summary_exists_and_is_synthetic(self):
        summary_path = ROOT / "data" / "processed" / "kpi_summary.json"
        self.assertTrue(summary_path.exists())
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        self.assertEqual(summary["data_type"], "synthetic")

    def test_completed_orders_positive(self):
        summary = json.loads((ROOT / "data" / "processed" / "kpi_summary.json").read_text(encoding="utf-8"))
        self.assertGreater(summary["completed_orders"], 0)

    def test_campaign_output_exists(self):
        self.assertTrue((ROOT / "data" / "processed" / "campaign_kpis.csv").exists())


if __name__ == "__main__":
    unittest.main()
