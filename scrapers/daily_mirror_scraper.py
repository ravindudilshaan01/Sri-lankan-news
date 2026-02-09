"""
Scraper for Daily Mirror news website
"""
from typing import List
from datetime import datetime
from bs4 import BeautifulSoup
from dateutil import parser as date_parser

from scrapers.base_scraper import BaseScraper
from models.article import Article


class DailyMirrorScraper(BaseScraper):
    """Scraper for Daily Mirror news"""
    
    def parse_headlines(self, soup: BeautifulSoup) -> List[Article]:
        """Parse headlines from Daily Mirror"""
        articles = []
        
        try:
            # Find all headline elements
            headline_elements = soup.select(self.selectors['headlines'])
            
            for element in headline_elements:
                try:
                    title = element.get_text(strip=True)
                    url = element.get('href', '')
                    
                    # Make URL absolute if relative
                    if url and not url.startswith('http'):
                        url = f"https://www.dailymirror.lk/{url.lstrip('/')}"
                    
                    if not title or not url:
                        continue
                    
                    # Try to find timestamp
                    timestamp = None
                    parent = element.find_parent()
                    if parent:
                        time_elem = parent.find('time')
                        if time_elem:
                            try:
                                timestamp = date_parser.parse(time_elem.get('datetime', '') or time_elem.get_text())
                            except:
                                pass
                    
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
