"""
EXP-032: Santiago Team Orchestrator
===================================

Orchestrates multi-role Santiago agents in in-memory team bubbles.

Coordinates PM, Architect, Developer, and Ethicist roles through
evolution rounds with evaluation gates.
"""

import asyncio
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum

from in_memory_git_service import InMemoryGitService


class EvolutionPhase(Enum):
    """Phases of a Santiago evolution round."""
    PLANNING = "planning"
    REQUIREMENTS = "requirements" 
    ARCHITECTURE = "architecture"
    DEVELOPMENT = "development"
    TESTING = "testing"
    EVALUATION = "evaluation"
    PROMOTION = "promotion"


@dataclass
class RoleAgent:
    """Represents a role agent in the team."""
    name: str
    prompt_template: str
    workspace_path: Path
    capabilities: List[str]
    
    async def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process work for this role (mock implementation)."""
        # In real implementation, this would call LLM
        await asyncio.sleep(0.1)  # Simulate processing time
        
        return {
            "role": self.name,
            "output": f"Processed {context.get('task', 'unknown')} for {self.name}",
            "timestamp": time.time()
        }


@dataclass
class EvolutionRound:
    """A complete evolution round for a domain."""
    domain: str
    round_number: int
    team_id: str
    start_time: float
    phases: Dict[EvolutionPhase, Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.phases is None:
            self.phases = {}


class SantiagoTeamOrchestrator:
    """
    Orchestrates multi-role Santiago teams in in-memory bubbles.
    
    Manages evolution rounds with evaluation gates and promotion.
    """
    
    def __init__(self, git_service: InMemoryGitService = None):
        self.git_service = git_service or InMemoryGitService()
        self.active_rounds: Dict[str, EvolutionRound] = {}
        self.role_agents: Dict[str, RoleAgent] = {}
        
    def register_role_agent(self, agent: RoleAgent):
        """Register a role agent."""
        self.role_agents[agent.name] = agent
    
    async def start_evolution_round(
        self, 
        domain: str, 
        round_number: int = 1,
        evaluation_threshold: float = 0.8
    ) -> str:
        """
        Start a new evolution round for a domain.
        
        Args:
            domain: Domain name (e.g., 'diabetes', 'copd')
            round_number: Round number
            evaluation_threshold: Minimum score to promote
            
        Returns:
            Team ID for the round
        """
        team_id = f"{domain}_round_{round_number}"
        
        # Create team bubble
        self.git_service.create_team_bubble(team_id)
        
        # Create role workspaces
        for role_name in ['pm', 'architect', 'developer', 'ethicist']:
            workspace_path = self.git_service.clone_role_workspace(team_id, role_name)
            
            # Create mock role agent
            agent = RoleAgent(
                name=role_name,
                prompt_template=f"You are a {role_name} for {domain} domain.",
                workspace_path=workspace_path,
                capabilities=[f"{role_name}_tasks"]
            )
            self.register_role_agent(agent)
        
        # Initialize evolution round
        evolution_round = EvolutionRound(
            domain=domain,
            round_number=round_number,
            team_id=team_id,
            start_time=time.time()
        )
        self.active_rounds[team_id] = evolution_round
        
        return team_id
    
    async def run_evolution_cycle(self, team_id: str) -> Dict[str, Any]:
        """
        Run a complete evolution cycle for a team.
        
        Args:
            team_id: Team identifier
            
        Returns:
            Cycle results
        """
        if team_id not in self.active_rounds:
            raise ValueError(f"No active round for team {team_id}")
        
        evolution_round = self.active_rounds[team_id]
        
        # Phase 1: Requirements (PM)
        pm_results = await self._run_role_phase(team_id, 'pm', {
            'task': 'gather_requirements',
            'domain': evolution_round.domain
        })
        evolution_round.phases[EvolutionPhase.REQUIREMENTS] = pm_results
        
        # Phase 2: Architecture (Architect)
        arch_results = await self._run_role_phase(team_id, 'architect', {
            'task': 'design_architecture',
            'requirements': pm_results
        })
        evolution_round.phases[EvolutionPhase.ARCHITECTURE] = arch_results
        
        # Phase 3: Development (Developer)
        dev_results = await self._run_role_phase(team_id, 'developer', {
            'task': 'implement_features',
            'architecture': arch_results
        })
        evolution_round.phases[EvolutionPhase.DEVELOPMENT] = dev_results
        
        # Phase 4: Ethics Review (Ethicist)
        ethics_results = await self._run_role_phase(team_id, 'ethicist', {
            'task': 'review_ethics',
            'implementation': dev_results
        })
        evolution_round.phases[EvolutionPhase.TESTING] = ethics_results
        
        # Phase 5: Evaluation
        evaluation_results = await self._evaluate_round(evolution_round)
        evolution_round.phases[EvolutionPhase.EVALUATION] = evaluation_results
        
        return {
            'team_id': team_id,
            'round_number': evolution_round.round_number,
            'domain': evolution_round.domain,
            'phases': {k.value: v for k, v in evolution_round.phases.items()},
            'evaluation_score': evaluation_results.get('score', 0),
            'duration': time.time() - evolution_round.start_time
        }
    
    async def _run_role_phase(self, team_id: str, role: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Run a phase for a specific role."""
        if role not in self.role_agents:
            raise ValueError(f"No agent registered for role {role}")
        
        agent = self.role_agents[role]
        
        # Process work
        results = await agent.process(context)
        
        # Commit changes to Git
        commit_message = f"{role}: {context.get('task', 'work')} - {evolution_round.domain}"
        commit_hash = self.git_service.commit_and_push_role_changes(
            team_id, role, commit_message
        )
        
        results['commit_hash'] = commit_hash
        return results
    
    async def _evaluate_round(self, evolution_round: EvolutionRound) -> Dict[str, Any]:
        """Evaluate the quality of an evolution round."""
        # Mock evaluation - in real implementation, this would use LLM evaluation
        await asyncio.sleep(0.1)
        
        # Simple scoring based on phase completion
        completed_phases = len([p for p in evolution_round.phases.values() if p])
        total_phases = len(EvolutionPhase)
        score = completed_phases / total_phases
        
        return {
            'score': score,
            'completed_phases': completed_phases,
            'total_phases': total_phases,
            'evaluation_criteria': ['completeness', 'quality', 'ethics'],
            'recommendations': ['promote' if score > 0.8 else 'revise']
        }
    
    def promote_round(self, team_id: str, output_path: Path) -> bool:
        """
        Promote a successful evolution round to disk.
        
        Args:
            team_id: Team identifier
            output_path: Where to save the patch
            
        Returns:
            True if promoted successfully
        """
        if team_id not in self.active_rounds:
            return False
        
        evolution_round = self.active_rounds[team_id]
        evaluation = evolution_round.phases.get(EvolutionPhase.EVALUATION, {})
        
        if evaluation.get('score', 0) < 0.8:
            return False
        
        # Export patch
        self.git_service.export_patch(team_id, output_path)
        
        # Mark as promoted
        evolution_round.phases[EvolutionPhase.PROMOTION] = {
            'promoted': True,
            'patch_path': str(output_path),
            'timestamp': time.time()
        }
        
        return True
    
    def cleanup_round(self, team_id: str):
        """Clean up a completed evolution round."""
        if team_id in self.active_rounds:
            del self.active_rounds[team_id]
        
        self.git_service.cleanup_team_bubble(team_id)
        
        # Clean up role agents
        for role in ['pm', 'architect', 'developer', 'ethicist']:
            if role in self.role_agents:
                del self.role_agents[role]
    
    def get_round_status(self, team_id: str) -> Dict[str, Any]:
        """Get status of an evolution round."""
        if team_id not in self.active_rounds:
            return {"status": "not_found"}
        
        evolution_round = self.active_rounds[team_id]
        
        return {
            "team_id": team_id,
            "domain": evolution_round.domain,
            "round_number": evolution_round.round_number,
            "duration": time.time() - evolution_round.start_time,
            "phases_completed": len([p for p in evolution_round.phases.values() if p]),
            "evaluation_score": evolution_round.phases.get(EvolutionPhase.EVALUATION, {}).get('score', 0),
            "git_status": self.git_service.get_team_status(team_id)
        }


# CLI interface
def main():
    """CLI entry point for team orchestrator."""
    import argparse
    
    parser = argparse.ArgumentParser(description="EXP-032: Santiago Team Orchestrator")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Start round
    start_parser = subparsers.add_parser('start-round', help='Start evolution round')
    start_parser.add_argument('domain', help='Domain name')
    start_parser.add_argument('--round', type=int, default=1, help='Round number')
    start_parser.add_argument('--threshold', type=float, default=0.8, help='Evaluation threshold')
    
    # Run cycle
    run_parser = subparsers.add_parser('run-cycle', help='Run evolution cycle')
    run_parser.add_argument('team_id', help='Team identifier')
    
    # Get status
    status_parser = subparsers.add_parser('status', help='Get round status')
    status_parser.add_argument('team_id', help='Team identifier')
    
    # Promote
    promote_parser = subparsers.add_parser('promote', help='Promote round to disk')
    promote_parser.add_argument('team_id', help='Team identifier')
    promote_parser.add_argument('output_path', help='Output patch file')
    
    # Cleanup
    cleanup_parser = subparsers.add_parser('cleanup', help='Clean up round')
    cleanup_parser.add_argument('team_id', help='Team identifier')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    orchestrator = SantiagoTeamOrchestrator()
    
    try:
        if args.command == 'start-round':
            team_id = asyncio.run(orchestrator.start_evolution_round(
                args.domain, args.round, args.threshold
            ))
            print(f"✅ Started evolution round: {team_id}")
            
        elif args.command == 'run-cycle':
            results = asyncio.run(orchestrator.run_evolution_cycle(args.team_id))
            print(f"✅ Completed evolution cycle for {args.team_id}")
            print(f"   Evaluation Score: {results['evaluation_score']:.2f}")
            print(f"   Duration: {results['duration']:.1f}s")
            
        elif args.command == 'status':
            status = orchestrator.get_round_status(args.team_id)
            print(f"Round {args.team_id} Status:")
            print(json.dumps(status, indent=2))
            
        elif args.command == 'promote':
            success = orchestrator.promote_round(args.team_id, Path(args.output_path))
            if success:
                print(f"✅ Promoted round {args.team_id} to: {args.output_path}")
            else:
                print(f"❌ Failed to promote round {args.team_id} (evaluation score too low)")
            
        elif args.command == 'cleanup':
            orchestrator.cleanup_round(args.team_id)
            print(f"✅ Cleaned up round: {args.team_id}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)


if __name__ == '__main__':
    main()