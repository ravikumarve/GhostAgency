# Ghost Agency Dashboard Test Suite

This directory contains comprehensive test scripts for the Ghost Agency dashboard.

## Files

- `test_dashboard.py` - Main test script using FastAPI TestClient
- `test_dashboard_integration.py` - Integration test with live server
- `dashboard_test_results.json` - JSON output from test runs
- `DASHBOARD_TEST_README.md` - This file

## Usage

### Quick Test (Recommended)
```bash
python3 test_dashboard.py
```

This uses FastAPI's TestClient to test all dashboard routes without starting a server.

### Integration Test
```bash
python3 test_dashboard_integration.py
```

This starts the actual server and tests endpoints live (requires server to not already be running).

## What's Tested

1. **HTTP Routes**: All dashboard endpoints (`/`, `/agents`, `/clients`, `/stats`)
2. **Status Codes**: All routes return HTTP 200
3. **Content Types**: Proper HTML/CSS content types
4. **Template Rendering**: Jinja2 templates render correctly with context data
5. **Static Files**: CSS files are served correctly
6. **Brutalist CSS**: Specific brutalist styling patterns are present
7. **Navigation**: Links between pages work correctly
8. **Template Inheritance**: Base template structure is maintained

## Test Results

The main test script generates:
- Console output with detailed pass/fail information
- JSON file (`dashboard_test_results.json`) with structured results
- Exit code (0 = success, 1 = failures, 2 = error)

## Integration

These tests can be integrated into CI/CD pipelines. The main test script (`test_dashboard.py`) is designed to be:
- Fast (completes in seconds)
- Reliable (no external dependencies beyond FastAPI TestClient)
- Comprehensive (covers all critical dashboard functionality)
- Non-destructive (doesn't modify any data)

## Running in CI

Add to your CI pipeline:
```yaml
- name: Test Dashboard
  run: python3 test_dashboard.py
```

The script will exit with code 0 if all tests pass, making it suitable for CI gatekeeping.

## Customization

To add additional tests, modify `test_dashboard.py` and add new test cases to the `test_dashboard_routes()` function.

For testing specific edge cases or additional routes, extend the `routes_to_test` list and add appropriate assertions.