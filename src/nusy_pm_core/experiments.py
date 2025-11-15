"""Experiments Service."""

import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from rdflib import URIRef, Literal

from .models.experiment import ExperimentResult, ExperimentConfig, ExperimentStatus
from .models.kg import KGNode, KGRelation
from .knowledge.graph import KnowledgeGraph, NUSY


class ExperimentsService:
    """Service for managing experiments, configs, and results."""

    def __init__(self, experiments_file: Optional[Path] = None, kg: Optional[KnowledgeGraph] = None):
        self.experiments_file = experiments_file or Path(__file__).resolve().parents[2] / "data" / "experiments.json"
        self.experiments_file.parent.mkdir(parents=True, exist_ok=True)
        self.kg = kg or KnowledgeGraph()
        self._experiments: Dict[str, ExperimentResult] = {}
        self._configs: Dict[str, ExperimentConfig] = {}
        self._load_experiments()

    def _load_experiments(self) -> None:
        """Load experiments from storage."""
        if self.experiments_file.exists():
            with open(self.experiments_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for exp_data in data.get('experiments', []):
                    exp = self._deserialize_experiment(exp_data)
                    self._experiments[exp.experiment_name] = exp
                for config_data in data.get('configs', []):
                    config = self._deserialize_config(config_data)
                    self._configs[config.experiment_name] = config

    def _save_experiments(self) -> None:
        """Save experiments to storage."""
        data = {
            'experiments': [self._serialize_experiment(exp) for exp in self._experiments.values()],
            'configs': [self._serialize_config(config) for config in self._configs.values()]
        }
        with open(self.experiments_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def _serialize_experiment(self, exp: ExperimentResult) -> Dict[str, Any]:
        """Serialize an experiment to dictionary."""
        return {
            'experiment_name': exp.experiment_name,
            'start_time': exp.start_time.isoformat(),
            'end_time': exp.end_time.isoformat() if exp.end_time else None,
            'status': exp.status,
            'phases_completed': exp.phases_completed,
            'total_phases': exp.total_phases,
            'success_metrics': exp.success_metrics,
            'failures': exp.failures,
            'decisions_made': [self._serialize_decision(d) for d in exp.decisions_made],
            'final_assessment': exp.final_assessment
        }

    def _deserialize_experiment(self, data: Dict[str, Any]) -> ExperimentResult:
        """Deserialize an experiment from dictionary."""
        exp = ExperimentResult(
            experiment_name=data['experiment_name'],
            start_time=datetime.fromisoformat(data['start_time']),
            end_time=datetime.fromisoformat(data['end_time']) if data.get('end_time') else None,
            status=data['status'],
            phases_completed=data['phases_completed'],
            total_phases=data['total_phases'],
            success_metrics=data['success_metrics'],
            failures=data['failures'],
            decisions_made=[self._deserialize_decision(d) for d in data.get('decisions_made', [])],
            final_assessment=data['final_assessment']
        )
        return exp

    def _serialize_config(self, config: ExperimentConfig) -> Dict[str, Any]:
        """Serialize a config to dictionary."""
        return {
            'experiment_name': config.experiment_name,
            'duration_days': config.duration_days,
            'phases': [self._serialize_phase(p) for p in config.phases],
            'decision_triggers': config.decision_triggers,
            'success_criteria': config.success_criteria,
            'api_keys': config.api_keys,
            'resource_limits': config.resource_limits
        }

    def _deserialize_config(self, data: Dict[str, Any]) -> ExperimentConfig:
        """Deserialize a config from dictionary."""
        config = ExperimentConfig(
            experiment_name=data['experiment_name'],
            duration_days=data['duration_days'],
            phases=[self._deserialize_phase(p) for p in data['phases']],
            decision_triggers=data['decision_triggers'],
            success_criteria=data['success_criteria'],
            api_keys=data.get('api_keys', {}),
            resource_limits=data.get('resource_limits', {})
        )
        return config

    def _serialize_phase(self, phase) -> Dict[str, Any]:
        """Serialize a phase."""
        return {
            'name': phase.name,
            'duration_days': phase.duration_days,
            'behaviors': phase.behaviors,
            'success_metrics': phase.success_metrics,
            'status': phase.status,
            'start_time': phase.start_time.isoformat() if phase.start_time else None,
            'end_time': phase.end_time.isoformat() if phase.end_time else None,
            'metrics_results': phase.metrics_results
        }

    def _deserialize_phase(self, data: Dict[str, Any]):
        """Deserialize a phase."""
        from .models.experiment import ExperimentPhase
        phase = ExperimentPhase(
            name=data['name'],
            duration_days=data['duration_days'],
            behaviors=data['behaviors'],
            success_metrics=data['success_metrics'],
            status=data['status'],
            start_time=datetime.fromisoformat(data['start_time']) if data.get('start_time') else None,
            end_time=datetime.fromisoformat(data['end_time']) if data.get('end_time') else None,
            metrics_results=data['metrics_results']
        )
        return phase

    def _serialize_decision(self, decision) -> Dict[str, Any]:
        """Serialize a decision."""
        return {
            'id': decision.id,
            'title': decision.title,
            'context': decision.context,
            'options': decision.options,
            'priority': decision.priority,
            'timestamp': decision.timestamp.isoformat(),
            'resolved': decision.resolved,
            'resolution': decision.resolution,
            'resolution_timestamp': decision.resolution_timestamp.isoformat() if decision.resolution_timestamp else None
        }

    def _deserialize_decision(self, data: Dict[str, Any]):
        """Deserialize a decision."""
        from .models.experiment import Decision
        decision = Decision(
            id=data['id'],
            title=data['title'],
            context=data['context'],
            options=data['options'],
            priority=data['priority'],
            timestamp=datetime.fromisoformat(data['timestamp']),
            resolved=data['resolved'],
            resolution=data.get('resolution'),
            resolution_timestamp=datetime.fromisoformat(data['resolution_timestamp']) if data.get('resolution_timestamp') else None
        )
        return decision

    def create_experiment_config(self, config: ExperimentConfig) -> ExperimentConfig:
        """Create a new experiment config."""
        self._configs[config.experiment_name] = config
        self._save_experiments()

        # Add to KG
        config_uri = URIRef(f"{NUSY}experiment_config/{config.experiment_name}")
        self.kg.add_node(KGNode(config_uri, config.experiment_name, NUSY.ExperimentConfig))
        self.kg.add_relation(KGRelation(config_uri, NUSY.duration, Literal(config.duration_days)))
        self.kg.save()

        return config

    def start_experiment(self, experiment_name: str) -> Optional[ExperimentResult]:
        """Start a new experiment."""
        config = self._configs.get(experiment_name)
        if not config:
            return None

        exp = ExperimentResult(
            experiment_name=experiment_name,
            start_time=datetime.now(timezone.utc),
            total_phases=len(config.phases)
        )
        self._experiments[experiment_name] = exp
        self._save_experiments()

        # Add to KG
        exp_uri = URIRef(f"{NUSY}experiment/{experiment_name}")
        self.kg.add_node(KGNode(exp_uri, experiment_name, NUSY.Experiment))
        self.kg.add_relation(KGRelation(exp_uri, NUSY.status, Literal(exp.status)))
        self.kg.save()

        return exp

    def get_experiment(self, experiment_name: str) -> Optional[ExperimentResult]:
        """Get an experiment by name."""
        return self._experiments.get(experiment_name)

    def list_experiments(self) -> List[ExperimentResult]:
        """List all experiments."""
        return list(self._experiments.values())

    def update_experiment_status(self, experiment_name: str, status: str, phases_completed: int = 0, metrics: Dict[str, float] = None) -> bool:
        """Update experiment status."""
        exp = self._experiments.get(experiment_name)
        if not exp:
            return False

        exp.status = status
        exp.phases_completed = phases_completed
        if metrics:
            exp.success_metrics.update(metrics)
        if status in [ExperimentStatus.COMPLETED.value, ExperimentStatus.FAILED.value]:
            exp.end_time = datetime.now(timezone.utc)
        self._save_experiments()

        # Update KG
        exp_uri = URIRef(f"{NUSY}experiment/{experiment_name}")
        self.kg.add_relation(KGRelation(exp_uri, NUSY.status, Literal(status)))
        self.kg.save()

        return True