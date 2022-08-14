import random
from datetime import timedelta, datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .models import Food, Log, Comment


# Helper functions
def create_user(username: str, password: str = '', fname: str = '', lname: str = '',
                email: str = '', save=False):
    """
    Create a user with the given `username`, and optional `password`,
    first name `fname`, last name `lname`, and `email`.
    """
    user = User(username=username, email=email, password=make_password(password),
                first_name=fname, last_name=lname)

    if save:
        user.save()
    return user


def create_food(name: str, desc: str, ingredients: str = None, calories: int = None, save=False):
    """
    Create a food with the given `name` and `desc`, along with
    optional `ingredients`, and number of calories.
    """
    food = Food(name=name, desc=desc, ingredients=ingredients,
                calories=calories)

    if save:
        food.save()
    return food


def create_log(creator: User, food: Food, pub_date: datetime, save=False):
    """
    Create a food log on the given date,
    associated to `creator` and a `food`.
    """
    log = Log(creator=creator, food=food, pub_date=pub_date)

    if save:
        log.save()
    return log


def create_comment(creator: User, assoc_log: Log, comment_text: str,
                   day_offset: int, save=False):
    """
    Create a comment with an optional associated user, associated log,
    `comment_text` and published the given number of `date_offset` to now
    (negative for comments published in the past,
    positive for comments that have yet to be published).
    """
    time = timezone.now() + timedelta(days=day_offset)
    return Comment.objects.create(user=creator, assoc_log=assoc_log,
                                  comment=comment_text, pub_date=time)


# Create your tests here.
class CommentModelTests(TestCase):
    def test_comment_is_recent_from_future(self):
        """
        is_recent is False if pub_date is from the future
        """
        time = timezone.now() + timedelta(days=random.randint(2, 100))
        future_comment = Comment(pub_date=time)

        self.assertIs(future_comment.is_recent(), False)

    def test_comment_is_recent_from_far_past(self):
        """
        is_recent is False if pub_date is more than a day in the past (> 24h)
        """
        time = timezone.now() - timedelta(days=random.randint(2, 100))
        far_past_comment = Comment(pub_date=time)

        self.assertIs(far_past_comment.is_recent(), False)

    def test_comment_is_recent_from_recent_timespan(self):
        """
        is_recent is True if pub_date is within 24h range in the past
        """
        rand_hour_diff = random.randint(0, 23)
        rand_minute_diff = random.randint(0, 59)
        rand_second_diff = random.randint(0, 59)
        time = timezone.now() - timedelta(hours=rand_hour_diff,
                                          minutes=rand_minute_diff,
                                          seconds=rand_second_diff)

        recent_comment = Comment(pub_date=time)

        self.assertIs(recent_comment.is_recent(), True)


class LogIndexViewTests(TestCase):
    def test_no_logs(self):
        """
        If no logs exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('logs:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No logs are available.")
        self.assertQuerysetEqual(response.context['latest_logs'], [])

    def test_single_log(self):
        """
        Created log should exist in log index
        """
        food = create_food('test food', 'test desc', save=True)
        user = create_user('awu', save=True)
        log = create_log(user, food, timezone.now(), save=True)

        response = self.client.get(reverse('logs:index'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "No logs are available")
        self.assertQuerysetEqual(response.context['latest_logs'], [log])

    def test_multiple_logs(self):
        """
        All created logs should exist in log index
        """
        logs = []
        num_iterations = random.randint(2, 10)
        for i in range(num_iterations):
            food = create_food(f'test food{i}', f'test desc{i}', save=True)
            user = create_user(f'awu{i}', save=True)
            log = create_log(user, food, timezone.now(), save=True)
            logs.append(log)

        response = self.client.get(reverse('logs:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(logs), num_iterations)
        self.assertNotContains(response, "No logs are available")
        self.assertQuerysetEqual(response.context['latest_logs'], logs, ordered=False)
