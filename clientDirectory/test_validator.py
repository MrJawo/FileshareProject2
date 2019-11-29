import unittest
from clientDirectory.validator import Validator


class TestValidator(unittest.TestCase):

    def setUp(self):
        self.validator = Validator()
        print('setUp')

    def tearDown(self):
        pass

    def test_reject_password_is_too_short(self):

        password = 'Short'

        result = self.validator.password_is_valid(password)

        self.assertFalse(result)

    def test_reject_password_if_dont_have_both_upper_lower_case(self):

        password = 'onlylowercase'

        result = self.validator.password_is_valid(password)

        self.assertFalse(result)

    def test_reject_password_if_password_have_whitespace(self):

        password = 'Password with space'

        result = self.validator.password_is_valid(password)

        self.assertFalse(result)

    def test_accept_a_valid_password(self):

        password = 'ValidPassword'

        result = self.validator.password_is_valid(password)

        self.assertTrue(result)

