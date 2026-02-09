"""
Generate Beautiful HTML report for news articles with enhanced UI
"""
import json
from datetime import datetime
from collections import defaultdict, Counter
from storage import DataManager
import config


def generate_html_report(output_file='reports/news_report.html'):
    """Generate an attractive interactive HTML report"""
    
    # Load data
    dm = DataManager()
    articles = dm.load_from_csv()
    
    if not articles:
        print("No articles found!")
        return
    
    # Group by source and topic
    by_source = defaultdict(list)
    by_topic = defaultdict(list)
    by_sentiment = defaultdict(list)
    
    for article in articles:
        by_source[article.source].append(article)
        by_topic[article.topic or "Other"].append(article)
        by_sentiment[article.sentiment or "neutral"].append(article)
    
    # Get latest articles (top 5)
    latest_articles = sorted(articles, key=lambda x: x.scraped_at, reverse=True)[:5]
    
    # Get trending topics
    topic_counts = Counter([a.topic or "Other" for a in articles])
    trending_topics = topic_counts.most_common(5)
    
    # Category icons
    category_icons = {
        'Politics & Government': '🏛️',
        'Economy & Business': '💼',
        'Sports': '⚽',
        'Health': '🏥',
        'Technology': '💻',
        'Entertainment': '🎬',
        'Crime & Law': '⚖️',
        'International': '🌍',
        'Education': '📚',
        'Environment': '🌱',
        'Other': '📰'
    }
    
    # Generate HTML with enhanced styling
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sri Lanka News Analysis Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #3d315b 0%, #444b6e 50%, #5a5f8d 100%);
            padding: 20px;
            line-height: 1.6;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: #ffffff;
            border-radius: 24px;
            box-shadow: 0 25px 70px rgba(0,0,0,0.4);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #3d315b 0%, #444b6e 50%, #5a5f8d 100%);
            color: white;
            padding: 50px 40px 30px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        
        .header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: repeating-linear-gradient(
                45deg,
                transparent,
                transparent 10px,
                rgba(255,255,255,0.03) 10px,
                rgba(255,255,255,0.03) 20px
            );
        }}
        
        .header h1 {{
            font-size: 3em;
            margin-bottom: 10px;
            position: relative;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            font-weight: 700;
            letter-spacing: -1px;
        }}
        
        .header .date {{
            font-size: 1.1em;
            opacity: 0.95;
            position: relative;
            font-weight: 300;
        }}
        
        .latest-news-ticker {{
            background: rgba(0,0,0,0.2);
            padding: 20px;
            margin-top: 30px;
            border-radius: 12px;
            backdrop-filter: blur(10px);
            position: relative;
        }}
        
        .latest-news-ticker h3 {{
            font-size: 1.2em;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .latest-news-ticker .news-item {{
            font-size: 0.95em;
            padding: 8px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            display: flex;
            align-items: center;
            gap: 10px;
            transition: all 0.3s;
        }}
        
        .latest-news-ticker .news-item:hover {{
            background: rgba(255,255,255,0.1);
            padding-left: 10px;
            border-radius: 8px;
        }}
        
        .latest-news-ticker .news-item a:hover {{
            text-decoration: underline !important;
        }}
        
        .latest-news-ticker .news-item:last-child {{
            border-bottom: none;
        }}
        
        .pulse {{
            display: inline-block;
            width: 8px;
            height: 8px;
            background: #22c55e;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; transform: scale(1); }}
            50% {{ opacity: 0.5; transform: scale(1.2); }}
        }}
        
        .categories-bar {{
            background: linear-gradient(to bottom, #ffffff 0%, #f8fafc 100%);
            padding: 25px 40px;
            border-bottom: 2px solid #e2e8f0;
            overflow-x: auto;
            position: sticky;
            top: 0;
            z-index: 200;
        }}
        
        .categories-bar h3 {{
            font-size: 1.1em;
            color: #1e293b;
            margin-bottom: 15px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .category-buttons {{
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }}
        
        .category-btn {{
            padding: 10px 20px;
            border: 2px solid #e2e8f0;
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border-radius: 25px;
            cursor: pointer;
            font-size: 0.9em;
            font-weight: 600;
            color: #475569;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            display: inline-flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }}
        
        .category-btn:hover {{
            transform: translateY(-3px) scale(1.05);
            background: linear-gradient(135deg, #444b6e 0%, #3d315b 100%);
            color: white;
            border-color: #444b6e;
            box-shadow: 0 5px 20px rgba(68, 75, 110, 0.4);
        }}
        
        .category-btn.active {{
            background: linear-gradient(135deg, #444b6e 0%, #3d315b 100%);
            color: white;
            border-color: #444b6e;
            box-shadow: 0 5px 20px rgba(68, 75, 110, 0.4);
        }}
        
        .category-btn .count {{
            background: rgba(0,0,0,0.15);
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 700;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 25px;
            padding: 40px;
            background: linear-gradient(to bottom, #f8fafc 0%, #ffffff 100%);
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            padding: 30px;
            border-radius: 16px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            text-align: center;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            border: 2px solid transparent;
            cursor: pointer;
        }}
        
        .stat-card:hover {{
            transform: translateY(-8px) scale(1.05) rotate(1deg);
            box-shadow: 0 15px 40px rgba(68, 75, 110, 0.3);
            border-color: #444b6e;
        }}
        
        .stat-card .number {{
            font-size: 3em;
            font-weight: 800;
            background: linear-gradient(135deg, #3d315b 0%, #5a5f8d 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 8px;
            animation: numberPop 0.5s ease;
        }}
        
        @keyframes numberPop {{
            0% {{ transform: scale(0.5); opacity: 0; }}
            50% {{ transform: scale(1.1); }}
            100% {{ transform: scale(1); opacity: 1; }}
        }}
        
        .stat-card .label {{
            color: #64748b;
            margin-top: 8px;
            font-size: 1em;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .tabs {{
            display: flex;
            background: linear-gradient(to right, #f8fafc 0%, #ffffff 100%);
            padding: 0 40px;
            border-bottom: 3px solid #e2e8f0;
            overflow-x: auto;
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        
        .tab {{
            padding: 18px 30px;
            cursor: pointer;
            border: none;
            background: none;
            font-size: 1.05em;
            color: #64748b;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            white-space: nowrap;
            font-weight: 600;
            position: relative;
        }}
        
        .tab:hover {{
            color: #444b6e;
            background: rgba(68, 75, 110, 0.08);
            transform: translateY(-2px);
        }}
        
        .tab.active {{
            color: #444b6e;
            background: linear-gradient(to bottom, rgba(68, 75, 110, 0.15) 0%, transparent 100%);
            transform: scale(1.05);
        }}
        
        .tab.active::after {{
            content: '';
            position: absolute;
            bottom: -3px;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #3d315b 0%, #5a5f8d 100%);
            box-shadow: 0 2px 10px rgba(68, 75, 110, 0.5);
        }}
        
        .content {{
            padding: 40px;
            background: #ffffff;
        }}
        
        .tab-content {{
            display: none;
            animation: fadeIn 0.5s;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        .topic-section {{
            margin-bottom: 40px;
        }}
        
        .topic-header {{
            background: linear-gradient(135deg, #3d315b 0%, #444b6e 50%, #5a5f8d 100%);
            color: white;
            padding: 20px 28px;
            border-radius: 14px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 6px 20px rgba(68, 75, 110, 0.3);
            transition: all 0.3s;
            cursor: pointer;
        }}
        
        .topic-header:hover {{
            transform: translateX(5px);
            box-shadow: 0 8px 30px rgba(68, 75, 110, 0.5);
        }}
        
        .topic-header h3 {{
            font-size: 1.5em;
            font-weight: 700;
            letter-spacing: -0.5px;
        }}
        
        .topic-count {{
            background: rgba(255,255,255,0.25);
            backdrop-filter: blur(10px);
            padding: 8px 20px;
            border-radius: 25px;
            font-size: 0.95em;
            font-weight: 700;
            border: 1px solid rgba(255,255,255,0.3);
            transition: all 0.3s;
        }}
        
        .topic-header:hover .topic-count {{
            background: rgba(255,255,255,0.35);
            transform: scale(1.1);
        }}
        
        .article-card {{
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border: 2px solid #e2e8f0;
            border-radius: 14px;
            padding: 24px;
            margin-bottom: 18px;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            overflow: hidden;
            cursor: pointer;
            display: flex;
            gap: 20px;
        }}
        
        .article-image {{
            width: 100px;
            height: 100px;
            border-radius: 10px;
            background: linear-gradient(135deg, #444b6e 0%, #5a5f8d 100%);
            flex-shrink: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2.5em;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        
        .article-content {{
            flex: 1;
        }}
        
        .article-card::before {{
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 5px;
            background: linear-gradient(to bottom, #3d315b 0%, #5a5f8d 100%);
            opacity: 0;
            transition: opacity 0.3s;
        }}
        
        .article-card:hover {{
            box-shadow: 0 10px 40px rgba(68, 75, 110, 0.25);
            transform: translateX(10px) translateY(-3px);
            border-color: #444b6e;
        }}
        
        .article-card:hover::before {{
            opacity: 1;
        }}
        
        .article-title {{
            font-size: 1.35em;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 14px;
            line-height: 1.5;
            letter-spacing: -0.3px;
        }}
        
        .article-title a {{
            color: #1e293b;
            text-decoration: none;
            transition: all 0.3s;
        }}
        
        .article-title a:hover {{
            color: #444b6e;
            text-decoration: underline;
            text-decoration-color: #444b6e;
            text-decoration-thickness: 2px;
            text-shadow: 0 2px 10px rgba(68, 75, 110, 0.2);
        }}
        
        .article-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: 14px;
            font-size: 0.95em;
            align-items: center;
        }}
        
        .badge {{
            padding: 8px 16px;
            border-radius: 25px;
            font-size: 0.9em;
            font-weight: 700;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            display: inline-flex;
            align-items: center;
            gap: 6px;
            border: 2px solid transparent;
            cursor: pointer;
        }}
        
        .badge:hover {{
            transform: scale(1.15) rotate(2deg);
        }}
        
        .badge-source {{
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
            color: #1e40af;
            border-color: #93c5fd;
        }}
        
        .badge-source:hover {{
            box-shadow: 0 5px 15px rgba(59, 130, 246, 0.4);
        }}
        
        .badge-positive {{
            background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
            color: #15803d;
            border-color: #86efac;
            font-weight: 800;
            box-shadow: 0 2px 8px rgba(34, 197, 94, 0.2);
        }}
        
        .badge-positive:hover {{
            box-shadow: 0 5px 20px rgba(34, 197, 94, 0.5);
        }}
        
        .badge-negative {{
            background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
            color: #991b1b;
            border-color: #fca5a5;
            font-weight: 800;
            box-shadow: 0 2px 8px rgba(239, 68, 68, 0.2);
        }}
        
        .badge-negative:hover {{
            box-shadow: 0 5px 20px rgba(239, 68, 68, 0.5);
        }}
        
        .badge-neutral {{
            background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
            color: #475569;
            border-color: #cbd5e1;
        }}
        
        .badge-neutral:hover {{
            box-shadow: 0 5px 15px rgba(71, 85, 105, 0.3);
        }}
        
        .entities {{
            margin-top: 14px;
            padding: 14px;
            background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%);
            border-radius: 10px;
            font-size: 0.92em;
            border-left: 4px solid #444b6e;
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.05);
        }}
        
        .entity-type {{
            display: inline-block;
            margin-right: 18px;
            margin-bottom: 6px;
        }}
        
        .entity-label {{
            font-weight: 800;
            color: #444b6e;
            text-transform: uppercase;
            font-size: 0.85em;
            letter-spacing: 0.5px;
        }}
        
        .entity-values {{
            color: #3d315b;
            font-weight: 600;
            margin-left: 4px;
        }}
        
        .filter-bar {{
            background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
            padding: 24px;
            border-radius: 14px;
            margin-bottom: 30px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.06);
            border: 2px solid #e2e8f0;
            transition: all 0.3s;
        }}
        
        .filter-bar:hover {{
            box-shadow: 0 6px 25px rgba(68, 75, 110, 0.15);
            border-color: #444b6e;
        }}
        
        .filter-bar input {{
            width: 100%;
            padding: 16px 24px;
            border: 2px solid #cbd5e1;
            border-radius: 30px;
            font-size: 1.05em;
            transition: all 0.3s;
            background: white;
            font-weight: 500;
        }}
        
        .filter-bar input:focus {{
            outline: none;
            border-color: #444b6e;
            box-shadow: 0 0 0 4px rgba(68, 75, 110, 0.1);
            transform: scale(1.02);
        }}
        
        .section-title {{
            font-size: 1.8em;
            font-weight: 800;
            color: #1e293b;
            margin-bottom: 24px;
            padding-bottom: 12px;
            border-bottom: 3px solid #444b6e;
            display: inline-block;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2em;
            }}
            
            .stats {{
                grid-template-columns: repeat(2, 1fr);
                padding: 25px;
                gap: 15px;
            }}
            
            .tabs {{
                padding: 0 15px;
            }}
            
            .content {{
                padding: 20px;
            }}
            
            .article-card {{
                padding: 18px;
                flex-direction: column;
            }}
            
            .article-image {{
                width: 80px;
                height: 80px;
                font-size: 2em;
            }}
            
            .category-buttons {{
                overflow-x: auto;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Sri Lanka News Analysis</h1>
            <p class="date">Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            
            <div class="latest-news-ticker">
                <h3><span class="pulse"></span> Latest News Updates</h3>
"""
    
    # Add latest news items
    for article in latest_articles:
        sentiment_emoji = {"positive": "✅", "negative": "⚠️", "neutral": "📄"}.get(article.sentiment, "📄")
        # Create a hook headline - first 35 chars max for impact
        hook = article.title[:35].strip()
        if len(article.title) > 35:
            # Cut at last word boundary for clean hook
            hook = hook.rsplit(' ', 1)[0] + '...'
        html += f"""                <div class="news-item">
                    <span>{sentiment_emoji}</span>
                    <a href="{article.url}" target="_blank" style="color: white; text-decoration: none; flex: 1;">{hook}</a>
                </div>
"""
    
    html += """            </div>
        </div>
        
        <div class="categories-bar">
            <h3>📂 Browse by Category</h3>
            <div class="category-buttons">
                <button class="category-btn active" onclick="filterByCategory('all')">
                    <span>🌐 All Categories</span>
                    <span class="count">""" + str(len(articles)) + """</span>
                </button>
"""
    
    # Add category buttons
    for topic, count in sorted(by_topic.items(), key=lambda x: len(x[1]), reverse=True):
        icon = category_icons.get(topic, '📰')
        html += f"""                <button class="category-btn" onclick="filterByCategory('{topic.lower()}')">
                    <span>{icon} {topic}</span>
                    <span class="count">{len(by_topic[topic])}</span>
                </button>
"""
    
    html += """            </div>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="number">""" + str(len(articles)) + """</div>
                <div class="label">Total Articles</div>
            </div>
            <div class="stat-card">
                <div class="number">""" + str(len(by_source)) + """</div>
                <div class="label">News Sources</div>
            </div>
            <div class="stat-card">
                <div class="number">""" + str(len(by_topic)) + """</div>
                <div class="label">Topics</div>
            </div>
            <div class="stat-card">
                <div class="number">""" + str(len(by_sentiment.get('positive', []))) + """</div>
                <div class="label">Positive News</div>
            </div>
        </div>
        
        <div class="tabs">
            <button class="tab active" onclick="showTab('all')">📰 All Articles</button>
            <button class="tab" onclick="showTab('topics')">📁 By Topic</button>
            <button class="tab" onclick="showTab('sources')">🌐 By Source</button>
            <button class="tab" onclick="showTab('sentiment')">😊 By Sentiment</button>
        </div>
        
        <div class="content">
            <div class="filter-bar">
                <input type="text" id="searchBox" placeholder="🔍 Search articles by title, source, or topic..." onkeyup="filterArticles()">
            </div>
            
            <!-- All Articles Tab -->
            <div id="all" class="tab-content active">
                <h2 class="section-title">All Articles (""" + str(len(articles)) + """)</h2>
                <div class="articles-list">
"""
    
    # Add all articles
    for article in sorted(articles, key=lambda x: x.scraped_at, reverse=True):
        sentiment_class = f"badge-{article.sentiment}" if article.sentiment else "badge-neutral"
        sentiment_emoji = {"positive": "✅", "negative": "⚠️", "neutral": "📄"}.get(article.sentiment, "📄")
        
        # Shorten title for display
        display_title = article.title
        if len(article.title) > 100:
            display_title = article.title[:100].rsplit(' ', 1)[0] + '...'
        
        entities_html = ""
        if article.entities:
            entities_parts = []
            for ent_type, ent_list in article.entities.items():
                if ent_list:
                    entities_parts.append(f'<span class="entity-type"><span class="entity-label">{ent_type}:</span> <span class="entity-values">{", ".join(ent_list[:3])}</span></span>')
            if entities_parts:
                entities_html = f'<div class="entities">🏷️ {" ".join(entities_parts)}</div>'
        
        html += f"""
                    <div class="article-card" data-title="{article.title.lower()}" data-source="{article.source.lower()}" data-topic="{(article.topic or 'Other').lower()}" data-category="{(article.topic or 'Other').lower()}">
                        <div class="article-image">{category_icons.get(article.topic or 'Other', '📰')}</div>
                        <div class="article-content">
                            <div class="article-title">
                                <a href="{article.url}" target="_blank">{display_title}</a>
                            </div>
                            <div class="article-meta">
                                <span class="badge badge-source">📰 {article.source}</span>
                                <span class="badge {sentiment_class}">{sentiment_emoji} {(article.sentiment or 'neutral').upper()}</span>
                                <span style="color: #64748b; font-weight: 600;">{category_icons.get(article.topic or 'Other', '📰')} {article.topic or 'Other'}</span>
                            </div>
                            {entities_html}
                        </div>
                    </div>
"""
    
    html += """
                </div>
            </div>
            
            <!-- By Topic Tab -->
            <div id="topics" class="tab-content">
"""
    
    # Add articles by topic
    for topic, topic_articles in sorted(by_topic.items(), key=lambda x: len(x[1]), reverse=True):
        icon = category_icons.get(topic, '📰')
        html += f"""
                <div class="topic-section">
                    <div class="topic-header">
                        <h3>{icon} {topic}</h3>
                        <span class="topic-count">{len(topic_articles)} articles</span>
                    </div>
"""
        
        for article in topic_articles[:10]:
            sentiment_class = f"badge-{article.sentiment}" if article.sentiment else "badge-neutral"
            sentiment_emoji = {"positive": "✅", "negative": "⚠️", "neutral": "📄"}.get(article.sentiment, "📄")
            
            # Shorten title for display
            display_title = article.title
            if len(article.title) > 100:
                display_title = article.title[:100].rsplit(' ', 1)[0] + '...'
            
            html += f"""
                    <div class="article-card">
                        <div class="article-image">{icon}</div>
                        <div class="article-content">
                            <div class="article-title">
                                <a href="{article.url}" target="_blank">{display_title}</a>
                            </div>
                            <div class="article-meta">
                                <span class="badge badge-source">📰 {article.source}</span>
                                <span class="badge {sentiment_class}">{sentiment_emoji} {(article.sentiment or 'neutral').upper()}</span>
                            </div>
                        </div>
                    </div>
"""
        
        html += """
                </div>
"""
    
    html += """
            </div>
            
            <!-- By Source Tab -->
            <div id="sources" class="tab-content">
"""
    
    # Add articles by source
    for source, source_articles in sorted(by_source.items(), key=lambda x: len(x[1]), reverse=True):
        html += f"""
                <div class="topic-section">
                    <div class="topic-header">
                        <h3>🌐 {source}</h3>
                        <span class="topic-count">{len(source_articles)} articles</span>
                    </div>
"""
        
        for article in source_articles[:15]:
            sentiment_class = f"badge-{article.sentiment}" if article.sentiment else "badge-neutral"
            sentiment_emoji = {"positive": "✅", "negative": "⚠️", "neutral": "📄"}.get(article.sentiment, "📄")
            
            # Shorten title for display
            display_title = article.title
            if len(article.title) > 100:
                display_title = article.title[:100].rsplit(' ', 1)[0] + '...'
            
            html += f"""
                    <div class="article-card">
                        <div class="article-image">{category_icons.get(article.topic or 'Other', '📰')}</div>
                        <div class="article-content">
                            <div class="article-title">
                                <a href="{article.url}" target="_blank">{display_title}</a>
                            </div>
                            <div class="article-meta">
                                <span class="badge {sentiment_class}">{sentiment_emoji} {(article.sentiment or 'neutral').upper()}</span>
                                <span style="color: #64748b; font-weight: 600;">{category_icons.get(article.topic or 'Other', '📰')} {article.topic or 'Other'}</span>
                            </div>
                        </div>
                    </div>
"""
        
        html += """
                </div>
"""
    
    html += """
            </div>
            
            <!-- By Sentiment Tab -->
            <div id="sentiment" class="tab-content">
"""
    
    # Add articles by sentiment
    for sentiment in ['positive', 'negative', 'neutral']:
        sentiment_articles = by_sentiment.get(sentiment, [])
        if sentiment_articles:
            sentiment_emoji = {"positive": "✅ POSITIVE", "negative": "⚠️ NEGATIVE", "neutral": "📄 NEUTRAL"}.get(sentiment, sentiment)
            
            html += f"""
                <div class="topic-section">
                    <div class="topic-header">
                        <h3>{sentiment_emoji}</h3>
                        <span class="topic-count">{len(sentiment_articles)} articles</span>
                    </div>
"""
            
            for article in sentiment_articles[:15]:
                # Shorten title for display
                display_title = article.title
                if len(article.title) > 100:
                    display_title = article.title[:100].rsplit(' ', 1)[0] + '...'
                
                html += f"""
                    <div class="article-card">
                        <div class="article-image">{category_icons.get(article.topic or 'Other', '📰')}</div>
                        <div class="article-content">
                            <div class="article-title">
                                <a href="{article.url}" target="_blank">{display_title}</a>
                            </div>
                            <div class="article-meta">
                                <span class="badge badge-source">📰 {article.source}</span>
                                <span style="color: #64748b; font-weight: 600;">{category_icons.get(article.topic or 'Other', '📰')} {article.topic or 'Other'}</span>
                            </div>
                        </div>
                    </div>
"""
            
            html += """
                </div>
"""
    
    html += """
            </div>
        </div>
    </div>
    
    <script>
        function showTab(tabName) {
            const contents = document.querySelectorAll('.tab-content');
            contents.forEach(content => content.classList.remove('active'));
            
            const tabs = document.querySelectorAll('.tab');
            tabs.forEach(tab => tab.classList.remove('active'));
            
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }
        
        function filterArticles() {
            const searchText = document.getElementById('searchBox').value.toLowerCase();
            const articles = document.querySelectorAll('.article-card');
            
            articles.forEach(article => {
                const title = article.getAttribute('data-title') || '';
                const source = article.getAttribute('data-source') || '';
                const topic = article.getAttribute('data-topic') || '';
                
                if (title.includes(searchText) || source.includes(searchText) || topic.includes(searchText)) {
                    article.style.display = 'flex';
                } else {
                    article.style.display = 'none';
                }
            });
        }
        
        function filterByCategory(category) {
            const articles = document.querySelectorAll('.article-card');
            const buttons = document.querySelectorAll('.category-btn');
            
            // Update active button
            buttons.forEach(btn => btn.classList.remove('active'));
            event.target.closest('.category-btn').classList.add('active');
            
            // Filter articles
            articles.forEach(article => {
                const articleCategory = article.getAttribute('data-category') || '';
                
                if (category === 'all' || articleCategory === category) {
                    article.style.display = 'flex';
                } else {
                    article.style.display = 'none';
                }
            });
        }
    </script>
</body>
</html>
"""
    
    # Save HTML file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ HTML report generated: {output_file}")
    return output_file


if __name__ == "__main__":
    generate_html_report()
