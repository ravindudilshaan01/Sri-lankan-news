"""
Risk Analyst Agent - Main Agent Class
Integrates ReAct loop with LLM for intelligent risk analysis
"""
import os
import logging
import json
from typing import List, Dict, Any, Optional
from datetime import datetime

# LLM Integration - supports both OpenAI and local models
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logging.warning("OpenAI not available. Install with: pip install openai")

from models import Article
from .react_loop import ReActLoop, ReActPromptBuilder
from .risk_categories import (
    RiskLevel, RiskCategory, RiskAssessment, 
    RiskIndicators
)

logger = logging.getLogger("RiskAgent")


class RiskAnalystAgent:
    """
    AI Agent that analyzes news articles for risks using ReAct pattern
    
    This is the "brain" that replaces simple linear analysis with:
    Scrape → THINK → Analyze → ACT loop
    """
    
    def __init__(
        self, 
        model: str = "gpt-4-turbo-preview",
        api_key: Optional[str] = None,
        use_local_analysis: bool = True  # Fallback if no LLM
    ):
        """
        Initialize Risk Analyst Agent
        
        Args:
            model: LLM model to use (gpt-4, gpt-3.5-turbo, etc.)
            api_key: OpenAI API key (or set OPENAI_API_KEY env var)
            use_local_analysis: Use keyword-based analysis as fallback
        """
        self.model = model
        self.use_local_analysis = use_local_analysis
        
        # Initialize LLM client if available
        if OPENAI_AVAILABLE and (api_key or os.getenv('OPENAI_API_KEY')):
            self.client = OpenAI(api_key=api_key or os.getenv('OPENAI_API_KEY'))
            self.llm_available = True
            logger.info(f"LLM initialized with model: {model}")
        else:
            self.client = None
            self.llm_available = False
            logger.warning("LLM not available. Using local keyword-based analysis.")
        
        # Get risk categories for prompts
        self.risk_categories = [cat.value for cat in RiskCategory]
        
        # Build system prompt
        self.system_prompt = ReActPromptBuilder.build_system_prompt(
            self.risk_categories
        )
    
    def analyze_article(self, article: Article) -> RiskAssessment:
        """
        Main analysis method - uses ReAct pattern
        
        Args:
            article: News article to analyze
        
        Returns:
            RiskAssessment with reasoning trace
        """
        logger.info(f"Analyzing article: {article.title[:50]}...")
        
        # Initialize ReAct loop
        react_loop = ReActLoop(max_iterations=3)
        
        if self.llm_available:
            # Use LLM for intelligent analysis
            assessment = self._llm_based_analysis(article, react_loop)
        else:
            # Fallback to keyword-based analysis
            assessment = self._keyword_based_analysis(article, react_loop)
        
        # Add reasoning trace to assessment
        assessment.reasoning_trace = react_loop.get_reasoning_trace()
        
        return assessment
    
    def _llm_based_analysis(
        self, 
        article: Article, 
        react_loop: ReActLoop
    ) -> RiskAssessment:
        """
        Use LLM with ReAct pattern for deep analysis
        
        This is where the "magic" happens - the LLM thinks step by step
        """
        # Build analysis prompt
        analysis_prompt = ReActPromptBuilder.build_analysis_prompt(
            article_title=article.title,
            article_content=article.description or article.title,
            article_url=article.url
        )
        
        # STEP 1: THOUGHT - Ask LLM to reason about the article
        thought = react_loop.think(
            context={'article': article},
            llm_response="Analyzing article for risk indicators..."
        )
        
        # Call LLM
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=0.3,  # Lower = more focused
                max_tokens=1000
            )
            
            llm_output = response.choices[0].message.content
            
            # STEP 2: ACTION - Parse LLM's decision
            action_result = react_loop.act(
                action_type="ANALYZE_WITH_LLM",
                parameters={'prompt': analysis_prompt}
            )
            
            # STEP 3: OBSERVATION - Extract structured data from LLM response
            observation = react_loop.observe(llm_output)
            
            react_loop.add_step(thought, str(action_result), observation)
            
            # Parse LLM response into RiskAssessment
            assessment = self._parse_llm_response(article, llm_output)
            
        except Exception as e:
            logger.error(f"LLM analysis failed: {e}")
            # Fallback to keyword analysis
            assessment = self._keyword_based_analysis(article, react_loop)
        
        return assessment
    
    def _keyword_based_analysis(
        self, 
        article: Article, 
        react_loop: ReActLoop
    ) -> RiskAssessment:
        """
        Fallback: Rule-based analysis using keyword matching
        
        This works without LLM but is less sophisticated
        """
        text = f"{article.title} {article.description or ''}".lower()
        
        # THOUGHT
        thought = react_loop.think(
            context={'article': article},
            llm_response="Using keyword-based risk detection..."
        )
        
        # ACTION: Scan for risk indicators
        found_categories = []
        risk_score = 0
        
        for category, keywords in RiskIndicators.INDICATORS.items():
            for keyword in keywords:
                if keyword.lower() in text:
                    found_categories.append(category)
                    risk_score += 1
                    break  # Count category once
        
        action_result = react_loop.act(
            action_type="KEYWORD_SCAN",
            parameters={'keywords_found': risk_score}
        )
        
        # OBSERVATION
        observation = react_loop.observe(
            f"Found {len(found_categories)} risk categories: {[c.value for c in found_categories]}"
        )
        
        react_loop.add_step(thought, str(action_result), observation)
        
        # Determine risk level based on score
        if risk_score >= 5:
            risk_level = RiskLevel.HIGH
        elif risk_score >= 3:
            risk_level = RiskLevel.MEDIUM
        elif risk_score >= 1:
            risk_level = RiskLevel.LOW
        else:
            risk_level = RiskLevel.NONE
        
        # Generate recommendations
        actions = self._generate_recommendations(risk_level, found_categories)
        
        return RiskAssessment(
            article_id=str(hash(article.url)),
            article_title=article.title,
            risk_level=risk_level,
            risk_categories=found_categories[:3],  # Top 3
            reasoning=f"Keyword-based analysis found {risk_score} risk indicators",
            confidence=0.6 if found_categories else 0.3,  # Lower confidence for keywords
            recommended_actions=actions,
            key_entities=[],
            geographic_scope="Sri Lanka"
        )
    
    def _parse_llm_response(self, article: Article, llm_response: str) -> RiskAssessment:
        """
        Extract structured risk assessment from LLM's text response
        
        In production, you'd use structured output or function calling
        """
        # Simple parsing - look for keywords in response
        response_lower = llm_response.lower()
        
        # Determine risk level
        if "critical" in response_lower:
            risk_level = RiskLevel.CRITICAL
        elif "high" in response_lower:
            risk_level = RiskLevel.HIGH
        elif "medium" in response_lower or "moderate" in response_lower:
            risk_level = RiskLevel.MEDIUM
        elif "low" in response_lower:
            risk_level = RiskLevel.LOW
        else:
            risk_level = RiskLevel.NONE
        
        # Find mentioned categories
        found_categories = []
        for category in RiskCategory:
            if category.value.lower() in response_lower:
                found_categories.append(category)
        
        # Extract confidence (look for percentage)
        confidence = 0.75  # Default
        if "confidence" in response_lower:
            # Try to extract percentage
            import re
            match = re.search(r'(\d+)%', llm_response)
            if match:
                confidence = int(match.group(1)) / 100
        
        return RiskAssessment(
            article_id=str(hash(article.url)),
            article_title=article.title,
            risk_level=risk_level,
            risk_categories=found_categories[:3],
            reasoning=llm_response,
            confidence=confidence,
            recommended_actions=self._generate_recommendations(risk_level, found_categories),
            key_entities=[],
            geographic_scope="Sri Lanka"
        )
    
    def _generate_recommendations(
        self, 
        risk_level: RiskLevel, 
        categories: List[RiskCategory]
    ) -> List[str]:
        """Generate action recommendations based on risk assessment"""
        actions = []
        
        if risk_level == RiskLevel.CRITICAL:
            actions.append("🚨 ESCALATE: Notify senior analysts immediately")
            actions.append("📊 Create detailed intelligence report")
            actions.append("👥 Brief relevant stakeholders")
        
        elif risk_level == RiskLevel.HIGH:
            actions.append("⚠️ MONITOR: Set up continuous monitoring")
            actions.append("🔍 INVESTIGATE: Gather additional intelligence")
            actions.append("📋 Document for compliance review")
        
        elif risk_level == RiskLevel.MEDIUM:
            actions.append("👀 WATCH: Add to monitoring watchlist")
            actions.append("📝 Log in risk register")
        
        elif risk_level == RiskLevel.LOW:
            actions.append("ℹ️ RECORD: Add to intelligence database")
        
        else:
            actions.append("✓ No immediate action required")
        
        # Category-specific actions
        if RiskCategory.CORRUPTION in categories:
            actions.append("🔎 Cross-reference with sanctions databases")
        
        if RiskCategory.POLITICAL_INSTABILITY in categories:
            actions.append("🌍 Check international response and implications")
        
        return actions[:3]  # Top 3 actions
    
    def analyze_batch(self, articles: List[Article]) -> List[RiskAssessment]:
        """Analyze multiple articles"""
        assessments = []
        
        for i, article in enumerate(articles, 1):
            logger.info(f"Processing article {i}/{len(articles)}")
            try:
                assessment = self.analyze_article(article)
                assessments.append(assessment)
            except Exception as e:
                logger.error(f"Failed to analyze article {article.title[:30]}: {e}")
        
        return assessments
    
    def generate_summary_report(self, assessments: List[RiskAssessment]) -> Dict[str, Any]:
        """
        Generate executive summary of risk landscape
        """
        # Count by risk level
        risk_counts = {level: 0 for level in RiskLevel}
        for assessment in assessments:
            risk_counts[assessment.risk_level] += 1
        
        # Count by category
        category_counts = {}
        for assessment in assessments:
            for category in assessment.risk_categories:
                category_counts[category.value] = category_counts.get(category.value, 0) + 1
        
        # Get high-priority items
        high_priority = [
            a for a in assessments 
            if a.risk_level in [RiskLevel.CRITICAL, RiskLevel.HIGH]
        ]
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_articles_analyzed': len(assessments),
            'risk_distribution': {level.value: count for level, count in risk_counts.items()},
            'top_risk_categories': sorted(
                category_counts.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:5],
            'high_priority_count': len(high_priority),
            'high_priority_articles': [a.to_dict() for a in high_priority[:5]],
            'average_confidence': sum(a.confidence for a in assessments) / len(assessments) if assessments else 0
        }
