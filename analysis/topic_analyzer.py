"""
Topic analysis using keyword matching and basic categorization
"""
import logging
from typing import List, Dict, Tuple
from collections import Counter

from models.article import Article
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TopicAnalyzer")


class TopicAnalyzer:
    """Analyze topics in news articles using keyword matching"""
    
    def __init__(self, topic_keywords: Dict[str, List[str]] = None):
        """
        Initialize topic analyzer
        
        Args:
            topic_keywords: Dictionary mapping topic names to lists of keywords
        """
        self.logger = logger
        self.topic_keywords = topic_keywords or config.TOPIC_KEYWORDS
    
    def categorize_headline(self, text: str) -> str:
        """
        Categorize a headline into a topic
        
        Args:
            text: Headline text
        
        Returns:
            Topic name or "Other" if no match
        """
        if not text:
            return "Other"
        
        text_lower = text.lower()
        topic_scores = {}
        
        # Count keyword matches for each topic
        for topic, keywords in self.topic_keywords.items():
            score = sum(1 for keyword in keywords if keyword.lower() in text_lower)
            if score > 0:
                topic_scores[topic] = score
        
        # Return topic with highest score
        if topic_scores:
            return max(topic_scores.items(), key=lambda x: x[1])[0]
        
        return "Other"
    
    def process_articles(self, articles: List[Article]) -> List[Article]:
        """
        Categorize topics for all articles
        
        Args:
            articles: List of Article objects
        
        Returns:
            List of Article objects with topic field populated
        """
        self.logger.info(f"Categorizing topics for {len(articles)} articles...")
        
        for article in articles:
            try:
                topic = self.categorize_headline(article.title)
                article.topic = topic
            except Exception as e:
                self.logger.warning(f"Error categorizing article: {e}")
                article.topic = "Other"
        
        self.logger.info("Topic categorization complete")
        return articles
    
    def get_trending_topics(self, articles: List[Article], top_n: int = 10) -> List[Tuple]:
        """
        Get trending topics from articles
        
        Args:
            articles: List of Article objects
            top_n: Number of top topics to return
        
        Returns:
            List of tuples (topic, count)
        """
        topics = [article.topic for article in articles if article.topic]
        counter = Counter(topics)
        return counter.most_common(top_n)
    
    def get_topic_distribution(self, articles: List[Article]) -> Dict[str, int]:
        """Get distribution of topics across articles"""
        distribution = {}
        
        for article in articles:
            if article.topic:
                distribution[article.topic] = distribution.get(article.topic, 0) + 1
        
        return distribution
    
    def generate_topic_report(self, articles: List[Article]) -> Dict:
        """
        Generate comprehensive topic analysis report
        
        Args:
            articles: List of Article objects
        
        Returns:
            Dictionary containing various topic statistics
        """
        self.logger.info("Generating topic report...")
        
        distribution = self.get_topic_distribution(articles)
        trending = self.get_trending_topics(articles)
        
        # Group articles by topic
        by_topic = {}
        for article in articles:
            topic = article.topic or "Other"
            if topic not in by_topic:
                by_topic[topic] = []
            by_topic[topic].append(article)
        
        report = {
            "total_articles": len(articles),
            "distribution": distribution,
            "trending_topics": trending,
            "articles_by_topic": {
                topic: len(articles_list)
                for topic, articles_list in by_topic.items()
            }
        }
        
        return report
