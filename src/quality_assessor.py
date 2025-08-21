import re
import numpy as np

class QualityAssessor:
    def __init__(self):
        self.weights = {
            'data_availability': 0.2,
            'code_availability': 0.2,
            'methodology_strength': 0.4,
            'sample_size': 0.2
        }

    # --- Week 5: Quality Assessment Framework ---

    def check_data_availability(self, text):
        """Checks for a data availability statement with more robust patterns."""
        patterns = [
            r"data availability statement", r"data are available", r"data can be found",
            r"dataset is available", r"data can be accessed", r"supporting data",
            r"data set", r"dataset", r"data repository", r"supplementary materials",
            r"data sharing", r"data access", r"data availability"
        ]
        return any(re.search(p, text, re.IGNORECASE) for p in patterns)

    def check_code_availability(self, text):
        """Checks for a code availability statement with more robust patterns."""
        patterns = [
            r"code availability", r"code is available", r"scripts are available",
            r"analysis code", r"repository", r"github.com", r"gitlab.com",
            r"source code", r"implementation", r"algorithm", r"pseudocode",
            r"code repository", r"software", r"program"
        ]
        return any(re.search(p, text, re.IGNORECASE) for p in patterns)

    def assess_methodology_strength(self, text):
        """Assess the strength of the methodology based on keywords."""
        strength_score = 0
        if any(re.search(p, text, re.IGNORECASE) for p in [r"control group", r"controlled experiment"]):
            strength_score += 1
        if any(re.search(p, text, re.IGNORECASE) for p in [r"randomized", r"randomly assigned"]):
            strength_score += 1
        if any(re.search(p, text, re.IGNORECASE) for p in [r"double-blind", r"single-blind", r"blinded study"]):
            strength_score += 1
        return strength_score / 3.0 # Normalize score

    # --- Week 6: Methodology Validation ---

    def assess_sample_size(self, text):
        """Extracts sample size and provides a basic assessment with a more robust regex."""
        # Extracts numbers following patterns like 'n = ', 'N = ', 'sample of', etc.
        matches = re.findall(r"(?:sample size of|sample of|n\s*=\s*|N\s*=\s*)(\d+)", text, re.IGNORECASE)
        if not matches:
            return 0, None # Return 0 score and no sample size found
        
        sample_size = max([int(m) for m in matches]) # Take the largest mentioned sample size
        
        # Simple heuristic: larger sample is better.
        score = np.log10(sample_size) / 4 # Normalize score (e.g., n=100 -> 0.5, n=10000 -> 1.0)
        return min(score, 1.0), sample_size # Cap score at 1.0

    # --- Week 6: Quality Score Integration ---

    def calculate_unified_quality_score(self, text):
        """Combines multiple quality metrics into a single score."""
        scores = {
            'data_availability': 1.0 if self.check_data_availability(text) else 0.0,
            'code_availability': 1.0 if self.check_code_availability(text) else 0.0,
            'methodology_strength': self.assess_methodology_strength(text),
            'sample_size': self.assess_sample_size(text)[0]
        }

        weighted_score = sum(scores[metric] * self.weights[metric] for metric in self.weights)
        return weighted_score, scores

    def create_confidence_intervals(self, score):
        """
        Placeholder for creating confidence intervals for the quality score.
        """
        # For demonstration, we return a simple fixed interval.
        confidence_interval = (max(0, score - 0.1), min(1.0, score + 0.1))
        return confidence_interval

if __name__ == '__main__':
    assessor = QualityAssessor()
    
    paper_text_good = """
    This was a randomized, double-blind, controlled experiment with a sample size of 500. 
    The data are available upon request. Our code is available at github.com/example/repo.
    """
    
    paper_text_poor = """
    We looked at some data and found some interesting results.
    """

    print("--- Assessing Good Quality Paper ---")
    unified_score_good, scores_good = assessor.calculate_unified_quality_score(paper_text_good)
    confidence_interval_good = assessor.create_confidence_intervals(unified_score_good)
    print(f"Individual Scores: {scores_good}")
    print(f"Unified Quality Score: {unified_score_good:.4f}")
    print(f"Confidence Interval: {confidence_interval_good}")

    print("\n--- Assessing Poor Quality Paper ---")
    unified_score_poor, scores_poor = assessor.calculate_unified_quality_score(paper_text_poor)
    confidence_interval_poor = assessor.create_confidence_intervals(unified_score_poor)
    print(f"Individual Scores: {scores_poor}")
    print(f"Unified Quality Score: {unified_score_poor:.4f}")
    print(f"Confidence Interval: {confidence_interval_poor}")
