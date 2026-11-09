import json
import unittest
from pathlib import Path
from src.retail_halo_incrementality_engine import run_pipeline


class TestRetailHaloIncrementalityEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base_dir = Path(__file__).resolve().parent.parent
        cls.data_dir = cls.base_dir.parent / "data_cache"
        cls.out_dir = cls.base_dir / "outputs"
        cls.summary = run_pipeline(cls.data_dir, cls.out_dir)

    def test_01_sha256_and_record_counts(self) -> None:
        self.assertEqual(self.summary["total_verified_records"], 105600)
        self.assertEqual(
            self.summary["dataset_row_counts"]["hillstrom_omnichannel_retail"], 64000
        )
        self.assertEqual(
            self.summary["dataset_row_counts"]["uci_online_news_social_velocity"], 39644
        )
        self.assertEqual(
            self.summary["dataset_row_counts"]["uci_youtube_creator_engagement"], 1956
        )

    def test_02_geo_holdout_and_matched_market_did(self) -> None:
        geo = self.summary["geo_holdout_results"]
        self.assertAlmostEqual(geo["visit_lift_relative_pct"], 57.35, places=2)
        self.assertAlmostEqual(geo["conversion_lift_relative_pct"], 86.53, places=2)
        self.assertAlmostEqual(geo["spend_lift_relative_pct"], 91.42, places=2)
        self.assertGreater(self.summary["matched_market_did_ate_usd"], 0.50)

    def test_03_synthetic_control_simplex_conservation(self) -> None:
        sc = self.summary["synthetic_control_results"]
        self.assertEqual(sc["donor_markets_count"], 24)
        self.assertAlmostEqual(sc["simplex_weight_sum"], 1.0, places=5)
        self.assertGreaterEqual(sc["min_weight"], 0.0)
        self.assertLess(sc["pre_intervention_rmspe"], 0.05)

    def test_04_omnichannel_halo_and_mmm_calibration(self) -> None:
        halo = self.summary["omnichannel_halo_results"]
        self.assertAlmostEqual(halo["omnichannel_halo_multiplier"], 2.89, places=2)
        self.assertLess(halo["ridge_mmm_holdout_mape_pct"], 12.0)
        self.assertEqual(len(halo["surface_lifts"]), 4)

    def test_05_native_vs_3p_reconciliation_zero_drift(self) -> None:
        dq = self.summary["data_quality_reconciliation"]
        self.assertAlmostEqual(dq["raw_native_vs_3p_discrepancy_pct"], 6.84, places=2)
        self.assertEqual(dq["post_reconciliation_variance_usd"], 0.0)
        self.assertEqual(dq["governed_house_metrics_count"], 12)
        self.assertTrue((self.out_dir / "house_metric_dictionary.json").exists())


if __name__ == "__main__":
    unittest.main()
