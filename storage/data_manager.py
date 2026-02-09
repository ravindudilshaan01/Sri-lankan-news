"""
Data manager for persisting and retrieving news articles
"""
import os
import json
import pandas as pd
from typing import List, Optional
from datetime import datetime, timedelta
import logging

from models.article import Article
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DataManager")


class DataManager:
    """Handles storage and retrieval of news articles"""
    
    def __init__(self, csv_file: str = config.NEWS_DATA_FILE):
        self.csv_file = csv_file
        self.logger = logger
    
    def save_to_csv(self, articles: List[Article], append: bool = True):
        """
        Save articles to CSV file
        
        Args:
            articles: List of Article objects
            append: If True, append to existing file; if False, overwrite
        """
        if not articles:
            self.logger.warning("No articles to save")
            return
        
        # Convert articles to dictionaries
        data = [article.to_dict() for article in articles]
        df_new = pd.DataFrame(data)
        
        if append and os.path.exists(self.csv_file):
            # Load existing data
            df_existing = pd.read_csv(self.csv_file)
            
            # Remove duplicates based on URL
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            df_combined = df_combined.drop_duplicates(subset=['url'], keep='last')
            
            df_combined.to_csv(self.csv_file, index=False)
            self.logger.info(f"Appended {len(df_new)} articles to {self.csv_file} ({len(df_combined)} total)")
        else:
            df_new.to_csv(self.csv_file, index=False)
            self.logger.info(f"Saved {len(df_new)} articles to {self.csv_file}")
    
    def load_from_csv(self) -> List[Article]:
        """Load articles from CSV file"""
        if not os.path.exists(self.csv_file):
            self.logger.warning(f"CSV file not found: {self.csv_file}")
            return []
        
        try:
            df = pd.read_csv(self.csv_file)
            articles = []
            
            for _, row in df.iterrows():
                try:
                    # Convert NaN to None
                    row_dict = row.where(pd.notna(row), None).to_dict()
                    
                    # Parse entities if they exist as JSON string
                    if row_dict.get('entities') and isinstance(row_dict['entities'], str):
                        try:
                            row_dict['entities'] = json.loads(row_dict['entities'])
                        except:
                            row_dict['entities'] = None
                    
                    article = Article.from_dict(row_dict)
                    articles.append(article)
                except Exception as e:
                    self.logger.warning(f"Error loading article: {e}")
                    continue
            
            self.logger.info(f"Loaded {len(articles)} articles from {self.csv_file}")
            return articles
            
        except Exception as e:
            self.logger.error(f"Error loading CSV: {e}")
            return []
    
    def get_latest_articles(self, hours: int = 24) -> List[Article]:
        """
        Get articles from the last N hours
        
        Args:
            hours: Number of hours to look back
        """
        articles = self.load_from_csv()
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        latest = [
            article for article in articles
            if article.scraped_at and article.scraped_at >= cutoff_time
        ]
        
        self.logger.info(f"Found {len(latest)} articles from the last {hours} hours")
        return latest
    
    def get_by_source(self, source: str) -> List[Article]:
        """Get articles from a specific source"""
        articles = self.load_from_csv()
        filtered = [article for article in articles if article.source == source]
        return filtered
    
    def get_statistics(self) -> dict:
        """Get basic statistics about stored articles"""
        articles = self.load_from_csv()
        
        if not articles:
            return {"total": 0}
        
        sources = {}
        for article in articles:
            sources[article.source] = sources.get(article.source, 0) + 1
        
        return {
            "total": len(articles),
            "by_source": sources,
            "oldest": min((a.scraped_at for a in articles if a.scraped_at), default=None),
            "newest": max((a.scraped_at for a in articles if a.scraped_at), default=None)
        }
