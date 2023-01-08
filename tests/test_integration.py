import sys
import os

# add the parent directory of this file to the python Search Path to help with imports
parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(parent_dir)

from schema.schema import schema
import unittest

class TestCountCharsMethods(unittest.TestCase):
    def test_query(self):
        query = """
            query{
                verify(
                    password: "TesteSenhaFortee!123&"
                    rules: [
                        {rule: "minSize", value: 8},
                        {rule: "minSpecialChars", value: 2},
                        {rule: "noRepeted", value: 0},
                        {rule: "minDigit", value: 4}
                    ])
                    {
                        verify
                        noMatch
                    }
                }
        """
        result = schema.execute_sync(query)

        self.assertIsNone(result.errors)
        self.assertEqual(result.data["verify"]['verify'], 'false')
        self.assertEqual(result.data["verify"]['noMatch'], ['noRepeted', 'minDigit'])


    def test_min_size_rule(self):
    # Test password that is too short
        query = """
            query {
                verify(
                    password: "Test12&"
                    rules: [{rule: "minSize", value: 8}]
                ) {
                    verify
                }
            }
        """
        result = schema.execute_sync(query)

        self.assertIsNone(result.errors)
        self.assertEqual(result.data["verify"]['verify'], 'false')

    def test_min_special_chars_rule(self):
        # Test password with not enough special characters
        query = """
            query {
                verify(
                    password: "Test1234"
                    rules: [{rule: "minSpecialChars", value: 2}]
                ) {
                    verify
                }
            }
        """
        result = schema.execute_sync(query)

        self.assertIsNone(result.errors)
        self.assertEqual(result.data["verify"]['verify'], 'false')

    def test_no_repeted_rule(self):
        # Test password with repeated characters
        query = """
            query {
                verify(
                    password: "Testt12&"
                    rules: [{rule: "noRepeted", value: 0}]
                ) {
                    verify
                }
            }
        """
        result = schema.execute_sync(query)

        self.assertIsNone(result.errors)
        self.assertEqual(result.data["verify"]['verify'], 'false')

    def test_min_digit_rule(self):
        # Test password with not enough digits
        query = """
            query {
                verify(
                    password: "Testt&12"
                    rules: [{rule: "minDigit", value: 4}]
                ) {
                    verify
                }
            }
        """
        result = schema.execute_sync(query)

        self.assertIsNone(result.errors)
        self.assertEqual(result.data["verify"]['verify'], 'false')