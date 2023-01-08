import os
import sys
import unittest
# add the parent directory of this file to the python Search Path to help with imports
parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(parent_dir)

from utils.check_input_password import hasInvalidInputPassword

# Test the method that validates the password format of data receive from user
# in this case, only None passwords are invalid.
class TestIsValidInputPassword(unittest.TestCase):
    # CASE 01: password is None
    def test_invalid_input_password(self):
        # unittest does nto support assert error message direclty, but support usigin a regex that
        # match the message so I format the message adding '\' character to match the special characters
        expected_error_message = "Invalid input. The password must be provided"
        with self.assertRaisesRegex(ValueError, expected_error_message):
            hasInvalidInputPassword(None)