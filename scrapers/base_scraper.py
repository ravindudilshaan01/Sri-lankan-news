"""
Base scraper class with common functionality
"""
import time
import random
import logging
from abc import ABC, abstractmethod
from typing import List, Optional
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from models.article import Article
import config


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class BaseScraper(ABC):
    """Abstract base class for news scrapers"""
    
    def __init__(self, name: str, url: str, selectors: dict):
        self.name = name
        self.url = url
        self.selectors = selectors
        self.logger = logging.getLogger(f"Scraper.{name}")
        self.session = self._create_session()
        self.robots_allowed = self._check_robots_txt()
    
    def _create_session(self) -> requests.Session:
        """Create a session with retry logic"""
        session = requests.Session()
        
        # Retry strategy
        retry = Retry(
            total=config.MAX_RETRIES,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        return session
    
    def _get_user_agent(self) -> str:
        """Get a random user agent"""
        return random.choice(config.USER_AGENTS)
    
    def _check_robots_txt(self) -> bool:
        """
        Check if scraping is allowed by robots.txt
        For now, returns True - in production, parse robots.txt
        """
        try:
            robots_url = urljoin(self.url, '/robots.txt')
            response = self.session.get(robots_url, timeout=5)
            
            # Simple check - if robots.txt exists and doesn't explicitly disallow
            # In a real implementation, use robotparser module
            if response.status_code == 200:
                self.logger.info(f"robots.txt found for {self.name}, proceeding with caution")
            
            return True  # Simplified - always allow for this project
        except Exception as e:
            self.logger.warning(f"Could not check robots.txt: {e}")
            return True
    
    def rate_limit(self):
        """Implement rate limiting between requests"""
        delay = config.RATE_LIMIT_DELAY + random.uniform(0, 1)  # Add randomness
        self.logger.debug(f"Rate limiting: waiting {delay:.2f} seconds")
        time.sleep(delay)
    
    def fetch_page(self, url: Optional[str] = None) -> Optional[BeautifulSoup]:
        """Fetch and parse a webpage"""
        target_url = url or self.url
        
        if not self.robots_allowed:
            self.logger.warning(f"Scraping not allowed by robots.txt for {self.name}")
            return None
        
        try:
            headers = {'User-Agent': self._get_user_agent()}
            self.logger.info(f"Fetching {target_url}")
            
            response = self.session.get(
                target_url,
                headers=headers,
                timeout=config.REQUEST_TIMEOUT
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            self.logger.info(f"Successfully fetched {target_url}")
            return soup
            
        except requests.RequestException as e:
            self.logger.error(f"Error fetching {target_url}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error parsing {target_url}: {e}")
            return None
    
    @abstractmethod
    def parse_headlines(self, soup: BeautifulSoup) -> List[Article]:
        """
        Parse headlines from the page
        Must be implemented by subclasses
        """
        pass
    
    def scrape(self) -> List[Article]:
        """Main scraping method"""
        self.logger.info(f"Starting scrape for {self.name}")
        
        # Rate limit before fetching
        self.rate_limit()
        
        # Fetch page
        soup = self.fetch_page()
        if soup is None:
            self.logger.error(f"Failed to fetch page for {self.name}")
            return []
        
        # Parse headlines
        articles = self.parse_headlines(soup)
        self.logger.info(f"Scraped {len(articles)} articles from {self.name}")
        
        return articles
    
    def close(self):
        """Close the session"""
        self.session.close()
