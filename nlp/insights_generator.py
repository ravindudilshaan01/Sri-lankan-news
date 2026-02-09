"""
AI-powered insights generator
"""
import logging
import json
from typing import List, Dict
from datetime import datetime
from collections import defaultdict

from models.article import Article

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("InsightsGenerator")


class InsightsGenerator:
    """Generate AI-powered insights from analyzed news data"""
    
    def __init__(self):
        self.logger = logger
    
    def generate_daily_summary(self, articles: List[Article]) -> str:
        """
        Generate automated daily news digest
        
        Args:
            articles: List of analyzed Article objects
        
        Returns:
            Text summary of the day's news
        """
        if not articles:
            return "No articles available for summary."
        
        # Group by topic
        by_topic = defaultdict(list)
        for article in articles:
            topic = article.topic or "Other"
            by_topic[topic].append(article)
        
        summary_lines = [
            f"Daily News Summary - {datetime.now().strftime('%Y-%m-%d')}",
            f"Total Articles Analyzed: {len(articles)}",
            ""
        ]
        
        # Summarize each topic
        for topic, topic_articles in sorted(by_topic.items(), key=lambda x: len(x[1]), reverse=True):
            summary_lines.append(f"\n{topic} ({len(topic_articles)} articles):")
            
            # Show top 3 headlines
            for i, article in enumerate(topic_articles[:3], 1):
                sentiment_emoji = {"positive": "📈", "negative": "📉", "neutral": "➡️"}.get(article.sentiment, "")
                summary_lines.append(f"  {i}. {article.title} {sentiment_emoji}")
                summary_lines.append(f"     Source: {article.source}")
        
        return "\n".join(summary_lines)
    
    def identify_breaking_trends(self, articles: List[Article]) -> List[Dict]:
        """
        Identify topics or entities with sudden spikes in mentions
        
        Args:
            articles: List of Article objects
        
        Returns:
            List of trending items
        """
        trends = []
        
        # Analyze entity mentions
        entity_counts = defaultdict(int)
        for article in articles:
            if article.entities:
                for entity_type, entities in article.entities.items():
                    for entity in entities:
                        entity_counts[entity] += 1
        
        # Find entities mentioned multiple times (simple threshold)
        for entity, count in entity_counts.items():
            if count >= 3:  # Mentioned in at least 3 articles
                trends.append({
                    "type": "entity",
                    "name": entity,
                    "mentions": count
                })
        
        # sort by mentions
        trends.sort(key=lambda x: x["mentions"], reverse=True)
        
        return trends[:10]  # Top 10
    
    def compare_sources(self, articles: List[Article]) -> Dict:
        """
        Analyze how different outlets cover events
        
        Args:
            articles: List of Article objects
        
        Returns:
            Comparison statistics
        """
        by_source = defaultdict(list)
        for article in articles:
            by_source[article.source].append(article)
        
        comparison = {}
        
        for source, source_articles in by_source.items():
            # Calculate sentiment distribution
            sentiments = defaultdict(int)
            topics = defaultdict(int)
            
            for article in source_articles:
                if article.sentiment:
                    sentiments[article.sentiment] += 1
                if article.topic:
                    topics[article.topic] += 1
            
            comparison[source] = {
                "total_articles": len(source_articles),
                "sentiment_distribution": dict(sentiments),
                "top_topics": sorted(topics.items(), key=lambda x: x[1], reverse=True)[:5]
            }
        
        return comparison
    
    def export_insights(self, articles: List[Article], format: str = "json") -> str:
        """
        Export comprehensive insights report
        
        Args:
            articles: List of Article objects
            format: Output format ("json" or "text")
        
        Returns:
            Formatted report string
        """
        insights = {
            "generated_at": datetime.now().isoformat(),
            "total_articles": len(articles),
            "daily_summary": self.generate_daily_summary(articles),
            "breaking_trends": self.identify_breaking_trends(articles),
            "source_comparison": self.compare_sources(articles)
        }
        
        if format == "json":
            return json.dumps(insights, indent=2, default=str)
        else:
            # Text format
            return self.generate_daily_summary(articles)
