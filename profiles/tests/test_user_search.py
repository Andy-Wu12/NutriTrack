from django.test import TestCase
from django.urls import reverse

from test_util import account_util, search_query_util


class UserSearchTests(TestCase):
    def setUp(self):
        self.num_users = 4
        self.user = account_util.create_random_valid_user()
        self.usernames = [self.user.username]

        for i in range(self.num_users):
            user = account_util.create_random_valid_user()
            self.usernames.append(user.username)

    def test_user_search_query_empty(self):
        """
        Empty query should return the default of all logs
        """
        response = self.client.post(reverse('profiles:index'), search_query_util.create_search_form(''))
        self.assertContains(response, '<li>', count=self.num_users + 1)
        self.assertTemplateUsed(response, 'profiles/index.html')

    def test_user_search_query_no_results(self):
        """
        Non-empty query with no results should return message indicating as such
        """
        no_result_query = search_query_util.get_invalid_query_input(self.usernames)
        for c in no_result_query:
            response = self.client.post(reverse('profiles:index'),
                                        search_query_util.create_search_form(c))
            self.assertNotContains(response, '<li>')
            self.assertContains(response, 'No users')

    def test_returning_all_users_with_username_containing_query(self):
        """
        If a query is valid and has results, the usernames should contain the query
        as a substring
        """
        for username in self.usernames:
            response = self.client.post(reverse('profiles:index'),
                                        search_query_util.create_search_form(username))
            self.assertContains(response, '<li>')
            for c in username:
                response = self.client.post(reverse('profiles:index'),
                                            search_query_util.create_search_form(c))
                self.assertContains(response, '<li>')
