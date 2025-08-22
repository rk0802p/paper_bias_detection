import spacy
from transformers import DistilBertTokenizer
import re

class TextPreprocessor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    
    def preprocess_paper(self, text):
        # Clean and tokenize academic text
        doc = self.nlp(text)
        sentences = [sent.text for sent in doc.sents]
        return sentences
    
    def extract_citations(self, text):
        # Extract citation patterns using regex
        citation_pattern = r'\[(\d+(?:,\s*\d+)*)\]'
        citations = re.findall(citation_pattern, text)
        return citations
