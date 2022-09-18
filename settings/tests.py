from django.test import TestCase

from access.models import CustomUser
from .forms import PasswordForm, EmailForm
from test_util import account_util, util


# Create your tests here.
class SettingsViewTests(TestCase):
    def setUp(self):
        self.user = account_util.create_random_valid_user()
