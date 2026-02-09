"""
Scraper for News First website
"""
from typing import List
from datetime import datetime
from bs4 import BeautifulSoup
from dateutil import parser as date_parser

from scrapers.base_scraper import BaseScraper
from models.article import Article


class NewsFirstScraper(BaseScraper):
    """Scraper for News First"""
    
    def parse_headlines(self, soup: BeautifulSoup) -> List[Article]:
        """Parse headlines from News First"""
        articles = []
        
        try:
            headline_elements = soup.select(self.selectors['headlines'])
            
            for element in headline_elements:
                try:
                    title = element.get_text(strip=True)
                    url = element.get('href', '')
                    
                    if url and not url.startswith('http'):
                        url = f"https://www.newsfirst.lk/{url.lstrip('/')}"
                    
                    if not title or not url:
                        continue
                    
                    timestamp = None
                    parent = element.find_parent()
                    if parent:
                        time_elem = parent.find('span', class_='date')
                        if time_elem:
                            try:
                                timestamp = date_parser.parse(time_elem.get_text())
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
