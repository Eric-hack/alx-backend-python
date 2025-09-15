# Unittests and Integration Tests

This project covers writing unittests and integration tests in Python using the `unittest` framework, `parameterized`, and `unittest.mock`.

## Tasks Completed

### 0. Parameterize a Unit Test
- Implemented tests for `utils.access_nested_map`.
- Used `@parameterized.expand` to test multiple inputs and expected outputs.
- Verified correct results and raised `KeyError` for invalid paths.

### 1. Parameterize a Unit Test (Exceptions)
- Added tests for invalid paths in `access_nested_map`.
- Confirmed that `KeyError` is raised with the correct exception message.

### 2. Mock HTTP Calls
- Wrote tests for `utils.get_json`.
- Patched `requests.get` using `unittest.mock.patch` to avoid real HTTP calls.
- Verified:
  - `requests.get` is called exactly once with the expected URL.
  - The returned payload matches the mocked response.

## Running Tests
Run all tests with:

```bash
python -m unittest discover 0x03-Unittests_and_integration_tests -p "test_*.py" -v
