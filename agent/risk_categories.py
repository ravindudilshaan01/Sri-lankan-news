"""
Risk Categories and Levels for News Analysis
Based on Exiger's risk intelligence framework
"""
from enum import Enum
from typing import List, Dict


class RiskLevel(Enum):
    """Risk severity levels"""
    CRITICAL = "Critical"  # Immediate threat, major impact
    HIGH = "High"          # Significant risk, requires attention
    MEDIUM = "Medium"      # Moderate risk, monitor closely
    LOW = "Low"            # Minor risk, informational
    NONE = "None"          # No significant risk identified


class RiskCategory(Enum):
    """Types of risks to monitor"""
    # Geopolitical & Security
    POLITICAL_INSTABILITY = "Political Instability"
    CIVIL_UNREST = "Civil Unrest"
    TERRORISM = "Terrorism"
    MILITARY_CONFLICT = "Military Conflict"
    
    # Economic & Financial
    ECONOMIC_CRISIS = "Economic Crisis"
    FINANCIAL_FRAUD = "Financial Fraud"
    CORRUPTION = "Corruption"
    SANCTIONS = "Sanctions"
    
    # Legal & Compliance
    REGULATORY_CHANGES = "Regulatory Changes"
    LEGAL_VIOLATIONS = "Legal Violations"
    HUMAN_RIGHTS = "Human Rights Violations"
    
    # Operational
    INFRASTRUCTURE_DAMAGE = "Infrastructure Damage"
    SUPPLY_CHAIN = "Supply Chain Disruption"
    CYBER_SECURITY = "Cyber Security Threat"
    
    # Reputational
    CORPORATE_SCANDAL = "Corporate Scandal"
    ENVIRONMENTAL = "Environmental Risk"
    SOCIAL_ISSUES = "Social Issues"
    
    # Other
    PUBLIC_HEALTH = "Public Health Crisis"
    NATURAL_DISASTER = "Natural Disaster"
    UNKNOWN = "Unknown/Other"


class RiskIndicators:
    """Keywords and patterns that indicate specific risk types"""
    
    INDICATORS: Dict[RiskCategory, List[str]] = {
        RiskCategory.POLITICAL_INSTABILITY: [
            "government collapse", "coup", "regime change", "political crisis",
            "election violence", "parliament dissolved", "cabinet reshuffle"
        ],
        RiskCategory.CIVIL_UNREST: [
            "protest", "riot", "strike", "demonstration", "unrest",
            "clashes", "violence", "mob", "agitation"
        ],
        RiskCategory.TERRORISM: [
            "terrorist", "bomb", "explosion", "attack", "militant",
            "extremist", "suicide bomber", "ISIS", "Al-Qaeda"
        ],
        RiskCategory.ECONOMIC_CRISIS: [
            "economic crisis", "inflation", "debt default", "bankruptcy",
            "currency collapse", "recession", "financial crisis", "IMF bailout"
        ],
        RiskCategory.CORRUPTION: [
            "corruption", "bribery", "embezzlement", "fraud", "kickback",
            "money laundering", "misappropriation", "graft"
        ],
        RiskCategory.HUMAN_RIGHTS: [
            "human rights", "torture", "arbitrary arrest", "disappearance",
            "unlawful detention", "abuse", "violation"
        ],
        RiskCategory.CYBER_SECURITY: [
            "cyber attack", "data breach", "hacking", "ransomware",
            "phishing", "malware", "cyber threat"
        ],
        RiskCategory.ENVIRONMENTAL: [
            "pollution", "toxic", "environmental damage", "deforestation",
            "oil spill", "chemical leak", "waste dumping"
        ],
        RiskCategory.PUBLIC_HEALTH: [
            "epidemic", "pandemic", "outbreak", "disease", "health crisis",
            "contamination", "food poisoning"
        ],
        RiskCategory.NATURAL_DISASTER: [
            "flood", "landslide", "cyclone", "earthquake", "tsunami",
            "drought", "wildfire", "natural disaster"
        ],
    }
    
    @classmethod
    def get_keywords(cls, category: RiskCategory) -> List[str]:
        """Get risk indicators for a specific category"""
        return cls.INDICATORS.get(category, [])
    
    @classmethod
    def all_keywords(cls) -> Dict[RiskCategory, List[str]]:
        """Get all risk indicators"""
        return cls.INDICATORS


class RiskAssessment:
    """Container for risk analysis results"""
    
    def __init__(
        self,
        article_id: str,
        article_title: str,
        risk_level: RiskLevel,
        risk_categories: List[RiskCategory],
        reasoning: str,
        confidence: float,
        recommended_actions: List[str],
        key_entities: List[str] = None,
        geographic_scope: str = "Sri Lanka"
    ):
        self.article_id = article_id
        self.article_title = article_title
        self.risk_level = risk_level
        self.risk_categories = risk_categories
        self.reasoning = reasoning
        self.confidence = confidence  # 0.0 to 1.0
        self.recommended_actions = recommended_actions
        self.key_entities = key_entities or []
        self.geographic_scope = geographic_scope
    
    def to_dict(self) -> dict:
        """Convert to dictionary for reporting"""
        return {
            'article_id': self.article_id,
            'article_title': self.article_title,
            'risk_level': self.risk_level.value,
            'risk_categories': [cat.value for cat in self.risk_categories],
            'reasoning': self.reasoning,
            'confidence': self.confidence,
            'recommended_actions': self.recommended_actions,
            'key_entities': self.key_entities,
            'geographic_scope': self.geographic_scope
        }
    
    def __repr__(self) -> str:
        return (f"RiskAssessment(risk_level={self.risk_level.value}, "
                f"categories={[c.value for c in self.risk_categories]}, "
                f"confidence={self.confidence:.2f})")
