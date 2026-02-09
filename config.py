"""
Central configuration for the Sri Lanka News Scraper
"""
import os

# Project paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

# Scraping settings
RATE_LIMIT_DELAY = 3  # seconds between requests
REQUEST_TIMEOUT = 15  # seconds
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

# User-Agent rotation list
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
]

# Target websites configuration
WEBSITES = {
    'ada_derana': {
        'name': 'Ada Derana',
        'url': 'https://www.adaderana.lk/news.php',
        'selectors': {
            'headlines': 'li a[href*="/news/"]',
            'timestamp': 'time',
            'category': 'span.category'
        }
    },
    'daily_mirror': {
        'name': 'Daily Mirror',
        'url': 'https://www.dailymirror.lk/',
        'selectors': {
            'headlines': 'h3.title a, h2.entry-title a, div.col_item_mid h4 a, h4 a',
            'timestamp': 'time.entry-date',
            'category': 'span.cat-links a'
        }
    },
    'news_first': {
        'name': 'News First',
        'url': 'https://www.newsfirst.lk/',
        'selectors': {
            'headlines': 'div.ng-star-inserted a[href^="/2026"]',
            'timestamp': 'span.date',
            'category': 'span.category'
        }
    },
    'colombo_gazette': {
        'name': 'Colombo Gazette',
        'url': 'https://colombogazette.com/',
        'selectors': {
            'headlines': 'div.grid a[href*="/2026/"]',
            'timestamp': 'time.entry-date',
            'category': 'span.cat-links a'
        }
    }
}

# Topic categories and keywords
TOPIC_KEYWORDS = {
    'Politics & Government': [
        'parliament', 'minister', 'president', 'government', 'election', 
        'political', 'cabinet', 'pm', 'prime minister', 'opposition', 
        'mp', 'politician', 'party', 'vote', 'democracy'
    ],
    'Economy & Business': [
        'economy', 'business', 'trade', 'export', 'import', 'rupee', 
        'inflation', 'gdp', 'investment', 'stock', 'market', 'financial',
        'bank', 'economic', 'revenue', 'budget', 'tax', 'debt'
    ],
    'Sports': [
        'cricket', 'football', 'rugby', 'sports', 'match', 'tournament',
        'player', 'team', 'victory', 'championship', 'game', 'athlete',
        'coach', 'score', 'win', 'trophy'
    ],
    'Health': [
        'health', 'hospital', 'doctor', 'medical', 'disease', 'covid',
        'pandemic', 'vaccine', 'treatment', 'patient', 'medicine',
        'healthcare', 'clinic', 'virus', 'infection'
    ],
    'Technology': [
        'technology', 'tech', 'digital', 'internet', 'software', 'app',
        'computer', 'mobile', 'cyber', 'ai', 'artificial intelligence',
        'data', 'online', 'innovation'
    ],
    'Entertainment': [
        'film', 'movie', 'cinema', 'actor', 'actress', 'music', 'singer',
        'entertainment', 'celebrity', 'concert', 'festival', 'culture',
        'art', 'theatre', 'drama'
    ],
    'Crime & Law': [
        'crime', 'police', 'arrest', 'court', 'judge', 'law', 'justice',
        'murder', 'theft', 'fraud', 'investigation', 'suspect', 'jail',
        'prison', 'criminal', 'lawyer', 'legal'
    ],
    'International': [
        'international', 'world', 'global', 'foreign', 'diplomatic',
        'embassy', 'united nations', 'india', 'china', 'usa', 'uk',
        'country', 'abroad', 'treaty', 'relations'
    ],
    'Education': [
        'education', 'school', 'university', 'student', 'teacher',
        'exam', 'academic', 'college', 'learning', 'course'
    ],
    'Environment': [
        'environment', 'climate', 'weather', 'flood', 'drought',
        'pollution', 'wildlife', 'nature', 'conservation', 'disaster'
    ]
}

# NLP settings
SENTIMENT_MODEL = 'distilbert-base-uncased-finetuned-sst-2-english'  # Hugging Face model
SPACY_MODEL = 'en_core_web_sm'
SENTENCE_TRANSFORMER_MODEL = 'all-MiniLM-L6-v2'

# Clustering settings
SIMILARITY_THRESHOLD = 0.75  # for duplicate detection
MIN_CLUSTER_SIZE = 2
DBSCAN_EPS = 0.3
DBSCAN_MIN_SAMPLES = 2

# Data files
NEWS_DATA_FILE = os.path.join(DATA_DIR, 'news_articles.csv')
ENTITIES_FILE = os.path.join(DATA_DIR, 'extracted_entities.json')
CLUSTERS_FILE = os.path.join(DATA_DIR, 'article_clusters.json')

# Report settings
REPORT_FILE = os.path.join(REPORTS_DIR, 'latest_report.html')
JSON_REPORT_FILE = os.path.join(REPORTS_DIR, 'latest_report.json')
