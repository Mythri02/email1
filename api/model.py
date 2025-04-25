# model.py
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch

model_name = "distilbert-base-uncased"

# Load once and reuse
tokenizer = DistilBertTokenizer.from_pretrained(model_name)
model = DistilBertForSequenceClassification.from_pretrained(model_name, num_labels=2)
model.eval()  # Disable training mode

def predict_email(email_text):
    inputs = tokenizer(email_text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    predicted_class = torch.argmax(outputs.logits, dim=-1).item()
    return predicted_class
