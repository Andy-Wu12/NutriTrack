import random
from datetime import timedelta, datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .models import Food, Log, Comment
from access.tests.test_login import create_login_form
from .forms import FoodForm

# Valid user account fields
valid_uname = "appTester01"
valid_pass = "s3cureP@ssword054!"
valid_email = "apptester@foodlog.com"


# Helper functions
def create_default_valid_user():
    username = valid_uname
    email = valid_email
    password = valid_pass
    User.objects.create_user(username, email, password)


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


def create_default_food():
    food = create_food('test food', 'test desc', save=True)
    return food


def create_default_log():
    food = create_default_food()
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
    # Authentication status messages
    auth_index_mess = f'Hi {valid_uname}! Here are the most recent logs'
    unauth_index_mess = 'Create your own food log'
    unauth_comment_mess = 'to leave a comment'

    def setUp(self):
        create_user(username=valid_uname, password=valid_pass,
                    email=valid_email, save=True)

    def test_index_authenticated(self):
        """
        Authenticated user should get a personal 'welcome message'
        in the heading and should be allowed to create logs
        """
        form = create_login_form(email=valid_email, password=valid_pass)
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
        form = create_login_form(email=valid_email, password=valid_pass)
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


class CreateLogTests(TestCase):
    food_name = 'test food'
    desc = 'test desc'
    ingredients = 'test ingredients'
    calories = 100

    def create_valid_default_log(self, logged_in=True):
        if logged_in:
            login_form = create_login_form(email=valid_email, password=valid_pass)
            self.client.post(reverse('access:login'), login_form.data)

        form_data = {'name': self.food_name, 'desc': self.desc,
                     'ingredients': self.ingredients, 'calories': self.calories}
        self.client.post(reverse('logs:create-log'), form_data)

    def setUp(self):
        create_default_valid_user()

    def test_log_has_correct_creator(self):
        """
        Ensure created log has the correct associated user
        """
        self.create_valid_default_log(logged_in=True)
        log = Log.objects.get(pk=1)
        self.assertEqual(str(log.creator), valid_uname)

    def test_log_has_correct_description(self):
        """
        Ensure created log has the correct description
        """
        self.create_valid_default_log(logged_in=True)
        log = Log.objects.get(pk=1)
        self.assertEqual(str(log.food.desc), self.desc)

    def test_log_has_correct_ingredients(self):
        """
        Ensure created log has the correct ingredients
        """
        self.create_valid_default_log(logged_in=True)
        log = Log.objects.get(pk=1)
        self.assertEqual(str(log.food.ingredients), self.ingredients)

    def test_log_has_correct_calories(self):
        """
        Ensure created log has the correct # calories
        """
        self.create_valid_default_log(logged_in=True)
        log = Log.objects.get(pk=1)
        self.assertEqual(log.food.calories, self.calories)


class CreateLogViewTests(TestCase):
    food_name = 'test food'
    desc = 'test desc'
    ingredients = 'test ingredients'
    calories = 100

    def login_default_user(self):
        login_form = create_login_form(email=valid_email, password=valid_pass)
        self.client.post(reverse('access:login'), login_form.data)

    def populate_log_create_form(self, name=True, desc=True, ingredients=True,
                                 calories=True):
        form_data = {}
        if name:
            form_data['name'] = self.food_name
        if desc:
            form_data['desc'] = self.desc
        if ingredients:
            form_data['ingredients'] = self.ingredients
        if calories:
            form_data['calories'] = self.calories
        return form_data

    def setUp(self):
        create_default_valid_user()

    def test_form_missing_name(self):
        """
        Name field should be required for log creation
        """
        self.login_default_user()
        form_data = self.populate_log_create_form(name=False)

        response = self.client.post(reverse('logs:create-log'), form_data)
        self.assertEqual(response.status_code, 400)

    def test_form_missing_description(self):
        """
        Description should be required for log creation
        """
        self.login_default_user()
        form_data = self.populate_log_create_form(desc=False)

        response = self.client.post(reverse('logs:create-log'), form_data)
        self.assertEqual(response.status_code, 400)

    def test_form_missing_ingredients(self):
        """
        Ingredients required for log creation
        """
        self.login_default_user()
        form_data = self.populate_log_create_form(ingredients=False)

        response = self.client.post(reverse('logs:create-log'), form_data)
        self.assertEqual(response.status_code, 400)

    def test_form_missing_calories(self):
        """
        # Calories required for log creation
        """
        self.login_default_user()
        form_data = self.populate_log_create_form(calories=False)

        response = self.client.post(reverse('logs:create-log'), form_data)
        self.assertEqual(response.status_code, 400)

    def test_form_redirect_unauthenticated_user(self):
        """
        Page should automatically redirect unauthenticated user
        to signup page
        """
        response = self.client.get(reverse('logs:create-log'))
        self.assertRedirects(response, reverse('access:signup'))

    def test_valid_log_creation_redirect(self):
        """
        Valid log creation should redirect user to logs index
        """
        self.login_default_user()
        form_data = self.populate_log_create_form()

        response = self.client.post(reverse('logs:create-log'), form_data)
        self.assertRedirects(response, reverse('logs:index'))

    def test_valid_log_creation_exists_in_db(self):
        """
        Valid log creation should be correctly stored in db
        """
        self.login_default_user()
        form_data = self.populate_log_create_form()

        response = self.client.post(reverse('logs:create-log'), form_data)
        log = Log.objects.get(pk=1)
        user = User.objects.get(pk=1)
        self.assertTrue(log)

        self.assertEqual(log.creator, user)
        self.assertEqual(log.food.name, self.food_name)
        self.assertEqual(log.food.desc, self.desc)
        self.assertEqual(log.food.ingredients, self.ingredients)
        self.assertEqual(log.food.calories, self.calories)

    def test_valid_log_creation_exists_in_view(self):
        """
        Valid log creation should show correct data in logs index
        """
        self.login_default_user()
        form_data = self.populate_log_create_form()

        self.client.post(reverse('logs:create-log'), form_data)
        response = self.client.get(reverse('logs:index'))
        user = User.objects.get(pk=1)

        self.assertContains(response, f"{user.username} uploaded")
        self.assertContains(response, f"{self.food_name}")
