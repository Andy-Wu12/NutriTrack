from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

import access.forms as access_form


valid_uname = 'tester123'
valid_email = 'tester@foodlog.com'
valid_pass = 'secur3passWord!'

# Not minimum length
invalid_uname = 'a'
# Not valid email format (auto-validated by Django EmailField)
invalid_email = 'av2@'
# Not minimum length
invalid_pass = '1234'

field_required_mess = 'This field is required'
invalid_cred_mess = 'Incorrect email/password combination'


# Helper functions and vars
def create_login_form(email='', password=''):
    form_data = {'email': email, 'password': password}
    form = access_form.LoginForm(data=form_data)
    return form


def create_default_valid_user():
    username = valid_uname
    email = valid_email
    password = valid_pass
    User.objects.create_user(username, email, password)


class LoginFormTests(TestCase):
    def test_form_missing_email(self):
        """
        If no email provided, the form is invalid
        """
        form = create_login_form(password=valid_pass)
        self.assertFalse(form.is_valid())

    def test_form_missing_password(self):
        """
        If no password provided, the form is invalid
        """
        form = create_login_form(email=valid_email)
        self.assertFalse(form.is_valid())

    def test_form_missing_email_and_password(self):
        """
        If neither password nor email provided, the form is invalid
        """
        form = create_login_form(email='', password='')
        self.assertFalse(form.is_valid())

    def test_valid_form_submission(self):
        """
        If both password and email provided, the form is valid.
        View tests responsible for handling cases where email doesn't
        exist for any user and other errors
        """
        create_default_valid_user()
        form = create_login_form(email=valid_email, password=valid_pass)
        self.assertTrue(form.is_valid())


class LoginFormViewsTests(TestCase):
    def setUp(self):
        # Create and store a valid user in database before each test
        create_default_valid_user()

    def test_form_missing_email(self):
        """
        If no email provided, send the user back to the form
        along with error code 400
        """
        form = create_login_form(password=valid_pass)
        response = self.client.post(reverse('access:login'), form.data)

        self.assertTemplateUsed('access/login.html')
        self.assertContains(response, field_required_mess, count=1, status_code=400)

    def test_form_missing_password(self):
        """
        If no password provided, send the user back to the form
        with status code 400
        """
        form = create_login_form(email=valid_email)
        response = self.client.post(reverse('access:login'), form.data)

        self.assertTemplateUsed('access/login.html')
        self.assertContains(response, field_required_mess, count=1, status_code=400)

    def test_form_empty(self):
        """
        If neither email nor password provided,
        send the user back to the form with status code 400
        """
        form = create_login_form()
        response = self.client.post(reverse('access:login'), form.data)

        self.assertTemplateUsed('access/login.html')
        self.assertContains(response, field_required_mess, count=2, status_code=400)

    def test_valid_form_invalid_email(self):
        """
        If no User exists with provided email,
        send the user back to the form with status code 400
        """
        form = create_login_form(email='testemail@testing.com', password=valid_pass)
        response = self.client.post(reverse('access:login'), form.data)

        self.assertTemplateUsed('access/login.html')
        self.assertContains(response, invalid_cred_mess, status_code=400)

    def test_invalid_email_error_message(self):
        """
        If no User exists with provided email,
        the login template should render a non-specific
        error message (don't tell user whether it's
        an incorrect password / username)
        """
        form = create_login_form(email='testemail@testing.com', password=valid_pass)
        response = self.client.post(reverse('access:login'), form.data)

        self.assertContains(response, invalid_cred_mess, status_code=400)

    def test_invalid_password_error_message(self):
        """
        If User with email exists but password invalid,
         render error message (don't tell user whether it's
        an incorrect password / username)
        """
        form = create_login_form(email=valid_email, password=invalid_pass)
        response = self.client.post(reverse('access:login'), form.data)

        self.assertContains(response, invalid_cred_mess, status_code=400)

    def test_valid_credentails(self):
        """
        If credentials are valid, redirect to logs index
        with status_code 200
        """
        form = create_login_form(email=valid_email, password=valid_pass)
        response = self.client.post(reverse('access:login'), form.data)

        self.assertRedirects(response, reverse('logs:index'))


class LoginSessionTests(TestCase):
    def setUp(self):
        create_default_valid_user()

    def test_not_logged_in(self):
        """
        If user is not authenticated and goes to login page,
        no redirect / re-render should occur.
        """
        response = self.client.get(reverse('access:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'access/login.html')

    def test_already_logged_in_redirect(self):
        """
        If user is authenticated and goes back to login page,
        they should automatically be redirected to logs index.
        """
        form = create_login_form(email=valid_email, password=valid_pass)
        self.client.post(reverse('access:login'), form.data)

        response = self.client.get(reverse('access:login'))

        self.assertRedirects(response, reverse('logs:index'))

    def test_login_then_signup(self):
        """
        If logs in then goes to signup page,
        they should automatically be redirected to logs index.
        """
        form = create_login_form(email=valid_email, password=valid_pass)
        self.client.post(reverse('access:login'), form.data)

        response = self.client.get(reverse('access:signup'))

        self.assertRedirects(response, reverse('logs:index'))
