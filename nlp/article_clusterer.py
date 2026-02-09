"""
Article clustering and similarity detection
"""
import logging
import numpy as np
from typing import List, Dict, Tuple
from sklearn.cluster import DBSCAN, KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

from models.article import Article
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ArticleClusterer")


class ArticleClusterer:
    """Cluster similar articles and detect duplicates"""
    
    def __init__(self, model_name: str = config.SENTENCE_TRANSFORMER_MODEL):
        """
        Initialize article clusterer
        
        Args:
            model_name: Sentence transformer model name
        """
        self.logger = logger
        self.model_name = model_name
        
        try:
            self.logger.info(f"Loading sentence transformer model: {model_name}")
            self.model = SentenceTransformer(model_name)
            self.logger.info("Model loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to load model: {e}")
            raise
    
    def generate_embeddings(self, articles: List[Article]) -> np.ndarray:
        """
        Generate embeddings for articles
        
        Args:
            articles: List of Article objects
        
        Returns:
            NumPy array of embeddings
        """
        texts = [article.title for article in articles]
        self.logger.info(f"Generating embeddings for {len(texts)} articles...")
        
        embeddings = self.model.encode(texts, show_progress_bar=True)
        self.logger.info("Embeddings generated successfully")
        
        return embeddings
    
    def find_similar_articles(
        self, 
        query_article: Article, 
        articles: List[Article], 
        top_n: int = 5,
        threshold: float = 0.7
    ) -> List[Tuple[Article, float]]:
        """
        Find articles similar to a query article
        
        Args:
            query_article: Article to find similar articles for
            articles: List of articles to search in
            top_n: Number of similar articles to return
            threshold: Minimum similarity threshold
        
        Returns:
            List of tuples (article, similarity_score)
        """
        # Generate embeddings
        query_embedding = self.model.encode([query_article.title])[0]
        article_embeddings = self.generate_embeddings(articles)
        
        # Calculate similarities
        similarities = cosine_similarity([query_embedding], article_embeddings)[0]
        
        # Get top N similar articles
        similar_indices = np.argsort(similarities)[::-1][:top_n + 1]  # +1 to handle self-match
        
        results = []
        for idx in similar_indices:
            if articles[idx].url != query_article.url and similarities[idx] >= threshold:
                results.append((articles[idx], float(similarities[idx])))
        
        return results[:top_n]
    
    def detect_duplicates(
        self, 
        articles: List[Article], 
        threshold: float = config.SIMILARITY_THRESHOLD
    ) -> List[List[Article]]:
        """
        Detect duplicate or near-duplicate articles
        
        Args:
            articles: List of Article objects
            threshold: Similarity threshold for duplicates
        
        Returns:
            List of duplicate groups (each group is a list of similar articles)
        """
        self.logger.info(f"Detecting duplicates among {len(articles)} articles...")
        
        embeddings = self.generate_embeddings(articles)
        similarity_matrix = cosine_similarity(embeddings)
        
        # Find duplicate groups
        duplicate_groups = []
        processed = set()
        
        for i in range(len(articles)):
            if i in processed:
                continue
            
            # Find all articles similar to this one
            similar_indices = np.where(similarity_matrix[i] >= threshold)[0]
            
            if len(similar_indices) > 1:  # More than just self
                group = [articles[idx] for idx in similar_indices]
                duplicate_groups.append(group)
                processed.update(similar_indices)
        
        self.logger.info(f"Found {len(duplicate_groups)} duplicate groups")
        return duplicate_groups
    
    def cluster_by_topic(
        self, 
        articles: List[Article], 
        n_clusters: int = None,
        method: str = 'dbscan'
    ) -> Dict[int, List[Article]]:
        """
        Cluster articles into topic groups
        
        Args:
            articles: List of Article objects
            n_clusters: Number of clusters (for K-Means)
            method: 'dbscan' or 'kmeans'
        
        Returns:
            Dictionary mapping cluster IDs to lists of articles
        """
        self.logger.info(f"Clustering {len(articles)} articles using {method}...")
        
        embeddings = self.generate_embeddings(articles)
        
        if method == 'dbscan':
            clusterer = DBSCAN(
                eps=config.DBSCAN_EPS,
                min_samples=config.DBSCAN_MIN_SAMPLES,
                metric='cosine'
            )
        elif method == 'kmeans':
            if n_clusters is None:
                n_clusters = min(10, len(articles) // 5)  # Heuristic
            clusterer = KMeans(n_clusters=n_clusters, random_state=42)
        else:
            raise ValueError(f"Unknown clustering method: {method}")
        
        cluster_labels = clusterer.fit_predict(embeddings)
        
        # Group articles by cluster
        clusters = {}
        for article, label in zip(articles, cluster_labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(article)
        
        self.logger.info(f"Created {len(clusters)} clusters")
        return clusters
