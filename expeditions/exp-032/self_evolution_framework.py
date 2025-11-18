"""
EXP-032: Self-Evolution Framework
==================================

Self-evolving Santiago agents with safety constraints and improvement mechanisms.

Implements evolutionary algorithms for agent improvement while maintaining
ethical boundaries and safety constraints.
"""

import asyncio
import json
import hashlib
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable, Tuple
from dataclasses import dataclass, field
from enum import Enum
import random

from team_orchestrator import SantiagoTeamOrchestrator, EvolutionRound


class SafetyConstraint(Enum):
    """Safety constraints for self-evolution."""
    ETHICAL_BOUNDARIES = "ethical_boundaries"
    RESOURCE_LIMITS = "resource_limits"
    QUALITY_THRESHOLDS = "quality_thresholds"
    HUMAN_OVERSIGHT = "human_oversight"
    REVERSIBILITY = "reversibility"


@dataclass
class EvolutionGenome:
    """Genome representing agent capabilities and parameters."""
    agent_type: str
    version: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    capabilities: List[str] = field(default_factory=list)
    fitness_score: float = 0.0
    generation: int = 0
    
    def __hash__(self):
        """Hash for genome uniqueness."""
        content = json.dumps({
            'agent_type': self.agent_type,
            'version': self.version,
            'parameters': self.parameters,
            'capabilities': self.capabilities
        }, sort_keys=True)
        return int(hashlib.md5(content.encode()).hexdigest(), 16)
    
    def mutate(self) -> 'EvolutionGenome':
        """Create a mutated copy of this genome."""
        new_genome = EvolutionGenome(
            agent_type=self.agent_type,
            version=f"{self.version}.{self.generation + 1}",
            parameters=self.parameters.copy(),
            capabilities=self.capabilities.copy(),
            generation=self.generation + 1
        )
        
        # Random mutations
        if random.random() < 0.3:  # 30% chance to add capability
            new_capability = f"enhanced_{random.choice(['reasoning', 'learning', 'collaboration', 'efficiency'])}"
            if new_capability not in new_genome.capabilities:
                new_genome.capabilities.append(new_capability)
        
        if random.random() < 0.2:  # 20% chance to modify parameter
            param_keys = list(new_genome.parameters.keys())
            if param_keys:
                key = random.choice(param_keys)
                if isinstance(new_genome.parameters[key], (int, float)):
                    new_genome.parameters[key] *= random.uniform(0.8, 1.2)
                elif isinstance(new_genome.parameters[key], bool):
                    new_genome.parameters[key] = not new_genome.parameters[key]
        
        return new_genome


@dataclass
class SafetyGate:
    """Safety gate for evolution validation."""
    constraint: SafetyConstraint
    validator: Callable[[EvolutionGenome, Dict[str, Any]], bool]
    description: str
    
    async def validate(self, genome: EvolutionGenome, context: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate genome against safety constraint."""
        try:
            result = self.validator(genome, context)
            return result, "passed" if result else "failed"
        except Exception as e:
            return False, f"validation_error: {str(e)}"


class SelfEvolutionFramework:
    """
    Self-evolving framework for Santiago agents.
    
    Implements evolutionary algorithms with safety constraints to improve
    agent capabilities while maintaining ethical and safety boundaries.
    """
    
    def __init__(self, orchestrator: SantiagoTeamOrchestrator = None):
        self.orchestrator = orchestrator or SantiagoTeamOrchestrator()
        self.genomes: Dict[str, List[EvolutionGenome]] = {}
        self.safety_gates: List[SafetyGate] = []
        self.evolution_history: List[Dict[str, Any]] = []
        
        self._setup_safety_gates()
    
    def _setup_safety_gates(self):
        """Set up safety constraints for evolution."""
        
        # Ethical boundaries gate
        def ethical_validator(genome: EvolutionGenome, context: Dict[str, Any]) -> bool:
            # Check for harmful capabilities
            harmful_caps = ['deception', 'manipulation', 'surveillance', 'weaponization']
            return not any(cap in genome.capabilities for cap in harmful_caps)
        
        self.safety_gates.append(SafetyGate(
            constraint=SafetyConstraint.ETHICAL_BOUNDARIES,
            validator=ethical_validator,
            description="Prevents evolution of harmful capabilities"
        ))
        
        # Resource limits gate
        def resource_validator(genome: EvolutionGenome, context: Dict[str, Any]) -> bool:
            # Check resource usage parameters
            max_memory = genome.parameters.get('max_memory_gb', 8)
            max_compute = genome.parameters.get('max_compute_hours', 24)
            return max_memory <= 16 and max_compute <= 48
        
        self.safety_gates.append(SafetyGate(
            constraint=SafetyConstraint.RESOURCE_LIMITS,
            validator=resource_validator,
            description="Limits resource consumption"
        ))
        
        # Quality thresholds gate
        def quality_validator(genome: EvolutionGenome, context: Dict[str, Any]) -> bool:
            # Require minimum fitness score
            return genome.fitness_score >= 0.6
        
        self.safety_gates.append(SafetyGate(
            constraint=SafetyConstraint.QUALITY_THRESHOLDS,
            validator=quality_validator,
            description="Maintains minimum quality standards"
        ))
        
        # Human oversight gate
        def oversight_validator(genome: EvolutionGenome, context: Dict[str, Any]) -> bool:
            # Require human review for major changes
            major_change = context.get('is_major_change', False)
            if major_change:
                return context.get('human_approved', False)
            return True
        
        self.safety_gates.append(SafetyGate(
            constraint=SafetyConstraint.HUMAN_OVERSIGHT,
            validator=oversight_validator,
            description="Requires human approval for major changes"
        ))
        
        # Reversibility gate
        def reversibility_validator(genome: EvolutionGenome, context: Dict[str, Any]) -> bool:
            # Ensure changes can be rolled back
            return 'rollback_version' in genome.parameters
        
        self.safety_gates.append(SafetyGate(
            constraint=SafetyConstraint.REVERSIBILITY,
            validator=reversibility_validator,
            description="Ensures changes are reversible"
        ))
    
    def register_base_genome(self, agent_type: str, genome: EvolutionGenome):
        """Register a base genome for an agent type."""
        if agent_type not in self.genomes:
            self.genomes[agent_type] = []
        self.genomes[agent_type].append(genome)
    
    async def evolve_agent_type(
        self, 
        agent_type: str, 
        generations: int = 5,
        population_size: int = 10,
        context: Dict[str, Any] = None
    ) -> List[EvolutionGenome]:
        """
        Evolve an agent type through multiple generations.
        
        Args:
            agent_type: Type of agent to evolve
            generations: Number of generations to run
            population_size: Size of each generation's population
            context: Evolution context
            
        Returns:
            List of evolved genomes
        """
        if agent_type not in self.genomes:
            raise ValueError(f"No base genome registered for {agent_type}")
        
        context = context or {}
        base_genome = self.genomes[agent_type][0]  # Use first as base
        
        current_population = [base_genome]
        
        for generation in range(generations):
            print(f"🧬 Generation {generation + 1}/{generations} for {agent_type}")
            
            # Generate new population through mutation
            new_population = []
            for _ in range(population_size):
                # Select parent (tournament selection)
                parent = self._tournament_selection(current_population)
                
                # Mutate
                mutant = parent.mutate()
                
                # Evaluate fitness
                fitness = await self._evaluate_fitness(mutant, context)
                mutant.fitness_score = fitness
                
                new_population.append(mutant)
            
            # Apply safety gates
            safe_population = []
            for genome in new_population:
                if await self._passes_safety_gates(genome, context):
                    safe_population.append(genome)
            
            if not safe_population:
                print(f"⚠️  No safe genomes in generation {generation + 1}, keeping previous population")
                safe_population = current_population
            
            # Sort by fitness and keep best
            safe_population.sort(key=lambda g: g.fitness_score, reverse=True)
            current_population = safe_population[:population_size // 2]  # Keep top half
            
            # Record evolution step
            self.evolution_history.append({
                'generation': generation + 1,
                'agent_type': agent_type,
                'population_size': len(current_population),
                'best_fitness': current_population[0].fitness_score if current_population else 0,
                'timestamp': time.time()
            })
        
        return current_population
    
    def _tournament_selection(self, population: List[EvolutionGenome]) -> EvolutionGenome:
        """Tournament selection for parent selection."""
        tournament_size = min(3, len(population))
        candidates = random.sample(population, tournament_size)
        return max(candidates, key=lambda g: g.fitness_score)
    
    async def _evaluate_fitness(self, genome: EvolutionGenome, context: Dict[str, Any]) -> float:
        """Evaluate fitness of a genome."""
        # Mock fitness evaluation - in real implementation, this would test the genome
        await asyncio.sleep(0.05)
        
        # Base fitness from capabilities
        base_fitness = len(genome.capabilities) * 0.1
        
        # Parameter optimization
        param_score = 0
        if 'efficiency' in genome.parameters:
            param_score += genome.parameters['efficiency'] * 0.2
        if 'accuracy' in genome.parameters:
            param_score += genome.parameters['accuracy'] * 0.3
        
        # Generation bonus (slight preference for newer generations)
        generation_bonus = genome.generation * 0.01
        
        fitness = min(1.0, base_fitness + param_score + generation_bonus)
        return fitness
    
    async def _passes_safety_gates(self, genome: EvolutionGenome, context: Dict[str, Any]) -> bool:
        """Check if genome passes all safety gates."""
        for gate in self.safety_gates:
            passed, reason = await gate.validate(genome, context)
            if not passed:
                print(f"🚫 Safety gate failed for {genome.agent_type} v{genome.version}: {gate.constraint.value} - {reason}")
                return False
        return True
    
    async def deploy_evolved_agent(
        self, 
        genome: EvolutionGenome, 
        team_id: str,
        deployment_path: Path
    ) -> bool:
        """
        Deploy an evolved agent to a team.
        
        Args:
            genome: Genome to deploy
            team_id: Target team
            deployment_path: Where to deploy
            
        Returns:
            True if deployment successful
        """
        try:
            # Create deployment manifest
            manifest = {
                'agent_type': genome.agent_type,
                'version': genome.version,
                'capabilities': genome.capabilities,
                'parameters': genome.parameters,
                'fitness_score': genome.fitness_score,
                'generation': genome.generation,
                'deployed_at': time.time(),
                'team_id': team_id
            }
            
            # Save manifest
            manifest_path = deployment_path / f"{genome.agent_type}_{genome.version}_manifest.json"
            manifest_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(manifest_path, 'w') as f:
                json.dump(manifest, f, indent=2)
            
            # Update team orchestrator with new agent
            # (In real implementation, this would load the agent)
            
            print(f"✅ Deployed {genome.agent_type} v{genome.version} to team {team_id}")
            return True
            
        except Exception as e:
            print(f"❌ Deployment failed: {e}")
            return False
    
    def get_evolution_report(self, agent_type: str = None) -> Dict[str, Any]:
        """Get evolution report for agent type or all."""
        if agent_type:
            history = [h for h in self.evolution_history if h['agent_type'] == agent_type]
        else:
            history = self.evolution_history
        
        if not history:
            return {"status": "no_evolution_history"}
        
        latest = max(history, key=lambda h: h['generation'])
        
        return {
            "total_generations": len(set(h['generation'] for h in history)),
            "agent_types_evolved": list(set(h['agent_type'] for h in history)),
            "latest_generation": latest['generation'],
            "best_fitness_achieved": latest['best_fitness'],
            "evolution_history": history[-10:],  # Last 10 entries
            "safety_gates": len(self.safety_gates),
            "safety_constraints": [g.constraint.value for g in self.safety_gates]
        }


# CLI interface
def main():
    """CLI entry point for self-evolution framework."""
    import argparse
    
    parser = argparse.ArgumentParser(description="EXP-032: Self-Evolution Framework")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Register genome
    register_parser = subparsers.add_parser('register-genome', help='Register base genome')
    register_parser.add_argument('agent_type', help='Agent type')
    register_parser.add_argument('version', help='Genome version')
    register_parser.add_argument('--capabilities', nargs='+', default=[], help='Agent capabilities')
    
    # Evolve
    evolve_parser = subparsers.add_parser('evolve', help='Evolve agent type')
    evolve_parser.add_argument('agent_type', help='Agent type to evolve')
    evolve_parser.add_argument('--generations', type=int, default=5, help='Number of generations')
    evolve_parser.add_argument('--population', type=int, default=10, help='Population size')
    
    # Deploy
    deploy_parser = subparsers.add_parser('deploy', help='Deploy evolved agent')
    deploy_parser.add_argument('agent_type', help='Agent type')
    deploy_parser.add_argument('version', help='Genome version')
    deploy_parser.add_argument('team_id', help='Target team')
    deploy_parser.add_argument('deployment_path', help='Deployment directory')
    
    # Report
    report_parser = subparsers.add_parser('report', help='Get evolution report')
    report_parser.add_argument('--agent-type', help='Specific agent type')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    framework = SelfEvolutionFramework()
    
    try:
        if args.command == 'register-genome':
            genome = EvolutionGenome(
                agent_type=args.agent_type,
                version=args.version,
                capabilities=args.capabilities,
                parameters={
                    'efficiency': 0.8,
                    'accuracy': 0.7,
                    'max_memory_gb': 8,
                    'max_compute_hours': 24,
                    'rollback_version': args.version
                }
            )
            framework.register_base_genome(args.agent_type, genome)
            print(f"✅ Registered base genome for {args.agent_type} v{args.version}")
            
        elif args.command == 'evolve':
            evolved = asyncio.run(framework.evolve_agent_type(
                args.agent_type, args.generations, args.population
            ))
            best = max(evolved, key=lambda g: g.fitness_score)
            print(f"✅ Evolved {args.agent_type} through {args.generations} generations")
            print(f"   Best fitness: {best.fitness_score:.3f}")
            print(f"   Capabilities: {best.capabilities}")
            
        elif args.command == 'deploy':
            # Find the genome
            if args.agent_type not in framework.genomes:
                print(f"❌ No genomes registered for {args.agent_type}")
                exit(1)
            
            genome = None
            for g in framework.genomes[args.agent_type]:
                if g.version == args.version:
                    genome = g
                    break
            
            if not genome:
                print(f"❌ Genome {args.agent_type} v{args.version} not found")
                exit(1)
            
            success = asyncio.run(framework.deploy_evolved_agent(
                genome, args.team_id, Path(args.deployment_path)
            ))
            
            if success:
                print(f"✅ Deployed {args.agent_type} v{args.version} to team {args.team_id}")
            else:
                print(f"❌ Deployment failed")
                exit(1)
            
        elif args.command == 'report':
            report = framework.get_evolution_report(args.agent_type)
            print("Evolution Report:")
            print(json.dumps(report, indent=2))
    
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)


if __name__ == '__main__':
    main()