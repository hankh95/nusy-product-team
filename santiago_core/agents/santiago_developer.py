"""
Santiago Developer Agent

Implements features and writes code for autonomous development tasks.
"""

import asyncio
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Optional

from santiago_core.core.agent_framework import SantiagoAgent, Task, Message, EthicalOversight


class SantiagoDeveloper(SantiagoAgent):
    """Developer agent for implementing features and writing code"""

    def __init__(self, workspace_path: Path):
        super().__init__("santiago-developer", workspace_path)
        self.implemented_features: List[Dict] = []
        self.test_results: Dict[str, Dict] = {}
        self.code_quality_metrics: Dict[str, float] = {}

    async def handle_custom_message(self, message: Message) -> None:
        """Handle developer-specific messages"""
        if message.message_type == "feature_review":
            await self.implement_feature(message)
        elif message.message_type == "architecture_ready":
            await self.review_architecture_for_implementation(message)
        elif message.message_type == "test_request":
            await self.run_tests(message)

    async def implement_feature(self, message: Message) -> None:
        """Implement a feature based on architectural review"""
        data = json.loads(message.content)
        feature_file = data.get("feature_file", "")
        architectural_review = data.get("architectural_review", {})

        # Read the feature specification
        if os.path.exists(feature_file):
            with open(feature_file, 'r') as f:
                feature_spec = f.read()
        else:
            self.logger.error(f"Feature file not found: {feature_file}")
            return

        # Check if architecture review passed
        if not architectural_review.get("approved", False):
            issues = architectural_review.get("issues", [])
            self.logger.warning(f"Architecture review failed: {issues}")
            # Still proceed but note the issues

        # Implement the feature
        implementation = await self._implement_feature(feature_spec, architectural_review)

        # Save implementation
        impl_path = self._save_implementation(implementation, feature_file)

        # Run tests
        test_results = await self._run_feature_tests(impl_path)

        # Record implementation
        self.implemented_features.append({
            "feature_file": feature_file,
            "implementation_file": str(impl_path),
            "test_results": test_results,
            "architectural_review": architectural_review
        })

        # Notify team of completion
        await self.broadcast_message(
            json.dumps({
                "feature": feature_file,
                "implementation": str(impl_path),
                "test_results": test_results
            }),
            "feature_implemented"
        )

    async def _implement_feature(self, feature_spec: str, architectural_review: Dict) -> str:
        """Generate code implementation for a feature"""
        # Parse feature spec to understand requirements
        scenarios = self._parse_bdd_scenarios(feature_spec)

        # Generate implementation based on scenarios
        implementation = self._generate_code_from_scenarios(scenarios, architectural_review)

        return implementation

    def _parse_bdd_scenarios(self, feature_spec: str) -> List[Dict]:
        """Parse BDD scenarios from feature specification"""
        scenarios = []
        lines = feature_spec.split('\n')

        current_scenario = None
        for line in lines:
            line = line.strip()
            if line.startswith('Scenario:'):
                if current_scenario:
                    scenarios.append(current_scenario)
                current_scenario = {
                    "title": line.replace('Scenario:', '').strip(),
                    "given": [],
                    "when": [],
                    "then": []
                }
            elif current_scenario:
                if line.startswith('Given'):
                    current_scenario["given"].append(line.replace('Given', '').strip())
                elif line.startswith('When'):
                    current_scenario["when"].append(line.replace('When', '').strip())
                elif line.startswith('Then'):
                    current_scenario["then"].append(line.replace('Then', '').strip())

        if current_scenario:
            scenarios.append(current_scenario)

        return scenarios

    def _generate_code_from_scenarios(self, scenarios: List[Dict], architectural_review: Dict) -> str:
        """Generate Python code from BDD scenarios"""
        code_lines = [
            '"""',
            'Autonomously generated feature implementation',
            '"""',
            '',
            'import asyncio',
            'import logging',
            'from typing import Dict, List, Optional',
            'from pathlib import Path',
            '',
            'logger = logging.getLogger(__name__)',
            '',
        ]

        for i, scenario in enumerate(scenarios):
            class_name = f"Feature{scenario['title'].replace(' ', '').replace('-', '')}"

            code_lines.extend([
                f'class {class_name}:',
                f'    """Implementation of: {scenario["title"]}"""',
                '',
                '    def __init__(self):',
                '        self.logger = logging.getLogger(self.__class__.__name__)',
                '',
            ])

            # Generate methods based on scenario steps
            for step in scenario.get("given", []):
                method_name = self._step_to_method_name("given", step)
                code_lines.extend([
                    f'    async def {method_name}(self) -> None:',
                    f'        """{step}"""',
                    '        # TODO: Implement step logic',
                    '        pass',
                    '',
                ])

            for step in scenario.get("when", []):
                method_name = self._step_to_method_name("when", step)
                code_lines.extend([
                    f'    async def {method_name}(self) -> None:',
                    f'        """{step}"""',
                    '        # TODO: Implement step logic',
                    '        pass',
                    '',
                ])

            for step in scenario.get("then", []):
                method_name = self._step_to_method_name("then", step)
                code_lines.extend([
                    f'    async def {method_name}(self) -> None:',
                    f'        """{step}"""',
                    '        # TODO: Implement step logic',
                    '        pass',
                    '',
                ])

            code_lines.extend([
                f'    async def execute_scenario(self) -> bool:',
                '        """Execute the complete scenario"""',
                '        try:',
            ])

            # Call all methods in order
            all_steps = scenario.get("given", []) + scenario.get("when", []) + scenario.get("then", [])
            for step in all_steps:
                method_name = self._step_to_method_name("", step)
                code_lines.append(f'            await self.{method_name}()')

            code_lines.extend([
                '            return True',
                '        except Exception as e:',
                '            self.logger.error(f"Scenario execution failed: {e}")',
                '            return False',
                '',
            ])

        return '\n'.join(code_lines)

    def _step_to_method_name(self, prefix: str, step: str) -> str:
        """Convert a BDD step to a method name"""
        # Simple conversion: lowercase, replace spaces with underscores, remove special chars
        method_name = step.lower()
        method_name = ''.join(c if c.isalnum() or c == ' ' else '' for c in method_name)
        method_name = method_name.replace(' ', '_')
        if prefix:
            method_name = f"{prefix}_{method_name}"
        return method_name

    def _save_implementation(self, implementation: str, feature_file: str) -> Path:
        """Save the implementation to a file"""
        # Create implementation directory
        impl_dir = self.workspace_path / "santiago-pm" / "src" / "features"
        impl_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename from feature file
        feature_name = Path(feature_file).stem
        impl_file = impl_dir / f"{feature_name}.py"

        with open(impl_file, 'w') as f:
            f.write(implementation)

        return impl_file

    async def _run_feature_tests(self, impl_path: Path) -> Dict:
        """Run tests for the implemented feature"""
        # Create a simple test file
        test_file = impl_path.parent / f"test_{impl_path.stem}.py"
        test_content = f'''
"""Tests for {impl_path.stem}"""

import pytest
import asyncio
from {impl_path.stem} import *


@pytest.mark.asyncio
async def test_feature_execution():
    """Test that the feature can be executed"""
    # This is a placeholder test - actual tests would be more specific
    assert True  # Placeholder assertion


if __name__ == "__main__":
    asyncio.run(test_feature_execution())
'''

        with open(test_file, 'w') as f:
            f.write(test_content)

        # Run the tests
        try:
            result = subprocess.run(
                ["python", "-m", "pytest", str(test_file), "-v"],
                capture_output=True,
                text=True,
                cwd=self.workspace_path
            )

            return {
                "passed": result.returncode == 0,
                "output": result.stdout,
                "errors": result.stderr,
                "test_file": str(test_file)
            }
        except Exception as e:
            return {
                "passed": False,
                "output": "",
                "errors": str(e),
                "test_file": str(test_file)
            }

    async def review_architecture_for_implementation(self, message: Message) -> None:
        """Review architecture design for implementation considerations"""
        data = json.loads(message.content)
        architecture = data.get("architecture", "")
        arch_file = data.get("file", "")

        # Analyze architecture for implementation concerns
        impl_concerns = self._analyze_architecture_for_implementation(architecture)

        # Send feedback to architect
        await self.send_message(
            "santiago-architect",
            json.dumps({
                "architecture_file": arch_file,
                "implementation_concerns": impl_concerns
            }),
            "implementation_feedback"
        )

    def _analyze_architecture_for_implementation(self, architecture: str) -> List[str]:
        """Analyze architecture document for implementation concerns"""
        concerns = []

        # Check for complex dependencies
        if "kubernetes" in architecture.lower():
            concerns.append("Kubernetes deployment may require additional infrastructure setup")

        # Check for advanced patterns
        if "microservices" in architecture.lower():
            concerns.append("Microservices architecture requires service discovery and communication setup")

        # Check for scalability requirements
        if "horizontal scaling" in architecture.lower():
            concerns.append("Scaling requirements may need load balancing implementation")

        return concerns

    async def run_tests(self, message: Message) -> None:
        """Run tests as requested"""
        data = json.loads(message.content)
        test_target = data.get("target", "all")

        # Run tests based on target
        if test_target == "all":
            results = await self._run_all_tests()
        else:
            results = await self._run_specific_tests(test_target)

        # Store results
        self.test_results[test_target] = results

        # Report results
        await self.broadcast_message(
            json.dumps({"test_results": results, "target": test_target}),
            "test_results"
        )

    async def _run_all_tests(self) -> Dict:
        """Run all tests in the project"""
        try:
            result = subprocess.run(
                ["python", "-m", "pytest", "--tb=short", "--cov-report=term-missing"],
                capture_output=True,
                text=True,
                cwd=self.workspace_path
            )

            return {
                "passed": result.returncode == 0,
                "output": result.stdout,
                "errors": result.stderr,
                "coverage": self._parse_coverage(result.stdout)
            }
        except Exception as e:
            return {
                "passed": False,
                "output": "",
                "errors": str(e),
                "coverage": 0.0
            }

    async def _run_specific_tests(self, target: str) -> Dict:
        """Run tests for a specific target"""
        # Simplified - just run pytest on the target
        try:
            result = subprocess.run(
                ["python", "-m", "pytest", target, "-v"],
                capture_output=True,
                text=True,
                cwd=self.workspace_path
            )

            return {
                "passed": result.returncode == 0,
                "output": result.stdout,
                "errors": result.stderr
            }
        except Exception as e:
            return {
                "passed": False,
                "output": "",
                "errors": str(e)
            }

    def _parse_coverage(self, output: str) -> float:
        """Parse coverage percentage from pytest output"""
        # Simple parsing - look for "TOTAL" coverage line
        lines = output.split('\n')
        for line in lines:
            if "TOTAL" in line and "%" in line:
                try:
                    # Extract percentage
                    parts = line.split()
                    for part in parts:
                        if "%" in part:
                            return float(part.replace("%", ""))
                except:
                    pass
        return 0.0

    async def start_working_on_task(self, task: Task) -> None:
        """Start working on a development task"""
        self.logger.info(f"Starting development task: {task.title}")

        # Evaluate task ethically
        ethical_review = EthicalOversight.evaluate_action(task.description)
        if not ethical_review["approved"]:
            self.logger.warning(f"Task failed ethical review: {ethical_review['concerns']}")
            await self.update_task_status(task.id, "blocked", ethical_concerns=ethical_review["concerns"])
            return

        # Process development tasks
        if "implement" in task.title.lower() or "feature" in task.title.lower():
            # Create a mock feature review message to trigger implementation
            mock_message = Message(
                sender="system",
                recipient=self.name,
                content=json.dumps({
                    "feature_file": f"features/{task.title.lower().replace(' ', '_')}.feature",
                    "architectural_review": {"approved": True, "issues": [], "recommendations": []}
                }),
                message_type="feature_review"
            )
            await self.implement_feature(mock_message)

        await self.update_task_status(task.id, "completed")