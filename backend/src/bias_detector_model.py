import torch
import pandas as pd
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, Trainer, TrainingArguments
from torch.utils.data import Dataset

class BiasDataset(Dataset):
    def __init__(self, texts, labels, tokenizer):
        self.encodings = tokenizer(texts, truncation=True, padding=True)
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

class BiasDetector:
    def __init__(self, num_labels=5):
        self.model = DistilBertForSequenceClassification.from_pretrained(
            'distilbert-base-uncased', 
            num_labels=num_labels
        )
        self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
        
    def train_bias_detector(self, train_dataset, val_dataset):
        training_args = TrainingArguments(
            output_dir='./results/bias_model',
            num_train_epochs=3,
            per_device_train_batch_size=16,
            per_device_eval_batch_size=64,
            warmup_steps=500,
            weight_decay=0.01,
            logging_dir='./logs',
            logging_steps=10,
            evaluation_strategy="epoch"
        )
        
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
        )
        
        trainer.train()

if __name__ == '__main__':
    # This is a placeholder for running the training.
    # It requires a larger, well-formed dataset to work correctly.
    print("Loading and preparing data...")

    # Load your annotated data
    # For demonstration, we'll use the sample, but a real run needs more data.
    try:
        df = pd.read_csv('data/annotated/sample_annotations.csv')
    except FileNotFoundError:
        print("Error: Annotation file not found. Please create 'data/annotated/sample_annotations.csv' first.")
        exit()

    # Create a mapping from bias type to integer label
    labels = list(df['bias_type'].unique())
    label2id = {label: i for i, label in enumerate(labels)}
    df['label_id'] = df['bias_type'].map(label2id)

    # For demonstration, we'll split the small sample data.
    # In a real scenario, you would use a proper train/validation split.
    train_texts = df['sentence'].tolist()
    train_labels = df['label_id'].tolist()
    val_texts = train_texts # Using same for demo
    val_labels = train_labels # Using same for demo

    detector = BiasDetector(num_labels=len(labels))
    
    train_dataset = BiasDataset(train_texts, train_labels, detector.tokenizer)
    val_dataset = BiasDataset(val_texts, val_labels, detector.tokenizer)

    print("Bias detector model script created. You would run this to train the model.")
    # To run training, you would call:
    # print("Starting training...")
    # detector.train_bias_detector(train_dataset, val_dataset)
    # print("Training complete.")
