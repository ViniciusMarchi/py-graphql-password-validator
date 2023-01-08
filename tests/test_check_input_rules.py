import os
import sys
import unittest
# add the parent directory of this file to the python Search Path to help with imports
parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(parent_dir)

from utils.check_input_rules import hasInvalidInputRules

# Tests the method that checks if the rules provided by the user are invalid input
class TestInvalidRules(unittest.TestCase):
    allowed_rules = ["minSize",
        "minUppercase",
        "minLowercase",
        "minDigit",
        "minSpecialChars",
        "noRepeted",
    ]

    # CASE 01: Rules are invalid
    def test_invalid_rule(self):
        invalid_rule = [
            {"rule": "minSize", "value": 1},
            {"rule": "invalidRule", "value": 0},
        ]

        # unittest does nto support assert error message direclty, but support usigin a regex that
        # match the message so I format the message adding '\' character to match the special characters
        excepted_error_message = "Rule\(s\) \['invalidRule'\] are not allowed.See the list of allowed rules: \['minSize', 'minUppercase', 'minLowercase', 'minDigit', 'minSpecialChars', 'noRepeted'\]"

        with self.assertRaisesRegex(Exception, excepted_error_message):
            hasInvalidInputRules(invalid_rule)

            # the error message should be the same as the expected message
            self.assertTrue(str(err.exception).find(expected_error_message))
            
    # CASE 02: None rule
    def test_none_rule(self):
        excepted_error_message = "Invalid input. The rules can not None"
        with self.assertRaisesRegex(ValueError, excepted_error_message):
            hasInvalidInputRules(None)

    # CASE 03: Rule with invalid format, e.g not <rule>:<value>
    def test_invalid_rule_format(self):
        expected_value_error_message = "Rule \{'value': 8\} is not in the expected format"
        with self.assertRaisesRegex(ValueError, expected_value_error_message):
            hasInvalidInputRules([{'value': 8}])

        expected_mindigit_error_message = "Rule \{'rule': 'minDigit'\} is not in the expected format"
        with self.assertRaisesRegex(ValueError, expected_mindigit_error_message):
            hasInvalidInputRules([{'rule': "minDigit"}])

    # CASE 04: Rule with negative <value>
    def test_invalid_value_rule(self):
        expected_error_message = "Rule\(s\) \['invalidRule2'\] are not allowed.See the list of allowed rules: \['minSize', 'minUppercase', 'minLowercase', 'minDigit', 'minSpecialChars', 'noRepeted'\]"
        with self.assertRaisesRegex(Exception, expected_error_message):
            hasInvalidInputRules([ {"rule": "invalidRule2", "value": -1}])