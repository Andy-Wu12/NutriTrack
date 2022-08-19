from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

import access.forms as access_form


# Helper functions and vars
def create_login_form(email='', password=''):
    form_data = {'email': email, 'password': password}
    form = access_form.LoginForm(data=form_data)
    form.is_valid()
    return form

def create_valid_user():
    username = 'new_test_user321'
    email = 'tester@testing.com'
    password = 'testPass123^@!'
    User.objects.create_user(username, email, password)

valid_uname = 'tester123'
valid_email = 'tester@foodlog.com'
valid_pass = 'secur3passWord!'

# Not minimum length
invalid_uname = 'a'
# Not valid email format (auto-validated by Django EmailField)
invalid_email = 'av2@'
# Not minimum length
invalid_pass = '1234'


class LoginFormTests(TestCase):
    def test_form_missing_email(self):
        """
        If no email provided, the form is invalid
        """
        pass

    def test_form_missing_password(self):
        """
        If no password provided, the form is invalid
        """
        pass

    def test_form_missing_email_and_password(self):
        """
        If neither password nor email provided, the form is invalid
        """
        pass

    def test_valid_form_submission(self):
        """
        If both password and email provided, the form is valid
        """
        pass

    def test_valid_form_username_doesnt_exist(self):
        """
        If form is valid but username doesn't exist, the form
        """
        pass

class LoginFormViewsTests(TestCase):
    def test_form_missing_email(self):
        """
        If no email provided, send the user back to the form
        along with error code 400
        """
        pass

    def test_form_missing_password(self):
        """
        If no password provided, send the user back to the form
        with status code 400
        """
        pass

    def test_valid_form_invalid_username_redirect(self):
        """
        If no User exists with provided username,
        send the user back to the form with status code 400
        """
        pass

    def test_invalid_username_error_message(self):
        """
        If no User exists with provided username,
        the login template should render a non-specific
        error message (don't tell user whether it's
        an incorrect password / username)
        """
        pass

    def test_invalid_password_error_message(self):
        """
        If no User exists with provided password,
        the login template should render a non-specific
        error message (don't tell user whether it's
        an incorrect password / username)
        """
        pass

    def test_valid_credentails(self):
        """
        If credentials are valid, redirect to logs index
        with status_code 200
        """
        pass