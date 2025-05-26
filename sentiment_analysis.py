from textblob import TextBlob

def get_sentiment(text):
    if not isinstance(text, str) or text.strip() == "":
        return "Neutral"
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"
