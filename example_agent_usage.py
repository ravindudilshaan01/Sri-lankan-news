"""
Example: How to Use the Risk Analyst Agent
Run this file directly to see the agent in action
"""
import logging
from models import Article
from agent import RiskAnalystAgent

logging.basicConfig(level=logging.INFO)

# Create sample news articles
sample_articles = [
    Article(
        title="Mass Protests Erupt in Colombo Over Rising Inflation",
        url="https://example.com/article1",
        source="Daily Mirror",
        description="Thousands took to the streets today as inflation reached 50%, "
                   "with protesters demanding government resignation and economic reforms. "
                   "Police used tear gas to disperse crowds near the presidential palace.",
        timestamp="2024-02-09 10:30:00"
    ),
    Article(
        title="Tech Startup Raises $10M in Series A Funding",
        url="https://example.com/article2",
        source="Tech News",
        description="Local software company SecureTech announced a successful Series A "
                   "funding round led by international investors, marking positive growth "
                   "in Sri Lanka's technology sector.",
        timestamp="2024-02-09 11:00:00"
    ),
    Article(
        title="Corruption Allegations Surface Against Minister",
        url="https://example.com/article3",
        source="News First",
        description="Opposition parties filed a formal complaint alleging the Finance Minister "
                   "received kickbacks from a major infrastructure project. The minister denies "
                   "all charges and calls it a political attack.",
        timestamp="2024-02-09 12:15:00"
    ),
]


def main():
    print("\n" + "="*80)
    print("🤖 Risk Analyst Agent - Example Run")
    print("="*80 + "\n")
    
    # Initialize agent (without LLM for this example)
    print("Initializing Risk Analyst Agent...")
    agent = RiskAnalystAgent(use_local_analysis=True)
    
    print(f"\nAnalyzing {len(sample_articles)} sample articles...\n")
    
    # Analyze each article
    assessments = []
    for i, article in enumerate(sample_articles, 1):
        print(f"\n{'─'*80}")
        print(f"📰 Article {i}: {article.title}")
        print(f"{'─'*80}")
        
        # Run risk analysis
        assessment = agent.analyze_article(article)
        assessments.append(assessment)
        
        # Display results
        print(f"\n🎯 RISK LEVEL: {assessment.risk_level.value}")
        print(f"📊 CONFIDENCE: {assessment.confidence * 100:.0f}%")
        print(f"\n📋 Risk Categories:")
        for category in assessment.risk_categories:
            print(f"   - {category.value}")
        
        print(f"\n💡 Recommended Actions:")
        for action in assessment.recommended_actions:
            print(f"   {action}")
        
        print(f"\n🧠 Reasoning:")
        print(f"   {assessment.reasoning}")
        
        # Show reasoning trace if available
        if hasattr(assessment, 'reasoning_trace') and assessment.reasoning_trace:
            print(f"\n🔍 Agent Reasoning Trace:")
            for step in assessment.reasoning_trace:
                print(f"\n   Step {step['step'] + 1}:")
                print(f"   💭 Thought: {step['thought'][:80]}...")
                print(f"   🎯 Action: {step['action'][:80]}...")
                print(f"   👁️ Observation: {step['observation'][:80]}...")
    
    # Generate summary
    print("\n\n" + "="*80)
    print("📊 EXECUTIVE SUMMARY")
    print("="*80)
    
    summary = agent.generate_summary_report(assessments)
    
    print(f"\nTotal Articles: {summary['total_articles_analyzed']}")
    print(f"\n🚨 Risk Distribution:")
    for level, count in summary['risk_distribution'].items():
        print(f"   {level}: {count}")
    
    print(f"\n🔝 Top Risk Categories:")
    for category, count in summary['top_risk_categories']:
        print(f"   {category}: {count}")
    
    print(f"\n⚠️ High Priority Items: {summary['high_priority_count']}")
    print(f"📈 Average Confidence: {summary['average_confidence'] * 100:.1f}%")
    
    print("\n" + "="*80)
    print("✅ Analysis Complete!")
    print("="*80 + "\n")
    
    print("💡 To use with OpenAI LLM:")
    print("   1. Set environment variable: OPENAI_API_KEY=your-key")
    print("   2. Change: RiskAnalystAgent(use_local_analysis=False)")
    print("   3. Run again for deeper AI-powered analysis!\n")


if __name__ == "__main__":
    main()
