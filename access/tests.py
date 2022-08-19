import random

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

import access.forms as access_form

# Helper functions and vars
def create_signup_form(email=None, username=None, password=None):
    form_data = {'email': email, 'username': username, 'password': password}
    form = access_form.SignupForm(data=form_data)
    form.is_valid()
    return form

valid_uname = 'tester123'
valid_email = 'tester@foodlog.com'
valid_pass = 'secur3passWord!'

# Not minimum length
invalid_uname = 'a'
# Not valid email format (auto-validated by Django EmailField)
invalid_email = 'av2@'
# Not minimum length
invalid_pass = '1234'


class UserCreationFormTests(TestCase):
    def test_form_missing_username(self):
        """
        If no username provided on the signup form, the form is invalid
        """
        form = create_signup_form(email=valid_email, password=valid_pass)
        self.assertFalse(form.is_valid())

    def test_form_missing_email(self):
        """
        If no email provided on the signup form, the form is invalid
        """
        form = create_signup_form(username=valid_uname, password=valid_pass)
        self.assertFalse(form.is_valid())

    def test_form_missing_password(self):
        """
        If no password provided on the signup form, the form is invalid
        """
        form = create_signup_form(username=valid_uname, email=valid_email)
        self.assertFalse(form.is_valid())

    def test_not_minimum_password_length(self):
        """
        If len(password) < minimum length, the form is invalid
        """
        form = create_signup_form(username=valid_uname, email=valid_email, password=invalid_pass)
        self.assertFalse(form.is_valid())

    def test_not_minimum_username_length(self):
        """
        If len(username) < minimum length, form invalid
        """
        form = create_signup_form(username=invalid_uname, email=valid_email, password=valid_pass)
        self.assertFalse(form.is_valid())

    def test_valid_form_submission(self):
        """
        If all fields are provided and meet requirements form is valid
        """
        form = create_signup_form(username=valid_uname, email=valid_email, password=valid_pass)
        self.assertTrue(form.is_valid())


class UserCreationViewTests(TestCase):
    def test_form_missing_username(self):
        """
        If no username is provided on the signup form,
        redirect (302) should send user back to form page,
        and User object should not be saved into db
        """
        form = create_signup_form(email=valid_email, password=valid_pass)
        response = self.client.post(reverse('access:signup'), form.cleaned_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('access:signup'))
        self.assertFalse(User.objects.filter(email=valid_email).exists())

    def test_form_missing_email(self):
        """
        If no email is provided on the signup form,
        redirect (302) should send user back to form page,
        and User object should not be saved into db
        """
        form = create_signup_form(username=valid_uname, password=valid_pass)
        response = self.client.post(reverse('access:signup'), form.cleaned_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('access:signup'))
        self.assertFalse(User.objects.filter(username=valid_uname).exists())

    def test_form_missing_password(self):
            """
            If no password is provided on the signup form,
            redirect (302) should send user back to form page,
            and User object should not be saved into db
            """
            form = create_signup_form(email=valid_email, username=valid_uname)
            response = self.client.post(reverse('access:signup'), form.cleaned_data)

            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, reverse('access:signup'))
            self.assertFalse(User.objects.filter(email=valid_email).exists())

    def test_not_minimum_password_length(self):
        """
        If len(password) < minimum length, form invalid
        """
        form = create_signup_form(username=valid_uname, email=valid_email, password=invalid_pass)
        response = self.client.post(reverse('access:signup'), form.cleaned_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('access:signup'))
        self.assertFalse(User.objects.filter(email=valid_email).exists())

    def test_not_minimum_username_length(self):
        """
        If len(username) < min length, form invalid
        """
        form = create_signup_form(username=invalid_uname, email=valid_email, password=valid_pass)
        response = self.client.post(reverse('access:signup'), form.cleaned_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('access:signup'))
        self.assertFalse(User.objects.filter(email=valid_email).exists())

    def test_exisiting_username(self):
        pass

    def test_existing_email(self):
        pass

    def test_valid_form_submission(self):
        """
        If all fields are provided and meet requirements (minimum length)
        redirect should be made to logs:index
        and new user object should be stored
        """
        form = create_signup_form(username=valid_uname, email=valid_email, password=valid_pass)
        response = self.client.post(reverse('access:signup'), form.cleaned_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('logs:index'))
        self.assertTrue(User.objects.filter(email=valid_email).exists())
