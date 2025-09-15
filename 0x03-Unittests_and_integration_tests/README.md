# Unittests and Integration Tests

This project covers writing unit tests and integration tests in Python using the `unittest` framework and `parameterized`.

## Progress

###  Task 0: Parameterize a unit test
- Implemented `TestAccessNestedMap.test_access_nested_map`  
- Verified `access_nested_map` returns correct results for different nested maps and paths.  
- Used `@parameterized.expand` to cover multiple test cases in one method.

###  Task 1: Parameterize unit test for exceptions
- Implemented `TestAccessNestedMap.test_access_nested_map_exception`  
- Verified that `KeyError` is raised for invalid paths.  
- Asserted that the exception message matches the missing key.  

## Running Tests
Run all tests with:
```bash
python -m unittest discover 0x03-Unittests_and_integration_tests -p "test_*.py" -v
