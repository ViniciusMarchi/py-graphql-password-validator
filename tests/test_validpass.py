import os
import sys
import unittest

# add the parent directory of this file to the python Search Path to help with imports
parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(parent_dir)

from password.validpass import PasswordValidator, validPassword

# Tests the validation password proccess
class TestCountCharsMethods(unittest.TestCase):
    validator = PasswordValidator()
    
    # Tests the number of uppercase characters in a password
    def test_count_uppercase_chars(self):
        # CASE 01: empty password
        self.assertEqual(self.validator._countUppercaseChars(''), 0)

        # CASE 02: password with no uppercase characters
        self.assertEqual(self.validator._countUppercaseChars('senha'), 0)

        # CASE 03: password with only one uppercase character
        self.assertEqual(self.validator._countUppercaseChars('Senha'), 1)

        # CASE 04: password with multiple uppercase characters
        self.assertEqual(self.validator._countUppercaseChars('SENHA'), 5)


    # Tests the number of lowercase characters in a password
    def test_count_lowercase_chars(self):
        # CASE 01: empty password
        self.assertEqual(self.validator._countLowerCaseChars(''), 0)

        # CASE 02: password without any lowercase characters
        self.assertEqual(self.validator._countLowerCaseChars('SENHA'), 0)

        # CASE 03: password with only one lowercase character
        self.assertEqual(self.validator._countLowerCaseChars('SeNHA'), 1)

        # CASE 04: password with multiple lowercase characters
        self.assertEqual(self.validator._countLowerCaseChars('senhat'), 6)


    # Tests a password's digit count
    def test_count_digits(self):
        # CASE 01: an empty password
        self.assertEqual(self.validator._countDigits(''), 0)

        # CASE 02: a password without digits
        self.assertEqual(self.validator._countDigits('senha'), 0)

        # CASE 03: a multi-digit password
        self.assertEqual(self.validator._countDigits('s3nh4'), 2)


    # Tests the count of special characters in a password
    def test_count_special_chars(self):
        # CASE 01: empty password
        self.assertEqual(self.validator._countSpecialChars(''), 0)

        # CASE 02: senha sem caracteres especiais
        self.assertEqual(self.validator._countSpecialChars('senha'), 0)

        # CASE 03: Testa em uma senha com apenas um caractere especial
        self.assertEqual(self.validator._countSpecialChars('senha!'), 1)

        # CASE 04: Testa em uma senha com múltiplos caracteres especiais
        self.assertEqual(self.validator._countSpecialChars('p$#0!d'), 3)


    def test_is_repeat(self):
        # CASE 01: empty password
        self.assertFalse(self.validator._isRepeat(''))

        # CASE 02: password without repeating characters
        self.assertFalse(self.validator._isRepeat('senha'))

        # CASE 03: password with a repeat
        self.assertTrue(self.validator._isRepeat('seenha'))

        # CASE 04: password with several repetitions
        self.assertTrue(self.validator._isRepeat('see nhaaaa'))


    def test_min_size(self):
        # CASE 01: empty password
        self.assertFalse(self.validator.minSize('', 10))

        # CASE 02: password length smaller than the given limit
        self.assertFalse(self.validator.minSize('senha', 10))

        # CASE 03: password with the same length as the given limit
        self.assertTrue(self.validator.minSize('se nh at', 8))

        # CASE 04: password length greater than the given limit
        self.assertTrue(self.validator.minSize('senha', 1))

    def test_min_uppercase(self):
        # CASE 01: empty password
        self.assertFalse(self.validator.minUppercase('', 1))

        # CASE 02: password with fewer uppercase characters than the specified limit
        self.assertFalse(self.validator.minUppercase('se', 2))

        # CASE 03: password with the number of uppercase characters equal to the given limit
        self.assertTrue(self.validator.minUppercase('SenhA', 2))

        # CASE 04: password with a number of uppercase characters greater than the specified limit
        self.assertTrue(self.validator.minUppercase('SENHATESTE', 7))

    def test_min_lowercase(self):
        # CASE 01: empty password
        self.assertFalse(self.validator.minLowercase('', 1))

        # CASE 02: password with a number of lowercase characters less than the given limit
        self.assertFalse(self.validator.minLowercase('SENhA', 2))

        # CASE 03: password with the number of lowercase characters equal to the given limit
        self.assertTrue(self.validator.minLowercase('SenHA', 2))

        # CASE 04: password with a number of lowercase characters greater than the given limit
        self.assertTrue(self.validator.minLowercase('senhateste', 7))

    def test_min_digit(self):
        # CASE 01: empty password
        self.assertFalse(self.validator.minDigit('', 1))

        # CASE 02: password with fewer digits than the given limit
        self.assertFalse(self.validator.minDigit('a', 2))

        # CASE 03: password with more digits than the given limit
        self.assertTrue(self.validator.minDigit('sa#qwqd23!', 2))

    def test_min_special_chars(self):
        # CASE 01: empty password
        self.assertFalse(self.validator.minSpecialChars('', 1))

        # CASE 02: password with fewer special characters than specified
        self.assertFalse(self.validator.minSpecialChars('senha', 2))

        # CASE 03: password with the same number of specified special characters
        self.assertTrue(self.validator.minSpecialChars('senha!d$', 2))

        # CASE 04: password with more than specified number of special characters
        self.assertTrue(self.validator.minSpecialChars('!@#!senha', 1))

    def test_no_repeted(self):
        # CASE 01: empty password
        self.assertTrue(self.validator.noRepeted('', 0))

        # CASE 02: password with repeated sequential characters
        self.assertFalse(self.validator.noRepeted('seenha', 0))


    def test_valid_password(self):
        # CASE 01: empty password
        verify, noMatch = validPassword('', [])
        self.assertTrue(verify)
        self.assertEqual(noMatch, [])

        # CASE 02: password that does not comply with the defined rules
        verify, noMatch = validPassword('minhaSenha', [
            {'rule': 'minSize', 'value': 8},
            {'rule': 'minUppercase', 'value': 1},
            {'rule': 'minLowercase', 'value': 1},
            {'rule': 'minDigit', 'value': 1},
            {'rule': 'minSpecialChars', 'value': 1},
            {'rule': 'noRepeted', 'value': 0},
        ])
        self.assertFalse(verify)
        self.assertEqual(noMatch, ['minDigit', 'minSpecialChars'])

        # CASE 03: password that respects all defined rules
        verify, noMatch = validPassword('Senh4#$1234', [
            {'rule': 'minSize', 'value': 8},
            {'rule': 'minUppercase', 'value': 1},
            {'rule': 'minLowercase', 'value': 1},
            {'rule': 'minDigit', 'value': 1},
            {'rule': 'minSpecialChars', 'value': 1},
            {'rule': 'noRepeted', 'value': 0},
        ])
        self.assertTrue(verify)
        self.assertEqual(noMatch, [])