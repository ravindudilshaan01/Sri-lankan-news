"""Scrapers package"""
from .base_scraper import BaseScraper
from .ada_derana_scraper import AdaDeranaScraper
from .daily_mirror_scraper import DailyMirrorScraper
from .news_first_scraper import NewsFirstScraper
from .colombo_gazette_scraper import ColomboGazetteScraper

__all__ = [
    'BaseScraper',
    'AdaDeranaScraper',
    'DailyMirrorScraper',
    'NewsFirstScraper',
    'ColomboGazetteScraper'
]
