from textblob import TextBlob

def sentiment_classifier(text):
    p_1 = TextBlob(text).sentiment.polarity
    if p_1==1:
        return "Positive"
    else:
        return "Negative"