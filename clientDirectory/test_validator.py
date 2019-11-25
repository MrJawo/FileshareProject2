import unittest

from  clientDirectory.validator import Validator

class TestValidator(unittest.TestCase):

    def setUp(self):
        self.validator = Validator()


    def test_reject_password_is_too_short(self):

        password = 'toosho'
        validator = Validator()

        result = validator.password_is_valid(password)

        self.assertFalse(result)

    def test_reject_password_if_dont_have_both_upper_lower_case(self):

        password = 'onlylowercase'
        validator = Validator()

        result = validator.password_is_valid(password)

        self.assertFalse(result)

    def test_reject_password_if_password_have_whitespace(self):

        password = 'Password whitspace'
        validator = Validator()

        result = validator.password_is_valid(password)

        self.assertFalse(result)

    def test_accept_a_valid_password(self):

        password = 'AvalidPassword'
        validator = Validator()

        result = validator.password_is_valid(password)

        self.assertTrue(result)

