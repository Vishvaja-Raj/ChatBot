from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Ensure the VADER lexicon is downloaded
nltk.download('vader_lexicon')

# Initialize the Sentiment Intensity Analyzer
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    # Analyze the sentiment of the text
    sentiment_scores = sia.polarity_scores(text)
    
    # Determine the overall sentiment
    if sentiment_scores['compound'] >= 0.05:
        return "Happy"
    elif sentiment_scores['compound'] <= -0.05:
        return "Sad"
    else:
        return "Neutral"