#!/usr/bin/env python3
"""
Final comprehensive test of Ghost Agency Dashboard
"""

from ghostagency.api.main import create_app
from fastapi.testclient import TestClient


def test_production_readiness():
    """Comprehensive test of dashboard production readiness"""

    print("=" * 70)
    print("GHOST AGENCY DASHBOARD - PRODUCTION READINESS TEST")
    print("=" * 70)

    app = create_app()
    client = TestClient(app)

    # Test suite
    tests = []

    # 1. Basic endpoint availability
    endpoints = [
        ("/", "Dashboard Home"),
        ("/agents", "Agents Management"),
        ("/clients", "Clients Management"),
        ("/stats", "Usage Statistics"),
        ("/api/v1/docs", "API Documentation"),
        ("/api/v1/health", "Health Check"),
        ("/static/css/brutalist.css", "CSS Assets"),
        ("/static/js/brutalist.js", "JS Assets"),
    ]

    for endpoint, description in endpoints:
        try:
            response = client.get(endpoint)
            success = response.status_code == 200
            tests.append(
                (f"Endpoint: {description}", success, f"Status: {response.status_code}")
            )
        except Exception as e:
            tests.append((f"Endpoint: {description}", False, f"Error: {e}"))

    # 2. Content validation
    try:
        response = client.get("/")
        content = response.text

        # Check for key elements
        has_title = "Ghost Agency" in content
        has_grid = "grid" in content
        has_cards = "card" in content
        has_data = "data-value" in content

        tests.append(("Content: Title present", has_title, ""))
        tests.append(("Content: Grid layout", has_grid, ""))
        tests.append(("Content: Card components", has_cards, ""))
        tests.append(("Content: Data values", has_data, ""))

    except Exception as e:
        tests.append(("Content validation", False, f"Error: {e}"))

    # 3. Static assets
    try:
        css_response = client.get("/static/css/brutalist.css")
        js_response = client.get("/static/js/brutalist.js")

        css_ok = css_response.status_code == 200 and len(css_response.text) > 0
        js_ok = js_response.status_code == 200 and len(js_response.text) > 0

        tests.append(
            ("Assets: CSS files", css_ok, f"Size: {len(css_response.text)} bytes")
        )
        tests.append(
            ("Assets: JS files", js_ok, f"Size: {len(js_response.text)} bytes")
        )

    except Exception as e:
        tests.append(("Static assets", False, f"Error: {e}"))

    # 4. API routes (require authentication)
    try:
        api_response = client.get("/api/v1/health")
        tests.append(
            (
                "API: Health endpoint",
                api_response.status_code == 200,
                f"Status: {api_response.status_code}",
            )
        )
    except Exception as e:
        tests.append(("API: Health endpoint", False, f"Error: {e}"))

    # API endpoints that require auth should return 401 (Unauthorized) not 404
    try:
        api_response = client.get("/api/v1/agents")
        tests.append(
            (
                "API: Agents endpoint (auth required)",
                api_response.status_code == 401,
                f"Status: {api_response.status_code}",
            )
        )
    except Exception as e:
        tests.append(("API: Agents endpoint", False, f"Error: {e}"))

    # Results
    print("\nTEST RESULTS:")
    print("-" * 50)

    all_passed = True
    for test_name, passed, details in tests:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
        if details:
            print(f"    {details}")
        if not passed:
            all_passed = False

    print("-" * 50)

    if all_passed:
        print("🎉 PRODUCTION READY!")
        print("All tests passed. The dashboard is ready for deployment.")
        print("\nDeployment options:")
        print(
            "1. Gunicorn + Uvicorn: gunicorn ghostagency.api.main:app -k uvicorn.workers.UvicornWorker"
        )
        print("2. Docker: Build with Dockerfile and deploy to container platform")
        print("3. Systemd: Create service file for production deployment")
    else:
        print("❌ NOT PRODUCTION READY")
        print("Some tests failed. Review the errors above.")

    print("=" * 70)

    return all_passed


if __name__ == "__main__":
    test_production_readiness()
