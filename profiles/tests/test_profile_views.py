import random
import sys

from django.test import TestCase
from django.urls import reverse

from access.models import CustomUser
from test_log_util import log_util


# Create your tests here.
class ProfileViewTests(TestCase):
    def setUp(self):
        self.num_users = 50
        self.users = [log_util.create_random_valid_user() for _ in range(self.num_users)]

    def test_invalid_profile_id(self):
        """
        Invalid user id route should return a 404 response and an error message
        """
        max_valid_id = len(self.users)
        num_loops = 100

        for i in range(num_loops):
            invalid_id = random.randint(max_valid_id, sys.maxsize)
            response = self.client.get(reverse('profiles:user', args=[invalid_id]))

            self.assertEqual(response.status_code, 404)
            self.assertContains(response, 'User does not exist')

    def test_valid_profile_ids(self):
        """
        Valid user id routes should successfully render with username somewhere on
        the page
        """
        for i in range(1, self.num_users + 1):
            user = CustomUser.objects.get(pk=i)
            response = self.client.get(reverse('profiles:user', args=[i]))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, f'{user.username}')
