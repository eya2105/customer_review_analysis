from __future__ import annotations

import sys
from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from customer_review_analysis.config import get_config, get_path


class ConfigTests(unittest.TestCase):
    def test_config_file_exists(self) -> None:
        self.assertTrue((REPO_ROOT / "config.yaml").exists())

    def test_project_paths_resolve(self) -> None:
        config = get_config()
        self.assertIn("paths", config)
        self.assertTrue(get_path("raw_data", "data/raw/all_california_gym_reviews.csv").exists())


if __name__ == "__main__":
    unittest.main()
