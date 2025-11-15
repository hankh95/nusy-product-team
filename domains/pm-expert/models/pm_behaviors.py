"""
PM Service Behaviors

This module defines the PM-specific behaviors and services that agents can perform
for product management tasks. These behaviors integrate with the Santiago agent framework.
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class PMBehaviorType(Enum):
    """Types of PM behaviors available."""
    SPRINT_PLANNING = "sprint_planning"
    BACKLOG_REFINEMENT = "backlog_refinement"
    RETROSPECTIVE = "retrospective"
    STAKEHOLDER_COMMUNICATION = "stakeholder_communication"
    RISK_ASSESSMENT = "risk_assessment"
    USER_STORY_MAPPING = "user_story_mapping"
    DISCOVERY_SESSION = "discovery_session"
    FEATURE_PRIORITIZATION = "feature_prioritization"


class PMServiceBehaviors:
    """PM-specific behaviors for autonomous agents."""
    
    def __init__(self, agent_adapter, knowledge_graph=None):
        self.agent_adapter = agent_adapter
        self.knowledge_graph = knowledge_graph
        self.behavior_history: List[Dict] = []
    
    async def facilitate_sprint_planning(self, 
                                        team_velocity: Optional[int] = None,
                                        backlog_items: Optional[List[Dict]] = None,
                                        sprint_goal: Optional[str] = None) -> Dict[str, Any]:
        """Facilitate a sprint planning session."""
        logger.info("Facilitating sprint planning session")
        
        context = {
            "team_velocity": team_velocity,
            "backlog_items_count": len(backlog_items) if backlog_items else 0,
            "sprint_goal": sprint_goal
        }
        
        # Have Pilot agent guide the sprint planning
        planning_prompt = f"""As the PM expert, facilitate a sprint planning session with the following context:
        
Team Velocity: {team_velocity if team_velocity else 'Unknown'}
Backlog Items: {len(backlog_items) if backlog_items else 0} items ready
Sprint Goal: {sprint_goal if sprint_goal else 'To be defined'}

Provide guidance on:
1. Setting a clear, achievable sprint goal
2. Selecting appropriate backlog items based on velocity
3. Breaking down large items if needed
4. Ensuring team alignment and commitment
5. Identifying risks and dependencies

Respond with a structured sprint plan."""
        
        response = await self.agent_adapter.send_message("pilot", planning_prompt, context)
        
        # Have Quartermaster review for ethical considerations
        ethical_review_prompt = f"""Review this sprint planning approach for ethical alignment:

{response[:1000]}

Ensure:
- Fair distribution of work
- Sustainable pace
- Team wellbeing considerations
- Transparent communication"""
        
        ethical_response = await self.agent_adapter.send_message("quartermaster", ethical_review_prompt)
        
        result = {
            "behavior": PMBehaviorType.SPRINT_PLANNING.value,
            "timestamp": datetime.now().isoformat(),
            "planning_guidance": response,
            "ethical_review": ethical_response,
            "status": "completed",
            "context": context
        }
        
        self.behavior_history.append(result)
        return result
    
    async def conduct_retrospective(self,
                                   sprint_id: str,
                                   team_feedback: Optional[List[str]] = None,
                                   metrics: Optional[Dict] = None) -> Dict[str, Any]:
        """Conduct a sprint retrospective."""
        logger.info(f"Conducting retrospective for sprint: {sprint_id}")
        
        context = {
            "sprint_id": sprint_id,
            "feedback_items": len(team_feedback) if team_feedback else 0,
            "metrics": metrics
        }
        
        retro_prompt = f"""As the PM expert, facilitate a retrospective for Sprint {sprint_id}.

Context:
- Team Feedback: {len(team_feedback) if team_feedback else 0} items
- Sprint Metrics: {metrics if metrics else 'Not provided'}

Guide the team through:
1. What went well?
2. What could be improved?
3. Action items for next sprint
4. Celebrating successes
5. Learning from challenges

Focus on continuous improvement and team growth."""
        
        response = await self.agent_adapter.send_message("pilot", retro_prompt, context)
        
        # Ethical review for safe space and fairness
        ethical_prompt = f"""Ensure this retrospective approach creates a safe, inclusive space:

{response[:1000]}

Validate:
- All voices heard equally
- Focus on improvement, not blame
- Psychological safety
- Actionable outcomes"""
        
        ethical_response = await self.agent_adapter.send_message("quartermaster", ethical_prompt)
        
        result = {
            "behavior": PMBehaviorType.RETROSPECTIVE.value,
            "timestamp": datetime.now().isoformat(),
            "retrospective_guidance": response,
            "ethical_review": ethical_response,
            "status": "completed",
            "context": context
        }
        
        self.behavior_history.append(result)
        return result
    
    async def refine_backlog(self,
                            backlog_items: List[Dict],
                            prioritization_criteria: Optional[Dict] = None) -> Dict[str, Any]:
        """Refine and prioritize the product backlog."""
        logger.info("Refining product backlog")
        
        context = {
            "items_count": len(backlog_items),
            "criteria": prioritization_criteria
        }
        
        refinement_prompt = f"""As the PM expert, help refine the product backlog with {len(backlog_items)} items.

Prioritization Criteria: {prioritization_criteria if prioritization_criteria else 'Value, Risk, Dependencies'}

Provide guidance on:
1. Clarifying acceptance criteria
2. Estimating effort/complexity
3. Prioritizing by value and risk
4. Identifying dependencies
5. Breaking down large items
6. Removing outdated items

Return structured recommendations."""
        
        response = await self.agent_adapter.send_message("pilot", refinement_prompt, context)
        
        result = {
            "behavior": PMBehaviorType.BACKLOG_REFINEMENT.value,
            "timestamp": datetime.now().isoformat(),
            "refinement_guidance": response,
            "status": "completed",
            "context": context
        }
        
        self.behavior_history.append(result)
        return result
    
    async def assess_risks(self,
                          project_context: Dict,
                          known_risks: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """Assess project risks and suggest mitigation strategies."""
        logger.info("Assessing project risks")
        
        context = {
            "project": project_context,
            "existing_risks": len(known_risks) if known_risks else 0
        }
        
        risk_prompt = f"""As the PM expert, assess project risks:

Project Context: {project_context}
Known Risks: {len(known_risks) if known_risks else 0}

Identify and analyze:
1. Technical risks
2. Resource risks
3. Timeline risks
4. Stakeholder risks
5. Market/business risks

For each risk, provide:
- Description
- Impact (high/medium/low)
- Probability (high/medium/low)
- Mitigation strategy"""
        
        response = await self.agent_adapter.send_message("pilot", risk_prompt, context)
        
        # Ethical review of risk mitigation strategies
        ethical_prompt = f"""Review these risk mitigation strategies for ethical considerations:

{response[:1000]}

Ensure strategies:
- Protect team wellbeing
- Maintain transparency with stakeholders
- Avoid exploitative shortcuts
- Uphold quality and integrity"""
        
        ethical_response = await self.agent_adapter.send_message("quartermaster", ethical_prompt)
        
        result = {
            "behavior": PMBehaviorType.RISK_ASSESSMENT.value,
            "timestamp": datetime.now().isoformat(),
            "risk_analysis": response,
            "ethical_review": ethical_response,
            "status": "completed",
            "context": context
        }
        
        self.behavior_history.append(result)
        return result
    
    async def facilitate_user_story_mapping(self,
                                           user_journey: Optional[str] = None,
                                           existing_stories: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """Facilitate a user story mapping session."""
        logger.info("Facilitating user story mapping")
        
        context = {
            "user_journey": user_journey,
            "story_count": len(existing_stories) if existing_stories else 0
        }
        
        mapping_prompt = f"""As the PM expert (trained in Jeff Patton's methodology), facilitate user story mapping:

User Journey: {user_journey if user_journey else 'To be defined'}
Existing Stories: {len(existing_stories) if existing_stories else 0}

Guide the team through:
1. Identifying user activities (backbone)
2. Mapping user tasks under each activity
3. Organizing by priority (walking skeleton)
4. Identifying MVP scope
5. Planning releases

Focus on user outcomes and value delivery."""
        
        response = await self.agent_adapter.send_message("pilot", mapping_prompt, context)
        
        result = {
            "behavior": PMBehaviorType.USER_STORY_MAPPING.value,
            "timestamp": datetime.now().isoformat(),
            "mapping_guidance": response,
            "status": "completed",
            "context": context
        }
        
        self.behavior_history.append(result)
        return result
    
    async def conduct_discovery_session(self,
                                       hypothesis: Optional[str] = None,
                                       research_questions: Optional[List[str]] = None) -> Dict[str, Any]:
        """Conduct a continuous discovery session."""
        logger.info("Conducting discovery session")
        
        context = {
            "hypothesis": hypothesis,
            "questions_count": len(research_questions) if research_questions else 0
        }
        
        discovery_prompt = f"""As the PM expert (trained in Lean UX and continuous discovery), facilitate a discovery session:

Hypothesis: {hypothesis if hypothesis else 'To be formulated'}
Research Questions: {len(research_questions) if research_questions else 0} questions

Guide the team through:
1. Formulating clear hypotheses
2. Designing experiments to test assumptions
3. Planning user research
4. Defining success metrics
5. Prototyping approaches

Apply build-measure-learn cycle."""
        
        response = await self.agent_adapter.send_message("pilot", discovery_prompt, context)
        
        # Ethical review for user research
        ethical_prompt = f"""Review this discovery approach for ethical research practices:

{response[:1000]}

Ensure:
- User privacy and data protection
- Informed consent
- Respect for user time
- Unbiased research methods"""
        
        ethical_response = await self.agent_adapter.send_message("quartermaster", ethical_prompt)
        
        result = {
            "behavior": PMBehaviorType.DISCOVERY_SESSION.value,
            "timestamp": datetime.now().isoformat(),
            "discovery_guidance": response,
            "ethical_review": ethical_response,
            "status": "completed",
            "context": context
        }
        
        self.behavior_history.append(result)
        return result
    
    async def manage_stakeholders(self,
                                 stakeholders: List[Dict],
                                 communication_plan: Optional[Dict] = None) -> Dict[str, Any]:
        """Manage stakeholder communication and expectations."""
        logger.info("Managing stakeholder communication")
        
        context = {
            "stakeholder_count": len(stakeholders),
            "has_plan": communication_plan is not None
        }
        
        stakeholder_prompt = f"""As the PM expert, provide stakeholder management guidance:

Stakeholders: {len(stakeholders)} identified
Communication Plan: {'Defined' if communication_plan else 'Needs creation'}

Provide guidance on:
1. Stakeholder analysis (influence/interest)
2. Communication strategies per stakeholder
3. Managing expectations
4. Handling conflicts
5. Building trust and alignment"""
        
        response = await self.agent_adapter.send_message("pilot", stakeholder_prompt, context)
        
        # Ethical review for trustworthy communication
        ethical_prompt = f"""Review stakeholder management approach for ethical communication:

{response[:1000]}

Ensure:
- Honesty and transparency
- Respectful engagement
- Fairness to all stakeholders
- Integrity in commitments"""
        
        ethical_response = await self.agent_adapter.send_message("quartermaster", ethical_prompt)
        
        result = {
            "behavior": PMBehaviorType.STAKEHOLDER_COMMUNICATION.value,
            "timestamp": datetime.now().isoformat(),
            "stakeholder_guidance": response,
            "ethical_review": ethical_response,
            "status": "completed",
            "context": context
        }
        
        self.behavior_history.append(result)
        return result
    
    def get_behavior_history(self) -> List[Dict]:
        """Get the history of executed PM behaviors."""
        return self.behavior_history
    
    def get_behavior_statistics(self) -> Dict[str, int]:
        """Get statistics about executed behaviors."""
        stats = {}
        for behavior in self.behavior_history:
            behavior_type = behavior.get("behavior", "unknown")
            stats[behavior_type] = stats.get(behavior_type, 0) + 1
        return stats
