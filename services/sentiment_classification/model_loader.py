from transformers import AutoTokenizer, AutoModelForSequenceClassification
from services.sentiment_classification.config import MODEL_PATH

def load_sentiment_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
    model.eval()
    return tokenizer, model
