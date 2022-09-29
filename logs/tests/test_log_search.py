import string

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from test_util import log_util, account_util, search_query_util


class LogSearchTests(TestCase):
    def setUp(self):
        self.num_logs = 10

        self.user = account_util.create_random_valid_user()
        self.food_name = log_util.generateRandStr(15)
        self.food_desc = 'test_desc'
        self.ingredients = 'test_ingredients'
        self.calories = 200
        for i in range(self.num_logs):
            food = log_util.create_food(creator=self.user, name=self.food_name,
                                        desc=self.food_desc, ingredients=self.ingredients,
                                        calories=self.calories, save=True)
            log_util.create_log(creator=self.user, food=food, pub_date=timezone.now(), save=True)

    def test_log_search_query_empty(self):
        """
        Empty query should return the default of all logs
        """
        response = self.client.post(reverse('logs:index'), search_query_util.create_search_form(''))
        self.assertContains(response, '<li>', count=self.num_logs)
        self.assertTemplateUsed(response, 'logs/index.html')

    def test_log_search_query_no_results(self):
        """
        Non-empty query with no results should return message indicating as such
        """
        no_result_query = search_query_util.get_invalid_query_input([self.food_name, self.user.username])
        for c in no_result_query:
            response = self.client.post(reverse('logs:index'),
                                        search_query_util.create_search_form(c))
            self.assertNotContains(response, '<li>')
            self.assertContains(response, 'No logs')

    def test_returning_all_logs_with_username_containing_query(self):
        """
        If a query is valid and has results, the resulting logs' creator's
        username should contain the query as a substring (case-insensitive)
        """
        for c in self.user.username:
            response = self.client.post(reverse('logs:index'),
                                        search_query_util.create_search_form(c))
            self.assertContains(response, '<li>', count=self.num_logs)

    def test_returning_all_logs_with_food_name_containing_query(self):
        """
        If a query is valid and has results, the resulting logs' associated
        food name should contain the query as a substring (case-insensitive)
        """
        for c in self.food_name:
            response = self.client.post(reverse('logs:index'),
                                        search_query_util.create_search_form(c))
            self.assertContains(response, '<li>', count=self.num_logs)

    def test_returning_all_logs_with_food_or_username_containing_query(self):
        """
        If a query is valid and has results, the resulting logs' associated
        food name OR creator's username should contain the query
        as a substring (case-insensitive)
        """
        valid_ascii_set = set(self.food_name) | set(self.user.username)
        for c in valid_ascii_set:
            response = self.client.post(reverse('logs:index'),
                                        search_query_util.create_search_form(c))
            self.assertContains(response, '<li>', count=self.num_logs)

