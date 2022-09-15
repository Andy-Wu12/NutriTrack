from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from test_util import log_util


# Create your tests here.
class ProfileLogsTest(TestCase):
    def setUp(self):
        self.user = log_util.create_random_valid_user()

    def test_no_logs_message(self):
        """
        User profile should render a message indicating that a user has no logs
        """
        request = self.client.get(reverse('profiles:user', args=(self.user.id, )))
        self.assertContains(request, 'no logs')

    def test_single_log_renders(self):
        """
        User profile should be able to render a single log
        """
        food = log_util.create_random_food()
        log = log_util.create_log(creator=self.user, food=food,
                                  pub_date=timezone.now(), save=True)
        request = self.client.get(reverse('profiles:user', args=(self.user.id, )))
        self.assertContains(request, log.food.name)

    def test_log_count(self):
        """
        Number of logs rendered should be equal to the number of logs a user has
        """
        food_count = 100
        food = log_util.create_random_food()
        foods = [log_util.create_food(food.creator, food.name,
                                      food.desc, save=True)
                 for _ in range(food_count)]

        logs = []
        for food in foods:
            log = log_util.create_log(self.user, food,
                                      timezone.now(), save=True)
            logs.append(log)

        request = self.client.get(reverse('profiles:user', args=(self.user.id, )))
        self.assertContains(request, food.name, count=food_count)

    def test_multiple_logs_render_correctly(self):
        """
        User profile should be able to render all logs
        """
        food_count = 100
        foods = [log_util.create_random_food() for _ in range(food_count)]

        logs = []
        for food in foods:
            log = log_util.create_log(self.user, food,
                                      timezone.now(), save=True)
            logs.append(log)

        request = self.client.get(reverse('profiles:user', args=(self.user.id, )))

        for log in logs:
            self.assertContains(request, log.food.name)
