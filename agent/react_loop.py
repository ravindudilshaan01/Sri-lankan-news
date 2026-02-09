"""
ReAct (Reasoning + Acting) Loop Implementation
This is the "brain" of the agent that follows: Thought → Action → Observation
"""
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

logger = logging.getLogger("ReActLoop")


@dataclass
class ReActStep:
    """Single step in the ReAct loop"""
    thought: str       # Why the agent is doing this
    action: str        # What the agent decides to do
    observation: str   # What the agent sees/learns
    step_number: int


class ReActLoop:
    """
    Implements the ReAct pattern for agent reasoning
    
    The agent iterates through:
    1. THOUGHT: Reasoning about what to do next
    2. ACTION: Deciding on an action (analyze, flag, request info, etc.)
    3. OBSERVATION: Getting results and updating understanding
    """
    
    def __init__(self, max_iterations: int = 5):
        """
        Initialize ReAct loop
        
        Args:
            max_iterations: Maximum reasoning steps before forcing a conclusion
        """
        self.max_iterations = max_iterations
        self.history: List[ReActStep] = []
        self.current_step = 0
    
    def think(self, context: Dict[str, Any], llm_response: str) -> str:
        """
        THOUGHT phase: Agent reasons about the situation
        
        Args:
            context: Current information (article, previous findings, etc.)
            llm_response: LLM's reasoning text
        
        Returns:
            The thought text
        """
        thought = f"[Step {self.current_step + 1} - THOUGHT] {llm_response}"
        logger.info(thought)
        return thought
    
    def act(self, action_type: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        ACTION phase: Agent decides what to do
        
        Available actions:
        - FLAG_RISK: Mark article as containing risk
        - REQUEST_INFO: Need more context
        - ANALYZE_DEEPER: Dive into specific aspect
        - CONCLUDE: Final assessment ready
        - ESCALATE: Send to human analyst
        
        Args:
            action_type: Type of action to take
            parameters: Action-specific parameters
        
        Returns:
            Action result
        """
        action = f"[Step {self.current_step + 1} - ACTION] {action_type}"
        
        if parameters:
            action += f" with params: {parameters}"
        
        logger.info(action)
        
        # Execute the action
        result = {
            'action_type': action_type,
            'parameters': parameters or {},
            'status': 'executed'
        }
        
        return result
    
    def observe(self, observation_data: Any) -> str:
        """
        OBSERVATION phase: Agent sees the result of action
        
        Args:
            observation_data: Result from the action
        
        Returns:
            Observation text
        """
        observation = f"[Step {self.current_step + 1} - OBSERVATION] {observation_data}"
        logger.info(observation)
        return observation
    
    def add_step(self, thought: str, action: str, observation: str):
        """Record a complete ReAct step"""
        step = ReActStep(
            thought=thought,
            action=action,
            observation=observation,
            step_number=self.current_step
        )
        self.history.append(step)
        self.current_step += 1
    
    def should_continue(self) -> bool:
        """Check if agent should continue reasoning"""
        return self.current_step < self.max_iterations
    
    def get_reasoning_trace(self) -> List[Dict[str, Any]]:
        """Get the complete reasoning history"""
        return [
            {
                'step': step.step_number,
                'thought': step.thought,
                'action': step.action,
                'observation': step.observation
            }
            for step in self.history
        ]
    
    def format_trace_for_report(self) -> str:
        """Format reasoning trace for human-readable report"""
        trace = []
        trace.append("=== Agent Reasoning Trace ===\n")
        
        for step in self.history:
            trace.append(f"\n--- Step {step.step_number + 1} ---")
            trace.append(f"💭 Thought: {step.thought}")
            trace.append(f"🎯 Action: {step.action}")
            trace.append(f"👁️ Observation: {step.observation}")
        
        return "\n".join(trace)
    
    def reset(self):
        """Clear history for new analysis"""
        self.history = []
        self.current_step = 0


class ReActPromptBuilder:
    """Builds prompts that guide the LLM to follow ReAct pattern"""
    
    @staticmethod
    def build_system_prompt(risk_categories: List[str]) -> str:
        """
        Create system prompt that forces ReAct reasoning
        
        This is THE KEY to making the agent think step-by-step
        """
        prompt = f"""You are an expert Risk Analyst for Exiger, a leading risk intelligence company.
Your task is to analyze news articles from Sri Lanka and identify potential risks using the ReAct framework.

You MUST follow this exact pattern for EVERY analysis:

THOUGHT: Explain your reasoning - why you're examining this article, what risks you're looking for
ACTION: Decide what to do - FLAG_RISK, REQUEST_INFO, ANALYZE_DEEPER, CONCLUDE, or ESCALATE  
OBSERVATION: State what you found - specific evidence from the article

Risk Categories to Consider:
{chr(10).join('- ' + cat for cat in risk_categories)}

When analyzing:
1. Look for specific indicators of each risk type
2. Consider severity and potential impact
3. Identify key entities (people, organizations, locations)
4. Assess confidence level (how certain are you?)
5. Recommend actions (monitor, investigate, escalate)

Be thorough but concise. Focus on actionable intelligence."""
        
        return prompt
    
    @staticmethod
    def build_analysis_prompt(article_title: str, article_content: str, article_url: str) -> str:
        """Create prompt for analyzing a specific article"""
        prompt = f"""Analyze this news article for risk assessment:

Title: {article_title}
URL: {article_url}
Content: {article_content}

Follow the ReAct pattern:
1. THOUGHT: What risks might this article indicate?
2. ACTION: What should I do with this information?
3. OBSERVATION: What specific evidence supports my assessment?

Provide:
- Risk Level (Critical/High/Medium/Low/None)
- Risk Categories (list all that apply)
- Confidence (0-100%)
- Key Entities (people, orgs, places mentioned)
- Recommended Actions (2-3 specific next steps)
"""
        return prompt
