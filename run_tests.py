import unittest

# Script that run all tests
tests = unittest.TestLoader().discover('tests')
test_runner = unittest.TextTestRunner(verbosity=2)
test_runner.run(tests)