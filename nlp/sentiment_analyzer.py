"""
Sentiment analysis for news headlines
"""
import logging
from typing import List, Tuple, Dict
from textblob import TextBlob
from transformers import pipeline
import torch

from models.article import Article

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SentimentAnalyzer")


class SentimentAnalyzer:
    """Analyze sentiment of news headlines"""
    
    def __init__(self, use_transformers: bool = True):
        """
        Initialize sentiment analyzer
        
        Args:
            use_transformers: If True, use transformer model; else use TextBlob
        """
        self.use_transformers = use_transformers
        self.logger = logger
        
        if use_transformers:
            try:
                self.logger.info("Loading transformer model for sentiment analysis...")
                self.pipeline = pipeline(
                    "sentiment-analysis",
                    model="distilbert-base-uncased-finetuned-sst-2-english",
                    device=0 if torch.cuda.is_available() else -1
                )
                self.logger.info("Transformer model loaded successfully")
            except Exception as e:
                self.logger.warning(f"Failed to load transformer model: {e}. Falling back to TextBlob")
                self.use_transformers = False
                self.pipeline = None
        else:
            self.pipeline = None
    
    def analyze_sentiment(self, text: str) -> Tuple[str, float]:
        """
        Analyze sentiment of text
        
        Args:
            text: Input text to analyze
        
        Returns:
            Tuple of (sentiment_label, confidence_score)
        """
        if not text:
            return "neutral", 0.0
        
        if self.use_transformers and self.pipeline:
            return self._analyze_with_transformers(text)
        else:
            return self._analyze_with_textblob(text)
    
    def _analyze_with_transformers(self, text: str) -> Tuple[str, float]:
        """Analyze using transformer model"""
        try:
            result = self.pipeline(text[:512])[0]  # Limit to 512 tokens
            label = result['label'].lower()  # "POSITIVE" or "NEGATIVE"
            score = result['score']
            return label, score
        except Exception as e:
            self.logger.warning(f"Transformer analysis failed: {e}. Falling back to TextBlob")
            return self._analyze_with_textblob(text)
    
    def _analyze_with_textblob(self, text: str) -> Tuple[str, float]:
        """Analyze using TextBlob"""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            # Convert polarity to label and confidence
            if polarity > 0.1:
                label = "positive"
                score = min(polarity, 1.0)
            elif polarity < -0.1:
                label = "negative"
                score = min(abs(polarity), 1.0)
            else:
                label = "neutral"
                score = 1.0 - abs(polarity)
            
            return label, score
        except Exception as e:
            self.logger.error(f"TextBlob analysis failed: {e}")
            return "neutral", 0.0
    
    def batch_analyze(self, articles: List[Article]) -> List[Article]:
        """
        Analyze sentiment for a batch of articles
        
        Args:
            articles: List of Article objects
        
        Returns:
            List of Article objects with sentiment fields populated
        """
        self.logger.info(f"Analyzing sentiment for {len(articles)} articles...")
        
        for i, article in enumerate(articles):
            try:
                sentiment, score = self.analyze_sentiment(article.title)
                article.sentiment = sentiment
                article.sentiment_score = score
                
                if (i + 1) % 10 == 0:
                    self.logger.debug(f"Processed {i + 1}/{len(articles)} articles")
            except Exception as e:
                self.logger.warning(f"Error analyzing article {i}: {e}")
                article.sentiment = "neutral"
                article.sentiment_score = 0.0
        
        self.logger.info(f"Sentiment analysis complete for {len(articles)} articles")
        return articles
    
    def get_sentiment_distribution(self, articles: List[Article]) -> Dict[str, int]:
        """Get distribution of sentiments across articles"""
        distribution = {"positive": 0, "negative": 0, "neutral": 0}
        
        for article in articles:
            if article.sentiment:
                distribution[article.sentiment] = distribution.get(article.sentiment, 0) + 1
        
        return distribution
