import pandas as pd
import os

class AnnotationTool:
    def __init__(self, preprocessed_dir='data/preprocessed', annotated_dir='data/annotated'):
        self.preprocessed_dir = preprocessed_dir
        self.annotated_dir = annotated_dir
        os.makedirs(self.annotated_dir, exist_ok=True)

    def annotate_paper(self, filename):
        filepath = os.path.join(self.preprocessed_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                sentences = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            print(f"Error: File not found at {filepath}. Make sure data is preprocessed.")
            return

        annotations = []
        bias_types = ['Selection Bias', 'Funding Bias', 'Publication Bias', 'Cognitive Bias', 'No Bias']
        
        print(f"Annotating {filename}. Enter the number corresponding to the bias type.")
        for i, bias_type in enumerate(bias_types):
            print(f"{i}: {bias_type}")

        for i, sentence in enumerate(sentences):
            print(f"\nSentence {i+1}/{len(sentences)}: {sentence}")
            while True:
                try:
                    label_num = input("Bias label: ")
                    if not label_num:
                        continue
                    label_idx = int(label_num)
                    if 0 <= label_idx < len(bias_types):
                        annotations.append({
                            'sentence': sentence,
                            'bias_type': bias_types[label_idx],
                            'label': 1 if bias_types[label_idx] != 'No Bias' else 0
                        })
                        break
                    else:
                        print(f"Invalid input. Please enter a number between 0 and {len(bias_types)-1}.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

        # Save annotations
        output_path = os.path.join(self.annotated_dir, f"{os.path.splitext(filename)[0]}_annotated.csv")
        df = pd.DataFrame(annotations)
        df.to_csv(output_path, index=False)
        print(f"Annotations saved to {output_path}")

if __name__ == '__main__':
    tool = AnnotationTool()
    # This is an example of how to run it.
    # You would need a file named 'example_paper.txt' in 'data/preprocessed'
    # tool.annotate_paper('example_paper.txt')
    print("Annotation tool script created. Run this script with a preprocessed file to start annotating.")
