"""
Sri Lanka News Web Scraper and Topic Analysis System
Main application entry point
"""
import argparse
import logging
from typing import List

import config
from scrapers import AdaDeranaScraper, DailyMirrorScraper, NewsFirstScraper, ColomboGazetteScraper
from storage import DataManager
from analysis import TopicAnalyzer
from nlp import SentimentAnalyzer, EntityRecognizer, ArticleClusterer, InsightsGenerator
from models import Article

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Main")


def create_scrapers() -> List:
    """Initialize all scrapers"""
    scrapers = []
    
    for site_id, site_config in config.WEBSITES.items():
        if site_id == 'ada_derana':
            scraper = AdaDeranaScraper(**site_config)
        elif site_id == 'daily_mirror':
            scraper = DailyMirrorScraper(**site_config)
        elif site_id == 'news_first':
            scraper = NewsFirstScraper(**site_config)
        elif site_id == 'colombo_gazette':
            scraper = ColomboGazetteScraper(**site_config)
        else:
            continue
        
        scrapers.append(scraper)
    
    return scrapers


def scrape_news():
    """Scrape news from all configured websites"""
    logger.info("Starting news scraping...")
    
    scrapers = create_scrapers()
    all_articles = []
    
    for scraper in scrapers:
        try:
            articles = scraper.scrape()
            all_articles.extend(articles)
            logger.info(f"Scraped {len(articles)} articles from {scraper.name}")
            scraper.close()
        except Exception as e:
            logger.error(f"Error scraping {scraper.name}: {e}")
    
    # Save to storage
    if all_articles:
        dm = DataManager()
        dm.save_to_csv(all_articles)
        logger.info(f"Total articles scraped: {len(all_articles)}")
    else:
        logger.warning("No articles were scraped")
    
    return all_articles


def analyze_news(articles: List[Article] = None, use_transformers: bool = True):
    """Run NLP analysis on articles"""
    logger.info("Starting NLP analysis...")
    
    # Load articles if not provided
    if articles is None:
        dm = DataManager()
        articles = dm.load_from_csv()
        
        if not articles:
            logger.error("No articles found to analyze")
            return
    
    # Filter to only new articles without analysis
    articles_to_analyze = [a for a in articles if a.sentiment is None]
    
    if not articles_to_analyze:
        logger.info("All articles already analyzed")
        articles_to_analyze = articles  # Still run for reporting
    
    logger.info(f"Analyzing {len(articles_to_analyze)} articles...")
    
    # 1. Topic categorization (keyword-based)
    logger.info("Step 1/4: Categorizing topics...")
    topic_analyzer = TopicAnalyzer()
    articles_to_analyze = topic_analyzer.process_articles(articles_to_analyze)
    
    # 2. Sentiment analysis
    logger.info("Step 2/4: Analyzing sentiment...")
    sentiment_analyzer = SentimentAnalyzer(use_transformers=use_transformers)
    articles_to_analyze = sentiment_analyzer.batch_analyze(articles_to_analyze)
    
    # 3. Named entity recognition
    logger.info("Step 3/4: Extracting entities...")
    try:
        entity_recognizer = EntityRecognizer()
        articles_to_analyze = entity_recognizer.process_articles(articles_to_analyze)
    except Exception as e:
        logger.error(f"NER failed: {e}. Please install spaCy model: python -m spacy download en_core_web_sm")
    
    # 4. Article clustering (optional for large datasets)
    logger.info("Step 4/4: Clustering articles...")
    if len(articles_to_analyze) >= 10:  # Only cluster if we have enough articles
        try:
            clusterer = ArticleClusterer()
            duplicate_groups = clusterer.detect_duplicates(articles_to_analyze)
            logger.info(f"Found {len(duplicate_groups)} groups of similar articles")
        except Exception as e:
            logger.error(f"Clustering failed: {e}")
    else:
        logger.info("Not enough articles for clustering (minimum 10 required)")
    
    # Save analyzed articles
    dm = DataManager()
    dm.save_to_csv(articles_to_analyze)
    
    logger.info("NLP analysis complete")
    return articles_to_analyze


def generate_report(articles: List[Article] = None):
    """Generate insights report"""
    logger.info("Generating insights report...")
    
    # Load articles if not provided
    if articles is None:
        dm = DataManager()
        articles = dm.load_from_csv()
        
        if not articles:
            logger.error("No articles found for reporting")
            return
    
    # Generate insights
    insights_gen = InsightsGenerator()
    
    # Generate and display daily summary
    summary = insights_gen.generate_daily_summary(articles)
    print("\n" + "="*80)
    print(summary)
    print("="*80 + "\n")
    
    # Export comprehensive report
    report_json = insights_gen.export_insights(articles, format="json")
    
    with open(config.JSON_REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write(report_json)
    
    logger.info(f"Report saved to {config.JSON_REPORT_FILE}")
    
    # Display statistics
    dm = DataManager()
    stats = dm.get_statistics()
    
    print("\nOverall Statistics:")
    print(f"Total Articles: {stats['total']}")
    print(f"\nArticles by Source:")
    for source, count in stats.get('by_source', {}).items():
        print(f"  {source}: {count}")
    

def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(
        description="Sri Lanka News Web Scraper and AI/NLP Analysis System"
    )
    parser.add_argument(
        '--scrape',
        action='store_true',
        help='Scrape news from websites'
    )
    parser.add_argument(
        '--analyze',
        action='store_true',
        help='Run NLP analysis on scraped articles'
    )
    parser.add_argument(
        '--report',
        action='store_true',
        help='Generate insights report'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Run scraping, analysis, and reporting'
    )
    parser.add_argument(
        '--no-transformers',
        action='store_true',
        help='Use TextBlob instead of transformer models (faster, less accurate)'
    )
    
    args = parser.parse_args()
    
    # If no arguments, run all
    if not any([args.scrape, args.analyze, args.report, args.all]):
        args.all = True
    
    try:
        articles = None
        
        if args.all or args.scrape:
            articles = scrape_news()
        
        if args.all or args.analyze:
            use_transformers = not args.no_transformers
            articles = analyze_news(articles, use_transformers=use_transformers)
        
        if args.all or args.report:
            generate_report(articles)
        
        logger.info("All tasks completed successfully")
        
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
    except Exception as e:
        logger.error(f"Error in main: {e}", exc_info=True)


if __name__ == "__main__":
    main()
