"""
Service layer for NuSy PM core.

Currently exposes the ``ExperimentRunnerService`` used by the autonomous
multi‑agent experiment runner.
"""

from .experiment_runner import ExperimentRunnerService

__all__ = ["ExperimentRunnerService"]

"""
Nusy PM Core Services

This package contains core services for the Nusy PM system.
"""

__version__ = "1.0.0"