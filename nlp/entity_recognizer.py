"""
Named Entity Recognition for news headlines
"""
import logging
from typing import List, Dict, Tuple
from collections import Counter
import spacy

from models.article import Article

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("EntityRecognizer")


class EntityRecognizer:
    """Extract named entities from news headlines"""
    
    def __init__(self, model_name: str = "en_core_web_sm"):
        """
        Initialize entity recognizer
        
        Args:
            model_name: spaCy model name
        """
        self.logger = logger
        self.model_name = model_name
        
        try:
            self.logger.info(f"Loading spaCy model: {model_name}")
            self.nlp = spacy.load(model_name)
            self.logger.info("spaCy model loaded successfully")
        except OSError:
            self.logger.error(f"spaCy model '{model_name}' not found. Please run: python -m spacy download {model_name}")
            raise
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract named entities from text
        
        Args:
            text: Input text
        
        Returns:
            Dictionary with entity types as keys and lists of entities as values
        """
        if not text:
            return {}
        
        try:
            doc = self.nlp(text)
            entities = {}
            
            for ent in doc.ents:
                entity_type = ent.label_
                entity_text = ent.text
                
                if entity_type not in entities:
                    entities[entity_type] = []
                
                if entity_text not in entities[entity_type]:
                    entities[entity_type].append(entity_text)
            
            return entities
        except Exception as e:
            self.logger.warning(f"Error extracting entities: {e}")
            return {}
    
    def process_articles(self, articles: List[Article]) -> List[Article]:
        """
        Extract entities from a batch of articles
        
        Args:
            articles: List of Article objects
        
        Returns:
            List of Article objects with entities field populated
        """
        self.logger.info(f"Extracting entities from {len(articles)} articles...")
        
        for i, article in enumerate(articles):
            try:
                entities = self.extract_entities(article.title)
                article.entities = entities
                
                if (i + 1) % 10 == 0:
                    self.logger.debug(f"Processed {i + 1}/{len(articles)} articles")
            except Exception as e:
                self.logger.warning(f"Error processing article {i}: {e}")
                article.entities = {}
        
        self.logger.info(f"Entity extraction complete for {len(articles)} articles")
        return articles
    
    def get_most_mentioned(self, articles: List[Article], entity_type: str = None, top_n: int = 10) -> List[Tuple]:
        """
        Get most mentioned entities across articles
        
        Args:
            articles: List of Article objects
            entity_type: Specific entity type to filter (e.g., "PERSON", "ORG", "GPE")
            top_n: Number of top entities to return
        
        Returns:
            List of tuples (entity, count) sorted by count
        """
        all_entities = []
        
        for article in articles:
            if not article.entities:
                continue
            
            if entity_type:
                all_entities.extend(article.entities.get(entity_type, []))
            else:
                # Collect all entities regardless of type
                for entities_list in article.entities.values():
                    all_entities.extend(entities_list)
        
        # Count and return top N
        counter = Counter(all_entities)
        return counter.most_common(top_n)
    
    def get_entity_timeline(self, articles: List[Article], entity: str) -> List[Article]:
        """
        Find articles mentioning a specific entity (person, org, location)
        
        Args:
            articles: List of Article objects
            entity: Entity name to search for
        
        Returns:
            List of articles mentioning the entity
        """
        matching_articles = []
        
        for article in articles:
            if not article.entities:
                continue
            
            # Check if entity appears in any entity list
            for entities_list in article.entities.values():
                if entity in entities_list:
                    matching_articles.append(article)
                    break
        
        # Sort by timestamp if available
        matching_articles.sort(
            key=lambda a: a.timestamp if a.timestamp else a.scraped_at,
            reverse=True
        )
        
        return matching_articles
