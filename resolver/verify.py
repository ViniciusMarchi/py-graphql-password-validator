import sys
import os

# add the parent directory of this file to the python Search Path to help with imports
parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(parent_dir)

from model import password_info
from strawberry.scalars import JSON
from password.validpass import validPassword
from utils.check_input_rules import hasInvalidInputRules, hasInvalidInputRuleValues
from utils.check_input_password import hasInvalidInputPassword


"""
validadePass is a resolver function that is called when the user performs the "verify" query.
This function first validates the input data and reports any errors to the user. If the input
data is valid, the password validation process is performed and the result is returned to the
user as a PasswordInfo object, defined in the schema.

Args:
password (str): The password to validate.
rules (List[Dict]): A list of dictionaries containing the rules to apply to the password.

Returns:
A PasswordInfo object containing the result of the validation.

Raises:
Exception: If any of the rules are not allowed.
Exception: If any value of any rule is negative.
Exception: If the password is None.
"""
def validadePass(password: str, rules: list[JSON]):
    hasInvalidInputRules(rules)
    hasInvalidInputRuleValues(rules)
    hasInvalidInputPassword(password)
    
    verify_result, no_match_list = validPassword(password, rules)
    return password_info.PasswordInfo(verify=verify_result, noMatch=no_match_list)
