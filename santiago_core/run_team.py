#!/usr/bin/env python3
"""
Santiago Autonomous Development Team Runner

This script initializes and runs the Santiago autonomous development team.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import sys
from pathlib import Path

# Add the santiago-core directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from santiago_core.core.team_coordinator import SantiagoTeamCoordinator


async def main():
    """Main entry point for the Santiago autonomous development team"""
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    logger = logging.getLogger("santiago-runner")
    logger.info("Starting Santiago Autonomous Development Team")

    # Initialize the team coordinator
    workspace_path = project_root
    coordinator = SantiagoTeamCoordinator(workspace_path)

    try:
        # Initialize the team
        init_task = asyncio.create_task(coordinator.initialize_team())

        # Wait a bit for initialization
        await asyncio.sleep(2)

        # Create and assign a demo task
        await coordinator.create_demo_task()

        # Let the team run for a limited time (30 seconds for testing)
        logger.info("Team is now active. Running for 30 seconds...")

        # Run for 30 seconds then shutdown
        await asyncio.sleep(30)

        logger.info("Test run completed, shutting down...")
        await coordinator.shutdown_team()

    except Exception as e:
        logger.error(f"Error running Santiago team: {e}")
        await coordinator.shutdown_team()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())