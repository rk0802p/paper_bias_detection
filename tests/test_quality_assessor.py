import unittest
import sys
import os

# Add the src directory to the Python path to import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.quality_assessor import QualityAssessor

class TestQualityAssessor(unittest.TestCase):

    def setUp(self):
        """Set up a new QualityAssessor instance for each test."""
        self.assessor = QualityAssessor()

    def test_data_availability(self):
        """Test the check_data_availability function."""
        good_text = "Our data are available in the supplementary materials."
        bad_text = "We analyzed the data."
        self.assertTrue(self.assessor.check_data_availability(good_text))
        self.assertFalse(self.assessor.check_data_availability(bad_text))

    def test_unified_score(self):
        """Test the unified quality score calculation."""
        # A text that should score relatively high
        high_quality_text = """
        This was a randomized, double-blind, controlled experiment with a sample size of 500. 
        The data are available upon request. Our code is available at github.com/example/repo.
        """
        # A text that should score low
        low_quality_text = "We looked at some data."

        score_high, _ = self.assessor.calculate_unified_quality_score(high_quality_text)
        score_low, _ = self.assessor.calculate_unified_quality_score(low_quality_text)

        self.assertGreater(score_high, 0.5)
        self.assertLess(score_low, 0.3)

if __name__ == '__main__':
    unittest.main()
