class Validator:

    def password_is_valid(self, password):

        if len(password) <= 8:
            return False

        if password.islower() or password.isupper():
            return False

        if ' ' in password:
            return False

        return True
