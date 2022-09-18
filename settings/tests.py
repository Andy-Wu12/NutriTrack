from django.test import TestCase

from access.models import CustomUser
from .forms import PasswordForm, EmailForm
from test_util import account_util


# Create your tests here.
class PrivacyViewTests(TestCase):
    def setUp(self):
        self.user1 = account_util.create_random_valid_user()
        self.user2 = account_util.create_random_valid_user()

    def test_default_privacy_is_public(self):
        """
        Default setting for logs should be public
        """
        pass

    def test_privacy_setting_set(self):
        """
        Users should be able to choose to make their logs public
        """
        pass

    def test_privacy_setting_unset(self):
        """
        Users should be able to choose to make their logs private
        """
        pass

    def test_private_log_detail_hidden_to_unauth_users(self):
        """
        Log details should not render at all for unauthorized users
        """
        pass

    def test_private_log_detail_not_hidden_to_owner(self):
        """
        Private Log details should NOT be hidden to it's own creator
        """
        pass

    def test_all_user_profile_private_logs_hidden(self):
        """
        The GET response should return no logs to unauthorized users
        """
        pass

    def test_all_profile_logs_unhidden(self):
        """
        All previously private logs should be available in profile GET response
        once user resets privacy setting
        """
        pass

    def test_all_private_logs_available_to_creator_on_profile(self):
        """
        All logs, regardless of privacy status, should be available to owner
        in profile page
        """
        pass


class PrivacyTemplateTests(TestCase):
    def setUp(self):
        self.user1 = account_util.create_random_valid_user()
        self.user2 = account_util.create_random_valid_user()

    def test_private_log_detail_hidden_to_unauth_users(self):
        """
        Log detail should provide a message to indicate unauthorized
        view status
        """
        pass

    def test_private_index_log_hidden(self):
        """
        Private logs should not render at all in logs index, even to owner
        """
        pass

    def test_private_log_detail_not_hidden_to_owner(self):
        """
        Private Log details should NOT be hidden to its own creator
        """
        pass

    def test_all_user_profile_private_logs_hidden(self):
        """
        Render message indicating unauthorized status for private logs
        """
        pass

    def test_all_profile_logs_unhidden(self):
        """
        All previously private logs should be rendered on profile
        if user resets privacy setting
        """
        pass

    def test_all_private_logs_available_to_creator(self):
        """
        All logs, regardless of privacy status, should be rendered on profile page for owner
        """
        pass

    def test_all_private_logs_available_to_creator_on_profile(self):
        """
        All logs, regardless of privacy status, should render on profile page
        if current user is owner
        """
        pass


class EmailChangeTests(TestCase):
    def setUp(self):
        self.user = account_util.create_random_valid_user()

    def test_existing_email_raises_form_error(self):
        """
        Cannot take the email of another user
        """
        pass

    def test_unused_email_valid_submission(self):
        """
        Valid email form submission requires unused email with valid format
        """
        pass

    def test_input_not_an_email(self):
        """
        Email input must be properly formatted
        """
        pass


class DeleteAccountTests(TestCase):
    def setUp(self):
        self.user = account_util.create_random_valid_user()

    def test_invalid_password_error_message(self):
        """
        If the password entered doesn't match the current user's render an error message
        """
        pass

    def test_valid_password_submission_deletes_account(self):
        """
        Entering the correct password should result in account deletion,
        and redirection to sign up page
        """
        pass


class ChangePasswordTests(TestCase):
    def setUp(self):
        self.uname = account_util.valid_uname
        self.pw = account_util.valid_pass
        self.email = account_util.valid_email
        self.user = account_util.create_user(self.uname, self.pw, email=self.email)

    def test_invalid_pass_confirmation_message(self):
        """
        Invalid password / confirmation should render an message indicating as such
        """
        pass

    def test_invalid_pass_length_message(self):
        """
        Password field should render a message indicating invalid password length
        if it is too short
        """
        pass

    def test_valid_password_change(self):
        """
        Password should change if both input fields match exactly
        """
        pass
