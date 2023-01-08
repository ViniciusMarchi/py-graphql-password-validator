allowed_rules = ["minSize",
	"minUppercase",
	"minLowercase",
	"minDigit",
	"minSpecialChars",
	"noRepeted",
]


"""
Checks if the rules are in the expected format. Each rule should be a dictionary with
keys 'rule' and 'value', like so: { 'rule': <rule>, 'value': <value> }. If the 'value'
field is not specified, the rule is considered invalid.

This function also checks if the values of the rules are valid. For example, a rule with
a negative value such as { 'rule': 'minDigit', 'value': -1 } is invalid because it does
not make sense to require a password to have a negative number of digits.

Args:
    rules (List[Dict]): A list of rules to check.

Raises:
    ValueError: If any of the rules are not in the correct format or if the input is None.
    Exception: If any of the rules are not in the list of allowed rules.
"""
def hasInvalidInputRules(rules):
    # the rules can be empty, e.g [], but can't be None
    if rules is None:
        raise ValueError('Invalid input. The rules can not None')
    
    invalid_rules = []
    for x in rules:
        # check if the rule format is correct, e.g {rule: <regra>, value: <valor>}
        if 'rule' not in x or 'value' not in x:
            raise ValueError(f'Rule {x} is not in the expected format')
    
        # checks if the rule is among the accepted rules, if it is not, adds it to the list of invalid rules.
        if x["rule"] not in allowed_rules:
            invalid_rules.append(x["rule"])

    # if the list of invalid rules is not empty, then the user provided invalid rules
    if (len(invalid_rules) > 0):
        raise Exception(f"Rule(s) {invalid_rules} are not allowed."+ 
            f"See the list of allowed rules: {allowed_rules}")


"""
Checks if any of the values in the provided list of rules is less than zero.

Args:
    rules: A list of rules to check.

Raises:
    Exception: If any of the values in the rules are less than zero.
"""
def hasInvalidInputRuleValues(rules):
    if any(x["value"] < 0 for x in rules):
        raise Exception("Negative values are not allowed in rules")