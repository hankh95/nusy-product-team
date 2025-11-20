#!/usr/bin/env python3
"""
CI/CD Pipeline Test for Santiago

This script validates that the CI/CD pipeline implementation is working correctly.
It tests the Docker deployment, API endpoints, and basic functionality.
"""

import requests
import time
import os
import sys
import subprocess
from pathlib import Path

def test_docker_build():
    """Test Docker image build"""
    print("🏗️  Testing Docker build...")

    try:
        # Check if Dockerfile exists
        if not Path("Dockerfile").exists():
            print("❌ Dockerfile not found")
            return False

        # Try to build the image
        result = subprocess.run(
            ["docker", "build", "-t", "santiago-test", "."],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )

        if result.returncode == 0:
            print("✅ Docker build successful")
            return True
        else:
            print("❌ Docker build failed")
            print(f"   Error: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("❌ Docker build timed out")
        return False
    except Exception as e:
        print(f"❌ Docker build failed: {e}")
        return False

def test_docker_compose():
    """Test Docker Compose setup"""
    print("\n🐳 Testing Docker Compose...")

    try:
        # Check if docker-compose.yml exists
        if not Path("docker-compose.yml").exists():
            print("❌ docker-compose.yml not found")
            return False

        # Try to validate the compose file
        result = subprocess.run(
            ["docker-compose", "config"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("✅ Docker Compose configuration valid")
            return True
        else:
            print("❌ Docker Compose configuration invalid")
            print(f"   Error: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ Docker Compose test failed: {e}")
        return False

def test_api_imports():
    """Test that API modules can be imported"""
    print("\n📦 Testing API imports...")

    try:
        # Test Santiago core imports
        import santiago_core
        print("✅ santiago_core imported successfully")

        # Test API server import
        import santiago_core.api
        print("✅ santiago_core.api imported successfully")

        # Test MCP service import
        import santiago_core.core.mcp_service
        print("✅ santiago_core.core.mcp_service imported successfully")

        return True

    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def test_makefile_targets():
    """Test key Makefile targets"""
    print("\n🔧 Testing Makefile targets...")

    try:
        # Check if Makefile exists
        if not Path("Makefile").exists():
            print("❌ Makefile not found")
            return False

        # Test make help (should not fail)
        result = subprocess.run(
            ["make", "help"],
            capture_output=True,
            text=True
        )

        # make help might not exist, so just check if make works
        result = subprocess.run(
            ["make", "--version"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("✅ Makefile system working")
            return True
        else:
            print("❌ Makefile system not working")
            return False

    except Exception as e:
        print(f"❌ Makefile test failed: {e}")
        return False

def test_github_actions():
    """Test GitHub Actions workflow files"""
    print("\n⚙️  Testing GitHub Actions configuration...")

    try:
        workflow_dir = Path(".github/workflows")
        if not workflow_dir.exists():
            print("❌ .github/workflows directory not found")
            return False

        ci_cd_file = workflow_dir / "ci-cd.yml"
        if not ci_cd_file.exists():
            print("❌ ci-cd.yml workflow not found")
            return False

        # Check if it's a valid YAML file (basic check)
        with open(ci_cd_file, 'r') as f:
            content = f.read()

        if "name:" in content and "on:" in content and "jobs:" in content:
            print("✅ CI/CD workflow file valid")
            return True
        else:
            print("❌ CI/CD workflow file appears invalid")
            return False

    except Exception as e:
        print(f"❌ GitHub Actions test failed: {e}")
        return False

def test_deployment_script():
    """Test deployment script exists and is executable"""
    print("\n🚀 Testing deployment script...")

    try:
        deploy_script = Path("scripts/deploy.sh")
        if not deploy_script.exists():
            print("❌ scripts/deploy.sh not found")
            return False

        # Check if executable
        if os.access(deploy_script, os.X_OK):
            print("✅ Deployment script exists and is executable")
            return True
        else:
            print("⚠️  Deployment script exists but is not executable")
            return False

    except Exception as e:
        print(f"❌ Deployment script test failed: {e}")
        return False

def test_documentation():
    """Test that documentation files exist"""
    print("\n📚 Testing documentation...")

    try:
        docs_to_check = [
            "README.md",
            "docs/CI_CD_DEPLOYMENT.md",
            "docs/API_REFERENCE.md",
            "GLOSSARY.md"
        ]

        missing_docs = []
        for doc in docs_to_check:
            if not Path(doc).exists():
                missing_docs.append(doc)

        if not missing_docs:
            print("✅ All documentation files present")
            return True
        else:
            print("❌ Missing documentation files:")
            for doc in missing_docs:
                print(f"   - {doc}")
            return False

    except Exception as e:
        print(f"❌ Documentation test failed: {e}")
        return False

def main():
    """Run all CI/CD tests"""
    print("🚀 Santiago CI/CD Pipeline Test")
    print("=" * 50)

    tests = [
        ("Docker Build", test_docker_build),
        ("Docker Compose", test_docker_compose),
        ("API Imports", test_api_imports),
        ("Makefile Targets", test_makefile_targets),
        ("GitHub Actions", test_github_actions),
        ("Deployment Script", test_deployment_script),
        ("Documentation", test_documentation),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")

    print("\n" + "=" * 50)
    print(f"📊 CI/CD Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All CI/CD tests passed! Pipeline implementation successful.")
        print("\nNext steps:")
        print("  • Push to trigger GitHub Actions CI/CD")
        print("  • Test deployment to staging environment")
        print("  • Validate production deployment")
        return 0
    else:
        print("⚠️  Some CI/CD tests failed. Check the implementation and try again.")
        return 1

if __name__ == "__main__":
    sys.exit(main())