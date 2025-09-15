# 0x03. Unittests and Integration Tests

## Task 0: Parameterize a unit test
We implemented unit tests for the function `utils.access_nested_map`.

- Created `TestAccessNestedMap` class inheriting from `unittest.TestCase`.
- Used `@parameterized.expand` to test multiple input cases.
- Verified expected results with `assertEqual`.

### Example
```bash
$ python 0x03-Unittests_and_integration_tests/test_utils.py -v
test_access_nested_map_0 ... ok
test_access_nested_map_1 ... ok
test_access_nested_map_2 ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
