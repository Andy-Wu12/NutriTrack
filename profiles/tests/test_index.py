from django.test import TestCase
from django.urls import reverse

from test_util import account_util, search_query_util


class UserIndexTests(TestCase):
    def setUp(self):
        self.num_users = 4
        self.user = account_util.create_random_valid_user()
        self.usernames = [self.user.username]

        for i in range(self.num_users):
            user = account_util.create_random_valid_user()
            self.usernames.append(user.username)

    def test_unathenticated_user_can_view_index(self):
        """
        Users index should not require authentication to view
        """
        response = self.client.get(reverse('profiles:index'))
        self.assertContains(response, '<li>', count=self.num_users + 1)
        self.assertTemplateUsed(response, 'profiles/index.html')

    def test_authenticated_user_can_view_index(self):
        """
        Authenticated users should be able to view user index
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('profiles:index'))
        self.assertContains(response, '<li>', count=self.num_users)
        self.assertTemplateUsed(response, 'profiles/index.html')

    def test_authenticated_username_doesnt_render(self):
        """
        Authenticated user's username should not show in the index
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('profiles:index'))
        self.assertContains(response, '<li>', count=self.num_users)
        self.assertNotContains(response, self.user.username)
        self.assertTemplateUsed(response, 'profiles/index.html')
