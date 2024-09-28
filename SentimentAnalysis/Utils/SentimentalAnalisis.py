# Import necessary libraries
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load the model and tokenizer from Hugging Face Model Hub
tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")

# Function to get sentiment from a review
def get_sentiment(review):
    # Encode the review
    inputs = tokenizer(review, return_tensors="pt", truncation=True, padding=True)
    
    # Perform inference
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Get predicted class (the index of the highest score)
    predictions = torch.argmax(outputs.logits, dim=1)
    
    # Map the predicted class to sentiment label
    sentiment_labels = ["very negative", "negative", "neutral", "positive", "very positive"]
    sentiment_index = predictions.item()  # Get the numerical index
    sentiment = sentiment_labels[sentiment_index]  # Get the corresponding label
    
    return sentiment, sentiment_index  # Return both label and index

