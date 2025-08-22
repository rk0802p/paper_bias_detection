import pandas as pd
import numpy as np

class DatasetUtils:
    def __init__(self, annotated_dir='data/annotated'):
        self.annotated_dir = annotated_dir

    def balance_dataset(self, filename, strategy='undersample'):
        """
        Balances the dataset using the specified strategy.
        Currently, only undersampling is implemented.
        """
        try:
            df = pd.read_csv(os.path.join(self.annotated_dir, filename))
        except FileNotFoundError:
            print(f"Error: File not found at {os.path.join(self.annotated_dir, filename)}")
            return None

        if strategy == 'undersample':
            bias_df = df[df['label'] == 1]
            no_bias_df = df[df['label'] == 0]

            if len(bias_df) == 0 or len(no_bias_df) == 0:
                print("Cannot balance a dataset with zero samples in one class.")
                return df

            if len(bias_df) < len(no_bias_df):
                no_bias_df_sampled = no_bias_df.sample(n=len(bias_df), random_state=42)
                balanced_df = pd.concat([bias_df, no_bias_df_sampled])
            else: # Oversample the minority class if it's the 'no_bias' class
                bias_df_sampled = bias_df.sample(n=len(no_bias_df), random_state=42)
                balanced_df = pd.concat([bias_df_sampled, no_bias_df])

            print(f"Dataset balanced via undersampling. Original size: {len(df)}, New size: {len(balanced_df)}")
            return balanced_df.sample(frac=1, random_state=42).reset_index(drop=True)
        else:
            print(f"Strategy '{strategy}' not implemented.")
            return df

    def augment_data(self, df):
        """
        Placeholder for data augmentation techniques.
        Real implementation could involve back-translation, synonym replacement, etc.
        """
        print("Data augmentation placeholder. This would increase the size of the training data.")
        # For example, you could find sentences with bias and replace certain words with synonyms.
        # This is a complex task and requires a good thesaurus or a pre-trained language model.
        return df

if __name__ == '__main__':
    utils = DatasetUtils()
    # Example of how to run the functions
    # balanced_df = utils.balance_dataset('sample_annotations.csv')
    # if balanced_df is not None:
    #     augmented_df = utils.augment_data(balanced_df)
    #     print(augmented_df.head())
    print("Dataset utilities script created.")
