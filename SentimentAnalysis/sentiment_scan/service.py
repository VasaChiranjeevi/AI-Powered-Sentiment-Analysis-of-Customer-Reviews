from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import logging

from Utility.constant import SentimentConstants

logger = logging.getLogger(__name__)

tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")


# Function to get sentiment from a review
class SentimentScanService:
    def get_sentiment(self, review):
        try:
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

            if sentiment == 'neutral':
                sentiment_index = SentimentConstants.NEUTRAL
            elif sentiment == 'negative' or sentiment == 'very negative':
                sentiment_index = SentimentConstants.NEGATIVE
            elif sentiment == 'positive' or sentiment == 'very positive':
                sentiment_index = SentimentConstants.POSITIVE

            return sentiment_index

        except Exception as e:
            logger.info(f"Error occurred while get sentiments: {e}")
            raise e