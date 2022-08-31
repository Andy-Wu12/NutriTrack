import random
from datetime import timedelta, datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .models import Food, Log, Comment
from access.tests.test_login import create_login_form


# Helper functions
def create_user(username: str, password: str = '', fname: str = '', lname: str = '',
                email: str = '', save=False):
    """
    Create a user with the given `username`, and optional `password`,
    first name `fname`, last name `lname`, and `email`.
    These parameters are optional for testing purposes.
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
                   day_offset: int, past=True):
    """
    Create a comment with an optional associated user, associated log,
    `comment_text` and published the given number of `date_offset` to now
    (negative for comments published in the past,
    positive for comments that have yet to be published).
    """
    time = timezone.now()
    if past:
        time = time - timedelta(days=day_offset)
    else:
        time = time + timedelta(days=day_offset)
    return Comment.objects.create(creator=creator, log=assoc_log,
                                  comment=comment_text, pub_date=time)


def create_default_log():
    food = create_food('test food', 'test desc', save=True)
    user = create_user('awu', save=True)
    log = create_log(user, food, timezone.now(), save=True)
    return log


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
        log = create_default_log()

        response = self.client.get(reverse('logs:index'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "No logs are available.")
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
        self.assertNotContains(response, "No logs are available.")
        self.assertQuerysetEqual(response.context['latest_logs'], logs, ordered=False)


class LogDetailViewTests(TestCase):
    def test_log_no_comment(self):
        """
        If no comments exist for a specific (and existing) log,
        an appropriate message is displayed.
        """
        log = create_default_log()

        response = self.client.get(reverse('logs:detail', args=(log.id, )))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Be the first to comment.")
        self.assertEqual(response.context['log'], log)
        self.assertQuerysetEqual(response.context['comment_list'], [])

    def test_past_comment(self):
        """
        Comments from the past SHOULD be rendered
        """
        log = create_default_log()
        day_offset = random.randint(1, 365)
        # Comment creator can be anyone, set as log creator for test simplicity
        comment = create_comment(log.creator, log, 'past comment',
                                 day_offset, past=True)

        response = self.client.get(reverse('logs:detail', args=(log.id, )))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Be the first to comment.")
        self.assertEqual(response.context['log'], log)
        self.assertQuerysetEqual(response.context['comment_list'], [comment])

    def test_future_comment(self):
        """
        A comment from the future should not be rendered ... yet
        """
        log = create_default_log()
        day_offset = random.randint(1, 365)
        create_comment(log.creator, log, 'past comment',
                       day_offset, past=False)

        response = self.client.get(reverse('logs:detail', args=(log.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Be the first to comment.")
        self.assertEqual(response.context['log'], log)
        self.assertQuerysetEqual(response.context['comment_list'], [])

    def test_past_and_future_comments(self):
        """
        If database contains past/present AND future comments,
        it should only render those not from the future.
        """
        log = create_default_log()
        day_offset = random.randint(1, 365)
        past_comment = create_comment(log.creator, log, 'this is the past',
                                      day_offset, past=True)
        create_comment(log.creator, log, 'this is the future',
                       day_offset, past=False)

        response = self.client.get(reverse('logs:detail', args=(log.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Be the first to comment.")
        self.assertEqual(response.context['log'], log)
        self.assertQuerysetEqual(response.context['comment_list'], [past_comment])

    def test_multiple_comments(self):
        """
        All past and present comments should be rendered
        """
        comments = []
        num_comments = 50
        log = create_default_log()
        day_offset = random.randint(1, 365)
        for i in range(num_comments):
            comments.append(create_comment(log.creator, log, 'this is the past',
                            day_offset, past=True))

        response = self.client.get(reverse('logs:detail', args=(log.id,)))
        self.assertNotContains(response, "Be the first to comment.")
        self.assertEqual(response.context['log'], log)
        self.assertQuerysetEqual(response.context['comment_list'], comments, ordered=False)


class LogSessionTests(TestCase):
    # Valid user account fields
    valid_uname = "appTester01"
    valid_pass = "s3cureP@ssword054!"
    valid_email = "apptester@foodlog.com"

    # Authentication status messages
    auth_index_mess = f'Hi {valid_uname}! Here are the most recent logs'
    unauth_index_mess = 'Create your own food log'
    unauth_comment_mess = 'to leave a comment'

    def setUp(self):
        create_user(username=self.valid_uname, password=self.valid_pass,
                    email=self.valid_email, save=True)

    def test_index_authenticated(self):
        """
        Authenticated user should get a personal 'welcome message'
        in the heading and should be allowed to create logs
        """
        form = create_login_form(email=self.valid_email, password=self.valid_pass)
        self.client.post(reverse('access:login'), form.data)

        response = self.client.get(reverse('logs:index'))
        self.assertContains(response, self.auth_index_mess)

    def test_index_unauthenticated(self):
        """
        Unauthenticated user should be referred to the signup page
        in the heading, but still allowed to view logs
        """
        response = self.client.get(reverse('logs:index'))
        self.assertContains(response, self.unauth_index_mess)

        redirect_path = reverse('access:signup')
        signup_button_html = f'<a href=\"{redirect_path}\">Sign Up</a>'
        self.assertContains(response, signup_button_html, html=True)

    def test_comment_authenticated_message(self):
        """
        Authenticated user should be able to comment
        along with seeing log details and other comments
        """
        log = create_default_log()
        form = create_login_form(email=self.valid_email, password=self.valid_pass)
        self.client.post(reverse('access:login'), form.data)

        response = self.client.get(reverse('logs:detail', args=(log.id, )))
        comment_post_path = reverse('logs:add-comment', args=(log.id, ))
        self.assertContains(response,
                            f'<form id="comment-form" action="{comment_post_path}" method="post">'
                            )

    def test_comment_unauthenticated_message(self):
        """
        Unauthenticated user should be asked to signup
        before commenting but still able to see
        log details and other comments
        """
        log = create_default_log()
        response = self.client.get(reverse('logs:detail', args=(log.id, )))
        self.assertContains(response, self.unauth_comment_mess)

        redirect_path = reverse('access:signup')
        signup_button_html = f'<a href=\"{redirect_path}\">Sign up</a>'
        self.assertContains(response, signup_button_html, html=True)
