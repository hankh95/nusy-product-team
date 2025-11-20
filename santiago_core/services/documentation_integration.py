#!/usr/bin/env python3
"""
Documentation Automation Integration

This script demonstrates how the automated documentation system integrates
with the kanban workflow to keep documentation synchronized with development.

Key integration points:
- Feature start: Generate documentation stubs
- Feature complete: Generate comprehensive feature docs
- Code review: Update API documentation
- Workflow transitions: Auto-update README and cross-references
"""

import asyncio
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

from santiago_core.services.documentation_service import DocumentationAutomationService


class DocumentationWorkflowIntegration:
    """Integration layer between kanban workflow and documentation automation"""

    def __init__(self, workspace_path: Path):
        self.workspace_path = workspace_path
        self.docs_service = DocumentationAutomationService(workspace_path)

    async def on_kanban_transition(self, transition_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle kanban workflow transitions and trigger appropriate documentation actions

        This method is called whenever a card moves between kanban columns.
        It determines what documentation actions should be taken based on the transition.
        """
        board_id = transition_data["board_id"]
        card_id = transition_data["card_id"]
        from_column = transition_data["from_column"]
        to_column = transition_data["to_column"]
        card_data = transition_data.get("card_data", {})

        actions_taken = []
        transition_type = self._classify_transition(from_column, to_column, card_data)

        print(f"📝 Processing documentation for transition: {from_column} → {to_column} ({transition_type})")

        # Call the documentation service
        result = await self.docs_service.handle_tool_call("docs_on_kanban_transition", {
            "board_id": board_id,
            "card_id": card_id,
            "from_column": from_column,
            "to_column": to_column,
            "transition_type": transition_type
        })

        if result.error:
            print(f"❌ Documentation automation error: {result.error}")
            return {"success": False, "error": result.error}

        # Additional actions based on transition type
        if transition_type == "feature_start":
            actions_taken.extend(await self._handle_feature_start(card_data))

        elif transition_type == "feature_complete":
            actions_taken.extend(await self._handle_feature_complete(card_data))

        elif transition_type == "code_review":
            actions_taken.extend(await self._handle_code_review(card_data))

        elif transition_type == "deployment_ready":
            actions_taken.extend(await self._handle_deployment_ready(card_data))

        # Update project README if significant changes occurred
        if actions_taken and len(actions_taken) > 0:
            await self._update_project_readme()

        return {
            "success": True,
            "transition_type": transition_type,
            "actions_taken": actions_taken,
            "documentation_updated": True
        }

    def _classify_transition(self, from_column: str, to_column: str, card_data: Dict[str, Any]) -> str:
        """Classify the type of workflow transition"""
        transition_map = {
            ("backlog", "ready"): "feature_planned",
            ("ready", "in_progress"): "feature_start",
            ("in_progress", "review"): "code_complete",
            ("review", "done"): "feature_complete",
            ("in_progress", "done"): "feature_complete",
            ("review", "in_progress"): "code_review",
            ("done", "deployed"): "deployment_ready"
        }

        return transition_map.get((from_column, to_column), "transition")

    async def _handle_feature_start(self, card_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Handle documentation actions when a feature starts development"""
        actions = []

        # Generate initial documentation stub
        feature_id = card_data.get("item_id", "unknown")
        title = card_data.get("title", "Unknown Feature")

        print(f"📝 Generating documentation stub for feature: {title}")

        # Create a basic feature documentation stub
        stub_content = f"""# {title}

**Feature ID:** {feature_id}
**Status:** In Development
**Started:** {datetime.now().strftime('%Y-%m-%d')}

## Overview

{card_data.get('description', 'Feature description to be updated during development.')}

## Implementation Plan

- [ ] Requirements analysis
- [ ] Design specification
- [ ] Code implementation
- [ ] Testing
- [ ] Documentation completion

## Files to be Created/Modified

*To be populated during development*

## API Changes

*To be documented as implemented*

---

*This documentation will be automatically updated as the feature progresses through the development workflow.*
"""

        # Save stub documentation
        docs_dir = self.workspace_path / "docs" / "features"
        docs_dir.mkdir(parents=True, exist_ok=True)
        stub_file = docs_dir / f"{feature_id}_stub.md"
        stub_file.write_text(stub_content)

        actions.append({
            "action": "feature_stub_created",
            "file": str(stub_file),
            "feature_id": feature_id
        })

        return actions

    async def _handle_feature_complete(self, card_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Handle documentation actions when a feature is completed"""
        actions = []

        feature_id = card_data.get("item_id", "unknown")
        implementation_files = card_data.get("implementation_files", [])

        print(f"📝 Generating comprehensive documentation for completed feature: {feature_id}")

        # Generate comprehensive feature documentation
        result = await self.docs_service.handle_tool_call("docs_generate_feature_docs", {
            "feature_id": feature_id,
            "implementation_files": implementation_files,
            "output_dir": "docs/features"
        })

        if not result.error:
            actions.append({
                "action": "feature_docs_completed",
                "feature_id": feature_id,
                "docs_file": result.result.get("feature_docs_generated")
            })

        # Update API documentation if this feature introduced API changes
        if self._feature_has_api_changes(card_data):
            api_result = await self.docs_service.handle_tool_call("docs_generate_api_docs", {
                "source_path": "src",
                "output_path": "docs/api-reference/generated-api.md",
                "include_private": False
            })

            if not api_result.error:
                actions.append({
                    "action": "api_docs_updated",
                    "api_docs_file": api_result.result.get("api_docs_generated")
                })

        return actions

    async def _handle_code_review(self, card_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Handle documentation actions during code review"""
        actions = []

        print("📝 Performing documentation review and validation")

        # Validate documentation links
        link_result = await self.docs_service.handle_tool_call("docs_validate_links", {
            "docs_path": "docs",
            "fix_broken": True
        })

        if not link_result.error:
            broken_links = link_result.result.get("broken_links", 0)
            fixes_applied = link_result.result.get("fixes_applied", 0)

            actions.append({
                "action": "links_validated",
                "broken_links_found": broken_links,
                "fixes_applied": fixes_applied
            })

        # Generate documentation quality metrics
        metrics_result = await self.docs_service.handle_tool_call("docs_quality_metrics", {
            "docs_path": "docs",
            "source_path": "src"
        })

        if not metrics_result.error:
            actions.append({
                "action": "quality_metrics_generated",
                "coverage": metrics_result.result.get("documentation_coverage", 0),
                "quality_score": metrics_result.result.get("quality_score", 0)
            })

        return actions

    async def _handle_deployment_ready(self, card_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Handle documentation actions when feature is ready for deployment"""
        actions = []

        print("📝 Preparing deployment documentation")

        # Update changelog or release notes
        await self._update_changelog(card_data)

        # Generate deployment documentation if needed
        if self._feature_requires_deployment_docs(card_data):
            actions.append({
                "action": "deployment_docs_prepared",
                "feature_id": card_data.get("item_id")
            })

        return actions

    async def _update_project_readme(self):
        """Update the main project README with current status"""
        result = await self.docs_service.handle_tool_call("docs_update_readme", {
            "readme_path": "README.md"
        })

        if result.error:
            print(f"⚠️  Failed to update README: {result.error}")
        else:
            print("✅ Project README updated with latest documentation links")

    def _feature_has_api_changes(self, card_data: Dict[str, Any]) -> bool:
        """Determine if a feature introduces API changes"""
        # Simple heuristic - check if any implementation files contain API-related patterns
        implementation_files = card_data.get("implementation_files", [])
        api_keywords = ["api", "endpoint", "route", "controller", "service"]

        for file_path in implementation_files:
            if any(keyword in file_path.lower() for keyword in api_keywords):
                return True

        return False

    def _feature_requires_deployment_docs(self, card_data: Dict[str, Any]) -> bool:
        """Determine if a feature requires deployment documentation"""
        # Check feature type or tags
        item_type = card_data.get("item_type", "")
        return item_type in ["feature", "epic"] or "infrastructure" in card_data.get("tags", [])

    async def _update_changelog(self, card_data: Dict[str, Any]):
        """Update project changelog"""
        # This would append to a CHANGELOG.md file
        # For now, just print what would be done
        feature_title = card_data.get("title", "Unknown feature")
        print(f"📝 Would update CHANGELOG.md with: '{feature_title}' completed")

    async def run_documentation_audit(self) -> Dict[str, Any]:
        """Run a comprehensive documentation audit"""
        print("🔍 Running comprehensive documentation audit...")

        # Scan codebase for documentation issues
        scan_result = await self.docs_service.handle_tool_call("docs_scan_codebase", {
            "source_paths": ["src", "santiago_core"],
            "output_report": "docs/audit-report.md"
        })

        # Generate quality metrics
        metrics_result = await self.docs_service.handle_tool_call("docs_quality_metrics", {
            "docs_path": "docs",
            "source_path": "src"
        })

        # Validate all links
        link_result = await self.docs_service.handle_tool_call("docs_validate_links", {
            "docs_path": "docs",
            "fix_broken": False
        })

        return {
            "audit_completed": True,
            "issues_found": scan_result.result.get("issues_found", 0) if not scan_result.error else 0,
            "documentation_coverage": metrics_result.result.get("documentation_coverage", 0) if not metrics_result.error else 0,
            "broken_links": link_result.result.get("broken_links", 0) if not link_result.error else 0,
            "quality_score": metrics_result.result.get("quality_score", 0) if not metrics_result.error else 0
        }

    async def auto_update_documentation(self, changed_files: List[str]) -> Dict[str, Any]:
        """Automatically update documentation based on code changes"""
        print(f"🔄 Auto-updating documentation for {len(changed_files)} changed files...")

        # Sync documentation with code changes
        sync_result = await self.docs_service.handle_tool_call("docs_sync_with_code", {
            "changed_files": changed_files,
            "docs_path": "docs"
        })

        # Update README if needed
        await self._update_project_readme()

        return {
            "sync_completed": not sync_result.error,
            "updates_made": sync_result.result.get("documentation_updates", 0) if not sync_result.error else 0
        }


# Integration hooks for kanban workflow
async def on_card_transition(transition_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Hook function called by kanban system when cards transition

    This function should be registered with the kanban service to enable
    automatic documentation updates during workflow transitions.
    """
    workspace_path = Path.cwd()  # Or get from config
    integration = DocumentationWorkflowIntegration(workspace_path)

    return await integration.on_kanban_transition(transition_data)


# CLI interface for manual documentation operations

# CLI interface for manual documentation operations
async def main():
    """CLI interface for documentation automation"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python documentation_integration.py <command> [args...]")
        print("Commands:")
        print("  audit                    - Run documentation audit")
        print("  update-readme           - Update project README")
        print("  generate-api-docs       - Generate API documentation")
        print("  validate-links          - Validate documentation links")
        print("  quality-metrics         - Show documentation quality metrics")
        return

    workspace_path = Path.cwd()
    integration = DocumentationWorkflowIntegration(workspace_path)

    command = sys.argv[1]

    try:
        if command == "audit":
            result = await integration.run_documentation_audit()
            print("📊 Documentation Audit Results:")
            print(f"  Issues Found: {result['issues_found']}")
            print(f"  Coverage: {result['documentation_coverage']:.1f}%")
            print(f"  Broken Links: {result['broken_links']}")
            print(f"  Quality Score: {result['quality_score']:.1f}/100")

        elif command == "update-readme":
            await integration._update_project_readme()
            print("✅ README updated")

        elif command == "generate-api-docs":
            result = await integration.docs_service.handle_tool_call("docs_generate_api_docs", {
                "source_path": "src",
                "output_path": "docs/api-reference/generated-api.md",
                "include_private": False
            })
            if result.error:
                print(f"❌ Error: {result.error}")
            else:
                print(f"✅ API docs generated: {result.result['api_docs_generated']}")

        elif command == "validate-links":
            result = await integration.docs_service.handle_tool_call("docs_validate_links", {
                "docs_path": "docs",
                "fix_broken": True
            })
            if result.error:
                print(f"❌ Error: {result.error}")
            else:
                print(f"✅ Links validated. Broken: {result.result['broken_links']}, Fixed: {result.result['fixes_applied']}")

        elif command == "quality-metrics":
            result = await integration.docs_service.handle_tool_call("docs_quality_metrics", {
                "docs_path": "docs",
                "source_path": "src"
            })
            if result.error:
                print(f"❌ Error: {result.error}")
            else:
                print("📊 Documentation Quality Metrics:")
                coverage = result.result.get('documentation_coverage', 0)
                quality_score = result.result.get('quality_score', 0)
                total_docs = result.result.get('total_doc_files', 0)
                code_with_docs = result.result.get('code_files_with_docs', 0)
                print(f"  Coverage: {coverage:.1f}%")
                print(f"  Quality Score: {quality_score:.1f}/100")
                print(f"  Doc Files: {total_docs}")
                print(f"  Code Files with Docs: {code_with_docs}")

        else:
            print(f"Unknown command: {command}")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())


# CLI interface for manual documentation operations
async def main():
    """CLI interface for documentation automation"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python documentation_integration.py <command> [args...]")
        print("Commands:")
        print("  audit                    - Run documentation audit")
        print("  update-readme           - Update project README")
        print("  generate-api-docs       - Generate API documentation")
        print("  validate-links          - Validate documentation links")
        print("  quality-metrics         - Show documentation quality metrics")
        return

    workspace_path = Path.cwd()
    integration = DocumentationWorkflowIntegration(workspace_path)

    command = sys.argv[1]

    try:
        if command == "audit":
            result = await integration.run_documentation_audit()
            print("📊 Documentation Audit Results:")
            print(f"  Issues Found: {result['issues_found']}")
            print(f"  Coverage: {result['documentation_coverage']:.1f}%")
            print(f"  Broken Links: {result['broken_links']}")
            print(f"  Quality Score: {result['quality_score']:.1f}/100")

        elif command == "update-readme":
            await integration._update_project_readme()
            print("✅ README updated")

        elif command == "generate-api-docs":
            result = await integration.docs_service.handle_tool_call("docs_generate_api_docs", {
                "source_path": "src",
                "output_path": "docs/api-reference/generated-api.md",
                "include_private": False
            })
            if result.error:
                print(f"❌ Error: {result.error}")
            else:
                print(f"✅ API docs generated: {result.result['api_docs_generated']}")

        elif command == "validate-links":
            result = await integration.docs_service.handle_tool_call("docs_validate_links", {
                "docs_path": "docs",
                "fix_broken": True
            })
            if result.error:
                print(f"❌ Error: {result.error}")
            else:
                print(f"✅ Links validated. Broken: {result.result['broken_links']}, Fixed: {result.result['fixes_applied']}")

        elif command == "quality-metrics":
            result = await integration.docs_service.handle_tool_call("docs_quality_metrics", {
                "docs_path": "docs",
                "source_path": "src"
            })
            if result.error:
                print(f"❌ Error: {result.error}")
            else:
                print("📊 Documentation Quality Metrics:")
                coverage = result.result.get('documentation_coverage', 0)
                quality_score = result.result.get('quality_score', 0)
                total_docs = result.result.get('total_doc_files', 0)
                code_with_docs = result.result.get('code_files_with_docs', 0)
                print(f"  Coverage: {coverage:.1f}%")
                print(f"  Quality Score: {quality_score:.1f}/100")
                print(f"  Doc Files: {total_docs}")
                print(f"  Code Files with Docs: {code_with_docs}")

        else:
            print(f"Unknown command: {command}")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
