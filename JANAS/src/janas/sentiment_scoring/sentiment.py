from transformers import BertJapaneseTokenizer, BertForSequenceClassification, AutoTokenizer, AutoModelForSequenceClassification
import torch
from langdetect import detect
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import logging

#logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

MODEL_NAME = "christian-phu/bert-finetuned-japanese-sentiment"
tokenizer = BertJapaneseTokenizer.from_pretrained(MODEL_NAME)
model = BertForSequenceClassification.from_pretrained(MODEL_NAME)


def analyze_sentiment(article: str):
    
    """
    Function that takes in article content as a string and conduct sentiment analysis based on language. 
    If English:
        VADER 
    If Japanese:x
        BERT Tokenization
        Bert model
        Softmax
        Calculating compound score
    """

    # Detect the language of the article
    lang = detect(article)

    if lang == "en":
        # English article sentiment analysis
        print("Detected language: English") 
        sid = SentimentIntensityAnalyzer()
        sentiment = sid.polarity_scores(article)
        print(sentiment)
        print("Success in english sentiment") 
        logger.info(sentiment)
    elif lang == "ja":
        
        # Load Japanese BERT model and tokenizer
        #model_name = "christian-phu/bert-finetuned-japanese-sentiment"
        #tokenizer = AutoTokenizer.from_pretrained(model_name)
        #model = AutoModelForSequenceClassification.from_pretrained(model_name)
        #tokenizer = BertJapaneseTokenizer.from_pretrained(model_name)
        #model = BertForSequenceClassification.from_pretrained(model_name)
        
        # Tokenize and preprocess the input text
        inputs = tokenizer(article, return_tensors="pt", truncation=True, max_length=512)
        
        # Perform sentiment analysis
        outputs = model(**inputs)
        # Turns logits into readable probabilities
        probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
        sentiment_classes = ["negative", "neutral", "positive"]
        sentiment_scores = {}
        for i, prob in enumerate(probabilities[0]):
            sentiment_class = sentiment_classes[i]
            sentiment_scores[sentiment_class] = prob.item()

        weights = {"negative": -1, "neutral": 0, "positive": 1}

        # Create compound score 
        compound_score = 0
        for i in range(len(sentiment_classes)):
            sentiment_class = sentiment_classes[i]
            probability = probabilities[0][i].item()
            weight = weights[sentiment_class]
            compound_score += probability * weight

        sentiment_scores['compound'] = compound_score
        
        sentiment = sentiment_scores
        print(sentiment)
        logger.info(sentiment)
        print("successfully recorded down a sentiment for japanese")
    else:
        sentiment = {"error": f"Unsupported language detected: {lang}"}
        print('fail')

    return sentiment


