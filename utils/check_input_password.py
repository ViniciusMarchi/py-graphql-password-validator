"""
Checks if a password received as input is in a valid format.

Args:
password (str): The password to check.

Raises:
ValueError: If the password is None.
"""
def hasInvalidInputPassword(password):
    # password may be an empty string, but it cannot be None.
    if password is None:
        raise ValueError('Invalid input. The password must be provided')