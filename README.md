# Sri Lanka News Risk Analyst Agent 🧠

An AI-powered risk analysis system that transforms news scraping into actionable intelligence. Built with the **ReAct (Reasoning + Acting)** pattern, this agent doesn't just collect news—it **thinks**, **analyzes**, and **recommends actions**.

Perfect for demonstrating AI agent development skills for roles in **risk intelligence, compliance, and security analysis** (e.g., Exiger, Deloitte Risk, etc.).

## 🚀 What's New: From Scraper to AI Agent

**Before**: Simple scraper that collected news → saved to CSV
**Now**: Intelligent agent that follows: **Scrape → THINK → ANALYZE → ACT**

### Key Features

### 🧠 **AI Risk Analysis Agent**
- **ReAct Pattern**: Agent reasons step-by-step (Thought → Action → Observation)
- **15+ Risk Categories**: Political instability, corruption, cyber threats, economic crisis, etc.
- **LLM Integration**: Uses GPT-4 for deep analysis (with keyword-based fallback)
- **Intelligent Reasoning**: Shows complete thought process and decision-making
- **Actionable Intelligence**: Recommends specific actions (escalate, monitor, investigate)
- **Executive Summaries**: High-level risk landscape overview

### 🌐 **Web Scraping**
- Scrapes news from 4 major Sri Lankan news websites:
  - Ada Derana
  - Daily Mirror
  - News First
  - Colombo Gazette
- Ethical scraping with rate limiting and robots.txt compliance
- Automatic retry logic and error handling
- Duplicate detection and deduplication

### 🤖 **AI/NLP Analysis**
- **Sentiment Analysis**: Determine if headlines are positive, negative, or neutral using TextBlob or transformer models
- **Named Entity Recognition (NER)**: Extract people, organizations, and locations using spaCy
- **Article Clustering**: Group similar articles and detect duplicates using Sentence-Transformers
- **Topic Categorization**: Classify articles into 10 predefined categories
- **Trend Analysis**: Identify breaking trends and most-mentioned entities
- **Insights Generation**: Create automated daily summaries and source comparisons

## Installation

### Prerequisites
- Python 3.8 or higher
- 8GB RAM recommended for NLP features
- (Optional) GPU for faster transformer models
- (Optional) OpenAI API key for LLM-powered risk analysis

### Step 1: Clone or Download
Download this project to your machine.

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Download NLP Models
```bash
# Download spaCy English model (required for NER)
python -m spacy download en_core_web_sm
```

### Step 5: (Optional) Setup OpenAI for LLM Analysis
```bash
# Windows PowerShell
$env:OPENAI_API_KEY="your-api-key-here"

# Linux/Mac
export OPENAI_API_KEY="your-api-key-here"
```

**Note**: Sentence-Transformer models (~400MB) will be downloaded automatically on first use.

## Usage

### 🆕 Risk Analysis Agent (NEW!)

#### Basic Risk Analysis (No API Key Required)
```bash
# Scrape news and run keyword-based risk analysis
python main.py --scrape --risk
```

#### Advanced AI Risk Analysis (Requires OpenAI API)
```bash
# Use GPT-4 for deep reasoning and analysis
python main.py --scrape --risk --use-llm
```

#### Run Everything (Recommended)
```bash
# Scrape, analyze, risk assessment, and report
python main.py --all
```

#### Try the Example
```bash
# See the agent in action with sample data
python example_agent_usage.py
```

### Traditional NLP Analysis

#### Quick Start - Run Everything
```bash
python main.py --all
```

This will:
1. Scrape news from all websites
2. Run NLP analysis (sentiment, entities, topics)
3. **Run AI risk analysis with ReAct agent** 🆕
4. Generate insights report

### Individual Commands

#### Scrape News Only
```bash
python main.py --scrape
```

#### Analyze Existing Data
```bash
python main.py --analyze
```

#### Risk Analysis Only
```bash
python main.py --risk --use-llm
```

#### Generate Report Only
```bash
python main.py --report
```

#### Use Fast Mode (TextBlob instead of transformers)
```bash
python main.py --all --no-transformers
```

## 📊 Output Examples

### Risk Analysis Report
```json
{
  "article_title": "Mass protests erupt over economic crisis",
  "risk_level": "High",
  "risk_categories": ["Civil Unrest", "Economic Crisis", "Political Instability"],
  "confidence": 0.85,
  "recommended_actions": [
    "⚠️ MONITOR: Set up continuous monitoring",
    "🔍 INVESTIGATE: Gather additional intelligence",
    "📋 Document for compliance review"
  ],
  "reasoning_trace": [
    {
      "thought": "Analyzing article for risk indicators...",
      "action": "ANALYZE_WITH_LLM",
      "observation": "Found multiple high-severity risk factors"
    }
  ]
}
```

### Executive Summary
```
🎯 RISK ANALYSIS SUMMARY
Total Articles Analyzed: 45
🚨 Risk Distribution:
   Critical: 2  |  High: 8  |  Medium: 15  |  Low: 12
🔝 Top Risk Categories:
   Economic Crisis: 12  |  Political Instability: 9  |  Civil Unrest: 7
⚠️ High Priority Articles: 10
```

## Project Structure

```
News/
├── main.py                     # Main application entry point
├── config.py                   # Central configuration
├── requirements.txt            # Python dependencies
├── AGENT_GUIDE.md             # 🆕 Beginner's guide to the agent
├── example_agent_usage.py     # 🆕 Example agent usage
│
├── agent/                     # 🆕 AI Risk Analyst Agent
│   ├── __init__.py
│   ├── risk_agent.py          # Main agent with LLM integration
│   ├── react_loop.py          # ReAct reasoning pattern
│   └── risk_categories.py     # Risk types and assessment
│
├── models/                     # Data models
│   ├── __init__.py
│   └── article.py              # Article data class
│
├── scrapers/                   # Web scraping modules
│   ├── __init__.py
│   ├── base_scraper.py         # Base scraper class
│   ├── ada_derana_scraper.py
│   ├── daily_mirror_scraper.py
│   ├── news_first_scraper.py
│   └── colombo_gazette_scraper.py
│
├── storage/                    # Data persistence
│   ├── __init__.py
│   └── data_manager.py         # CSV storage manager
│
├── analysis/                   # Topic analysis
│   ├── __init__.py
│   └── topic_analyzer.py       # Keyword-based categorization
│
├── nlp/                        # NLP/ML modules
│   ├── __init__.py
│   ├── sentiment_analyzer.py   # Sentiment analysis
│   ├── entity_recognizer.py    # Named entity recognition
│   ├── article_clusterer.py    # Similarity & clustering
│   └── insights_generator.py   # Report generation
│
├── data/                       # Scraped data (created automatically)
│   └── news_articles.csv
│
└── reports/                    # Generated reports (created automatically)
    ├── latest_report.json
    └── risk_analysis_report.json  # 🆕 AI risk analysis
```

## Configuration

Edit `config.py` to customize:

- **Scraping settings**: Rate limits, timeouts, user agents
- **Website configurations**: URLs and CSS selectors
- **Topic keywords**: Categories and associated keywords
- **NLP settings**: Model names and clustering parameters

## Topic Categories

Articles are automatically categorized into:
- Politics & Government
- Economy & Business
- Sports
- Health
- Technology
- Entertainment
- Crime & Law
- International
- Education
- Environment

## Output Files

### CSV Data File
`data/news_articles.csv` - Contains all scraped articles with analysis results

Columns:
- title, url, source, timestamp
- sentiment, sentiment_score
- entities (JSON), topic
- scraped_at

### JSON Report
`reports/latest_report.json` - Comprehensive insights report including:
- Daily summary
- Breaking trends
- Source comparison
- Topic distribution

## Ethical Scraping Guidelines

This project follows ethical web scraping practices:

✅ **Respect robots.txt**: Checks website policies
✅ **Rate limiting**: 3-second delay between requests
✅ **User-Agent rotation**: Identifies as a bot responsibly
✅ **Error handling**: Fails gracefully without overwhelming servers
✅ **No personal data**: Only collects public news headlines

**Important**: Always review target websites' Terms of Service before scraping.

## Performance Tips

### For Faster Analysis (Lower Accuracy)
```bash
python main.py --all --no-transformers
```
Uses TextBlob instead of transformer models - runs on any system.

### For Better Accuracy (Slower)
```bash
python main.py --all
```
Uses state-of-the-art transformer models - requires more RAM/time.

### GPU Acceleration
If you have a CUDA-capable GPU, transformer models will automatically use it for 5-10x speedup.

## Troubleshooting

### "spaCy model not found"
```bash
python -m spacy download en_core_web_sm
```

### "Out of memory" errors
- Use `--no-transformers` flag
- Process fewer articles at once
- Close other applications

### Scraping returns 0 articles
- Check your internet connection
- Website structure may have changed (update selectors in `config.py`)
- Rate limiting may be too aggressive

## Example Output

```
Daily News Summary - 2026-02-05
Total Articles Analyzed: 45

Politics & Government (12 articles):
  1. Parliament passes new economic reform bill 📈
     Source: Ada Derana
  2. Prime Minister addresses nation on inflation 📉
     Source: Daily Mirror
  ...

Sports (8 articles):
  1. Sri Lanka cricket team wins series 📈
     Source: News First
  ...
```

## Future Enhancements

- [ ] Add more news sources
- [ ] Implement advanced topic modeling (BERTopic)
- [ ] Create web dashboard for visualization
- [ ] Add email notifications for breaking news
- [ ] Multi-language support (Sinhala, Tamil)
- [ ] Scheduled automated scraping

## License

This project is for educational purposes. Please respect website Terms of Service and copyright laws.

## Contributing

Contributions welcome! Please:
1. Test scrapers with live websites
2. Document any changes to selectors
3. Follow existing code style

## Contact

For questions or issues, please create an issue in this repository.

---

**Made with ❤️ for Sri Lankan news analysis**
