import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class TraditionalModels:

    def train_tfidf_model(self, df):
        """Trains a TF-IDF and Logistic Regression model."""
        print("\n--- Training TF-IDF Model ---")
        # Map bias types to a single binary label: 0 for No Bias, 1 for Bias
        df['binary_label'] = df['label'].apply(lambda x: 0 if x == 0 else 1)
        
        X_train, X_test, y_train, y_test = train_test_split(
            df['sentence'], df['binary_label'], test_size=0.3, random_state=42
        )

        vectorizer = TfidfVectorizer(max_features=5000)
        X_train_tfidf = vectorizer.fit_transform(X_train)
        X_test_tfidf = vectorizer.transform(X_test)

        model = LogisticRegression()
        model.fit(X_train_tfidf, y_train)

        y_pred = model.predict(X_test_tfidf)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"TF-IDF Model Accuracy: {accuracy:.4f}")
        return model, vectorizer

    def rule_based_detector(self, sentence):
        """A simple rule-based detector for identifying potential funding bias."""
        funding_keywords = ['funded by', 'sponsored by', 'financial support from', 'grant from']
        for keyword in funding_keywords:
            if re.search(keyword, sentence, re.IGNORECASE):
                return "Funding Bias"
        return "No Bias"

class EnsembleModel:
    def __init__(self, dl_model, tfidf_model, rule_based_detector):
        self.dl_model = dl_model
        self.tfidf_model = tfidf_model
        self.rule_based_detector = rule_based_detector

    def predict(self, sentence):
        """Placeholder for an ensemble prediction method."""
        # In a real implementation, you would get predictions from each model
        # and combine them using a voting or weighting scheme.
        print(f"\n--- Ensemble Prediction for: '{sentence}' ---")
        
        # 1. Deep Learning Model Prediction (requires trained model)
        # dl_prediction = self.dl_model.predict(sentence)
        print("DL Model Prediction: (placeholder)")

        # 2. TF-IDF Model Prediction (requires trained model)
        # tfidf_prediction = self.tfidf_model.predict(vectorizer.transform([sentence]))
        print("TF-IDF Model Prediction: (placeholder)")

        # 3. Rule-based prediction
        rule_prediction = self.rule_based_detector(sentence)
        print(f"Rule-Based Prediction: {rule_prediction}")

        # Combine results (e.g., simple majority vote)
        final_prediction = rule_prediction # Placeholder logic
        return final_prediction

if __name__ == '__main__':
    print("Traditional Models script created.")
    try:
        df = pd.read_csv('data/annotated/sample_annotations.csv')
    except FileNotFoundError:
        print("Error: Annotation file not found.")
        exit()

    models = TraditionalModels()
    
    # Demonstrate training the TF-IDF model
    # Note: This will fail with the tiny sample file, as splitting it leaves no data for training or testing.
    if len(df) > 1:
        # models.train_tfidf_model(df.copy()) # copy to avoid changing original df
        pass

    # Demonstrate the rule-based detector
    print("\n--- Testing Rule-Based Detector ---")
    test_sentence_1 = "This study was funded by a major corporation."
    test_sentence_2 = "The methodology is sound and the results are clear."
    print(f"'{test_sentence_1}' -> {models.rule_based_detector(test_sentence_1)}")
    print(f"'{test_sentence_2}' -> {models.rule_based_detector(test_sentence_2)}")

    # Demonstrate the ensemble placeholder
    ensemble = EnsembleModel(dl_model=None, tfidf_model=None, rule_based_detector=models.rule_based_detector)
    ensemble.predict(test_sentence_1)
