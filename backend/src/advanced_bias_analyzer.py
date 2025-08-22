import re
import pandas as pd
import numpy as np

class AdvancedBiasAnalyzer:

    def __init__(self):
        self.bias_patterns = {
            "Confirmation Bias": [
                r"confirms our hypothesis", r"proves our theory", r"as we predicted",
                r"consistent with our beliefs", r"results support our view",
                r"demonstrates that", r"shows that", r"validates our approach",
                r"confirms the effectiveness", r"proves the superiority",
                r"to our knowledge", r"first and substantial", r"elegant",
                r"clearly shows", r"obviously", r"evidently", r"naturally",
                r"as expected", r"not surprisingly", r"obviously superior"
            ],
            "Selection Bias": [
                r"participants were excluded", r"sample was limited to", r"data was filtered",
                r"unrepresentative sample", r"non-random sample", r"selected based on",
                r"chosen for", r"restricted to", r"focused on", r"convenience sample",
                r"we focus on", r"this paper focuses on", r"we consider only",
                r"limited to", r"constrained to", r"specific to", r"particular case",
                r"selected subset", r"filtered dataset", r"curated data"
            ],
            "Publication Bias": [
                r"negative results were not published", r"studies with null results",
                r"file drawer problem", r"tendency to publish positive findings",
                r"significant results", r"positive outcomes", r"successful implementation",
                r"promising results", r"encouraging findings",
                r"state-of-the-art", r"outperforms", r"achieves better",
                r"superior performance", r"excellent results", r"remarkable",
                r"outstanding", r"exceptional", r"breakthrough", r"novel approach"
            ]
        }

    def linguistic_pattern_detector(self, text):
        """Detects bias based on a dictionary of linguistic patterns."""
        detected_biases = []
        for bias_type, patterns in self.bias_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    detected_biases.append(bias_type)
                    break # Move to the next bias type once a pattern is found
        return list(set(detected_biases)) # Return unique bias types found

class StatisticalAnalyzer:

    def extract_p_values(self, text):
        """Extracts p-values from text."""
        # This regex looks for patterns like p < 0.05, p = 0.01, p > .001
        p_value_pattern = r"p\s*(?:<|=|>|\u2264|\u2265)\s*(\d*\.?\d+)"
        return [float(p) for p in re.findall(p_value_pattern, text)]

    def detect_p_hacking(self, p_values):
        """Simple heuristic for detecting potential p-hacking."""
        # A common heuristic is to check for a large number of p-values just under 0.05
        suspicious_p_values = [p for p in p_values if 0.04 < p < 0.05]
        if len(suspicious_p_values) > 0 and len(p_values) > 0:
            # If a significant portion of p-values fall in this narrow, significant range
            if (len(suspicious_p_values) / len(p_values)) > 0.5: # Arbitrary threshold
                return True
        return False

    def validate_methodology(self, text):
        """Checks for the presence of important methodology keywords."""
        validation_rules = {
            "mentions_control_group": [r"control group", r"controlled experiment"],
            "mentions_randomization": [r"randomized", r"randomly assigned"],
            "mentions_blinding": [r"double-blind", r"single-blind", r"blinded study"]
        }
        
        methodology_checks = {}
        for check, patterns in validation_rules.items():
            methodology_checks[check] = any(re.search(p, text, re.IGNORECASE) for p in patterns)
        
        return methodology_checks

if __name__ == '__main__':
    analyzer = AdvancedBiasAnalyzer()
    statistical_analyzer = StatisticalAnalyzer()

    # --- Test Linguistic Pattern Detector ---
    print("--- Testing Linguistic Pattern Detector ---")
    test_sentence_1 = "Our results prove our theory that this is effective."
    test_sentence_2 = "The study sample was limited to young adults, so results may not be generalizable."
    print(f"'{test_sentence_1}' -> {analyzer.linguistic_pattern_detector(test_sentence_1)}")
    print(f"'{test_sentence_2}' -> {analyzer.linguistic_pattern_detector(test_sentence_2)}")

    # --- Test Statistical Analyzer ---
    print("\n--- Testing Statistical Analyzer ---")
    stats_text = "The results were significant (p < 0.05). Another test showed p = 0.045. We also found p > 0.06."
    p_values = statistical_analyzer.extract_p_values(stats_text)
    print(f"Extracted p-values from text: {p_values}")
    print(f"P-hacking suspected: {statistical_analyzer.detect_p_hacking(p_values)}")

    # --- Test Methodology Validator ---
    print("\n--- Testing Methodology Validator ---")
    method_text_1 = "This was a randomized, double-blind, controlled experiment."
    method_text_2 = "We observed the participants over a period of time."
    print(f"'{method_text_1}' -> {statistical_analyzer.validate_methodology(method_text_1)}")
    print(f"'{method_text_2}' -> {statistical_analyzer.validate_methodology(method_text_2)}")