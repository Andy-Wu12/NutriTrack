import random
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

import access.forms as access_form

# Helper functions and vars
def create_signup_form(email=None, username=None, password=None):
    form_data = {'email': email, 'username': username, 'password': password}
    return access_form.SignupForm(data=form_data)

valid_uname = 'tester123'
valid_email = 'abc@123.com'
valid_pass = '12345678'

# Not minimum length
invalid_uname = 'a'
# Not valid email format (auto-validated by Django EmailField)
invalid_email = 'av2@'
# Not minimum length
invalid_pass = '1234'


class UserCreationFormTests(TestCase):
    def test_form_missing_username(self):
        """
        If no username is provided on the signup form,
        the form is invalid
        """
        form = create_signup_form(email=valid_email, password=valid_pass)
        self.assertFalse(form.is_valid())

    def test_form_missing_email(self):
        """
        If no email is provided on the signup form,
        the form is invalid
        """
        form = create_signup_form(username=valid_uname, password=valid_pass)
        self.assertFalse(form.is_valid())

    def test_form_missing_password(self):
        """
        If no password is provided on the signup form,
        the form is invalid
        """
        form = create_signup_form(username=valid_uname, email=valid_email)
        self.assertFalse(form.is_valid())

    def test_not_minimum_password_length(self):
        """
        If provided password is not longer than minimum length,
        the form is invalid
        """
        form = create_signup_form(username=valid_uname, email=valid_email, password='1234')
        self.assertFalse(form.is_valid())

    def test_not_minimum_username_length(self):
        """
        If provided username is not longer than minimum length,
        the form is invalid
        """
        form = create_signup_form(username='a', email=valid_email, password=valid_pass)
        self.assertFalse(form.is_valid())

    def test_valid_form_submission(self):
        """
        If all fields are provided and meet requirements
        (minimum length), form is valid
        """
        form = create_signup_form(username=valid_uname, email=valid_email, password=valid_pass)
        self.assertTrue(form.is_valid())
