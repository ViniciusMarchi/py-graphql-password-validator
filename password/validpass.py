import re
from strawberry.scalars import JSON

# This class contains all methods for implementing the password validation rules.
class PasswordValidator:
    def __init__(self):
        pass

    # checks if the password meets the minimum length specified by the user
    def minSize(self, password, threshold):
        return len(password) >= threshold

    # checks if the password has the minimum number of uppercase characters specified by the user
    def minUppercase(self, password, threshold):
        return self._countUppercaseChars(password) >= threshold

    # checks if the password has the minimum number of lowercase characters specified by the user
    def minLowercase(self, password, threshold):
        return self._countLowerCaseChars(password) >= threshold

    # checks if the password has the minimum number of digits specified by the user
    def minDigit(self, password, threshold):
        return self._countDigits(password) >= threshold

    # checks if the password has the minimum number of special characters specified by the user
    def minSpecialChars(self, password, threshold):
        return self._countSpecialChars(password) >= threshold

    # Verifies that the password does not contain repeating characters in a sequence.
    # Returns true if the password does not contain repeating characters and false if it does.
    def noRepeted(self, password, value=0):
        return self._isRepeat(password) is None

    # Since the user selects the password rules from a predefined set, and the data has already been
    # validated to ensure that the selected rules are allowed, we can use the technique of dynamically
    # executing functions to enforce the chosen rules. A map structure is used to index the functions
    # by name, allowing us to execute the appropriate functions based on the set of rules specified
    def mappingFunctions(self):
        return {
           'minSize': self.minSize,
           'minUppercase': self.minUppercase,
           'minLowercase': self.minLowercase,
           'minDigit': self.minDigit,
           'minSpecialChars': self.minSpecialChars,
           'noRepeted': self.noRepeted
        }

    def _countUppercaseChars(self, password):
        return len(re.findall(r'[A-Z]', password))

    def _countLowerCaseChars(self, password):
        return len(re.findall(r'[a-z]', password))

    def _countDigits(self, password):
        return len(re.findall(r'[0-9]', password))

    def _countSpecialChars(self, password):
        return len(re.findall(r'[!@#$%^&*()-+\\/{}[]', password))

    def _isRepeat(self, password):
        return re.match(r'.*(\w)(\1)', password)


"""
Validates a password against a set of rules specified by the user.

This method assumes that the password and rules have already been validated and are in the 
correct format. This validation occurs in the previous module, the resolve module, when the data
is received by the API. So this method simply checks whether the password meets the specified rules.

Args:
password (str): The password to validate.
rules (List[Dict]): A list of dictionaries containing the rules to apply to the password.

Returns:
A tuple of the form (bool, List[]), where the bool indicates if the password is
valid and the list contains the rules that the password does not match.
"""
def validPassword(password: str, rules:list[JSON]) -> tuple[bool, list]:
    noMatchRules = []
    isValidPassword = False

    validator = PasswordValidator()
    validator_mapeed_functions = validator.mappingFunctions()

    for item in rules:
        rule = item['rule']
        value = item['value']

        # call the functions dinamically
        rule_result = validator_mapeed_functions[rule](password, value)
        # if the password does not match the rule we add this rule in the noMatchRules list
        if not rule_result:
            noMatchRules.append(rule)

    # if the list of unmet rules is not empty, then the password is invalid.
    if len(noMatchRules) == 0:
        isValidPassword = True

    return isValidPassword, noMatchRules