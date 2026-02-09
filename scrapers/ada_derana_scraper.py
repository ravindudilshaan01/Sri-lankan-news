"""
Scraper for Ada Derana news website
"""
from typing import List
from datetime import datetime
from bs4 import BeautifulSoup
from dateutil import parser as date_parser

from scrapers.base_scraper import BaseScraper
from models.article import Article


class AdaDeranaScraper(BaseScraper):
    """Scraper for Ada Derana news"""
    
    def parse_headlines(self, soup: BeautifulSoup) -> List[Article]:
        """Parse headlines from Ada Derana"""
        articles = []
        
        try:
            # Find all headline elements
            headline_elements = soup.select(self.selectors['headlines'])
            
            for element in headline_elements:
                try:
                    # Extract title and URL
                    title = element.get_text(strip=True)
                    url = element.get('href', '')
                    
                    # Make URL absolute if relative
                    if url and not url.startswith('http'):
                        url = f"https://www.adaderana.lk/{url.lstrip('/')}"
                    
                    # Skip if no title or URL
                    if not title or not url:
                        continue
                    
                    # Try to find timestamp (optional)
                    timestamp = None
                    parent = element.find_parent()
                    if parent:
                        time_elem = parent.find('time')
                        if time_elem:
                            try:
                                timestamp = date_parser.parse(time_elem.get('datetime', ''))
                            except:
                                pass
                    
                    # Create article
                    article = Article(
                        title=title,
                        url=url,
                        source=self.name,
                        timestamp=timestamp
                    )
                    articles.append(article)
                    
                except Exception as e:
                    self.logger.warning(f"Error parsing individual headline: {e}")
                    continue
            
        except Exception as e:
            self.logger.error(f"Error parsing headlines from {self.name}: {e}")
        
        return articles
