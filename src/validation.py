import pandas as pd
from sklearn.metrics import cohen_kappa_score

class DatasetValidator:
    def __init__(self, annotated_dir='data/annotated'):
        self.annotated_dir = annotated_dir

    def calculate_iaa(self, file1, file2):
        """
        Calculates the Inter-Annotator Agreement (IAA) between two annotation files.
        Assumes the files are CSVs with a 'label' column.
        """
        try:
            annotator1_df = pd.read_csv(os.path.join(self.annotated_dir, file1))
            annotator2_df = pd.read_csv(os.path.join(self.annotated_dir, file2))
        except FileNotFoundError as e:
            print(f"Error: {e}. Make sure both annotation files exist.")
            return None

        if len(annotator1_df) != len(annotator2_df):
            print("Error: Annotation files have different numbers of sentences.")
            return None

        # Assuming the 'label' column contains the annotations
        kappa = cohen_kappa_score(annotator1_df['label'], annotator2_df['label'])
        return kappa

    def validate_quality(self, filename):
        """
        Performs basic quality checks on an annotation file.
        """
        try:
            df = pd.read_csv(os.path.join(self.annotated_dir, filename))
        except FileNotFoundError:
            print(f"Error: File not found at {os.path.join(self.annotated_dir, filename)}")
            return False

        # Check for missing labels
        if df['label'].isnull().any():
            print(f"Warning: Missing labels found in {filename}")

        # Check for consistent labeling
        # Example: Ensure 'No Bias' has a label of 0, and others have 1
        mismatch = df[((df['bias_type'] == 'No Bias') & (df['label'] != 0)) |
                      ((df['bias_type'] != 'No Bias') & (df['label'] != 1))]
        
        if not mismatch.empty:
            print(f"Warning: Inconsistent labels found in {filename}:")
            print(mismatch)
        
        print(f"Quality checks passed for {filename}.")
        return True

if __name__ == '__main__':
    validator = DatasetValidator()
    # Example of how to run the functions
    # You would need two annotation files from two different annotators for the same paper.
    # kappa = validator.calculate_iaa('paper1_annotatorA.csv', 'paper1_annotatorB.csv')
    # if kappa is not None:
    #     print(f"Cohen's Kappa: {kappa}")
    # validator.validate_quality('sample_annotations.csv')
    print("Dataset validation script created.")
