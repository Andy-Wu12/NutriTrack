from django.test import TestCase
from django.urls import reverse

from access.models import CustomUser
from .forms import PasswordForm, EmailForm
from .models import Privacy
from test_util import account_util


def create_log_setting_form(value: bool):
    return {'log-setting': value}


# Create your tests here.
class PrivacyViewTests(TestCase):
    def setUp(self):
        self.user1 = account_util.create_random_valid_user()
        self.user2 = account_util.create_random_valid_user()
        self.client.force_login(self.user1)
        # self.client.force_login(self.user2)

    def test_default_privacy_is_off(self):
        """
        Default setting for logs should be public
        """
        user1_privacy = Privacy.objects.get(user=self.user1)
        user2_privacy = Privacy.objects.get(user=self.user2)
        self.assertTrue(user1_privacy)
        self.assertTrue(user2_privacy)

    def test_privacy_on(self):
        """
        Users should be able to choose to make their logs private
        """
        form = create_log_setting_form(False)
        self.client.post(reverse('settings:privacy'), form)
        privacy_setting = Privacy.objects.get(user=self.user1)
        self.assertFalse(privacy_setting.show_logs)

    def test_privacy_on_then_off(self):
        """
        Users should be able to choose to make their logs public
        """
        on_form = create_log_setting_form(False)
        off_form = create_log_setting_form(True)
        self.client.post(reverse('settings:privacy'), on_form)
        self.client.post(reverse('settings:privacy'), off_form)
        privacy_setting = Privacy.objects.get(user=self.user1)
        self.assertTrue(privacy_setting.show_logs)


class PrivacyTemplateTests(TestCase):
    def setUp(self):
        self.user1 = account_util.create_random_valid_user()
        self.user2 = account_util.create_random_valid_user()

    def test_private_log_detail_hidden_to_unauth_users(self):
        """
        Log detail should provide a message to indicate unauthorized
        view status
        """

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
        The GET response should return no logs to unauthorized users
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
