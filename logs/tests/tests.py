import random

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from logs.models import Log, Comment
from access.models import CustomUser
from access.tests.test_login import create_login_form
from test_util import log_util, account_util, settings_util

valid_uname = account_util.valid_uname
valid_pass = account_util.valid_pass
valid_email = account_util.valid_email


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


class CommentViewTests(TestCase):
    def setUp(self):
        self.user = account_util.create_random_valid_user()

    def test_get_comment_route_redirects_log(self):
        """
        GETting the add-comment route should automatically redirect user
        to corresponding log detail path
        """
        log = log_util.create_random_log(self.user)

        response = self.client.get(reverse('logs:add-comment', args=[log.id]))
        self.assertRedirects(response, reverse('logs:detail', args=[log.id]))

    def test_empty_comment_not_saved(self):
        """
        Empty input (including lengthy input with only whitespace) should
        be considered invalid
        """
        self.client.force_login(self.user)
        log = log_util.create_random_log(self.user)

        comment_form = log_util.create_comment_form('')
        self.client.post(reverse('logs:add-comment', args=[log.id]), comment_form)
        self.assertFalse(Comment.objects.filter(log=log).exists())

        comment_form = log_util.create_comment_form('     ')
        self.client.post(reverse('logs:add-comment', args=[log.id]), comment_form)
        self.assertFalse(Comment.objects.filter(log=log).exists())

    def test_comment_on_invalid_log_id_fails(self):
        """
        Users should not be able to comment on a log that doesn't exist
        """
        self.client.force_login(self.user)

        comment_form = log_util.create_comment_form('')
        response = self.client.post(reverse('logs:add-comment', args=[1]), comment_form)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(Comment.objects.all().exists())

    def test_valid_comment_saved(self):
        """
        A valid comment should be saved to db and render in template
        """
        self.client.force_login(self.user)
        log = log_util.create_random_log(self.user)

        comment_form = log_util.create_comment_form('test_random_comment')
        self.client.post(reverse('logs:add-comment', args=[log.id]), comment_form)
        self.assertTrue(Comment.objects.filter(log=log).exists())

    def test_valid_comment_strips_whitespace(self):
        """
        All leading and trailing whitespace should be stripped
        """
        self.client.force_login(self.user)
        log = log_util.create_random_log(self.user)

        comment_form = log_util.create_comment_form(' test_random_comment  ')
        self.client.post(reverse('logs:add-comment', args=[log.id]), comment_form)
        self.assertTrue(Comment.objects.filter(log=log).exists())

    def test_unauthenticated_comment_fails(self):
        """
        Unauthenticated users should not be allowed to comment
        """
        self.client.force_login(self.user)
        log = log_util.create_random_log(self.user)
        self.client.logout()

        comment_form = log_util.create_comment_form(' test_random_comment  ')
        self.client.post(reverse('logs:add-comment',
                                 args=[log.id]), comment_form)
        self.assertFalse(Comment.objects.filter(log=log).exists())

    def test_unauthorized_comment_fails_in_private_log(self):
        """
        Users that are not the owner should not be allowed to comment
        on a private log
        """
        # Create log for user1 and make it private
        self.client.force_login(self.user)
        log = log_util.create_random_log(self.user)
        self.client.post(reverse('settings:privacy'),
                         settings_util.create_log_setting_form(False))

        user2 = account_util.create_random_valid_user()
        self.client.force_login(user2)
        comment_form = log_util.create_comment_form("user2's comment!")
        self.client.post(reverse('logs:add-comment',
                                 args=[log.id]), comment_form)
        self.assertFalse(Comment.objects.filter(log=log).exists())


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
        log = log_util.create_default_log()

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
            user = log_util.create_user(f'awu{i}', save=True)
            food = log_util.create_food(user, f'test food{i}', f'test desc{i}', save=True)
            log = log_util.create_log(user, food, timezone.now(), save=True)
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
        log = log_util.create_default_log()

        response = self.client.get(reverse('logs:detail', args=(log.id, )))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Be the first to comment.")
        self.assertEqual(response.context['log'], log)
        self.assertQuerysetEqual(response.context['comment_list'], [])

    def test_past_comment(self):
        """
        Comments from the past SHOULD be rendered
        """
        log = log_util.create_default_log()
        day_offset = random.randint(1, 365)
        # Comment creator can be anyone, set as log creator for test simplicity
        comment = log_util.create_comment(log.creator, log, 'past comment',
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
        log = log_util.create_default_log()
        day_offset = random.randint(1, 365)
        log_util.create_comment(log.creator, log, 'past comment',
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
        log = log_util.create_default_log()
        day_offset = random.randint(1, 365)
        past_comment = log_util.create_comment(log.creator, log, 'this is the past',
                                               day_offset, past=True)
        log_util.create_comment(log.creator, log, 'this is the future',
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
        log = log_util.create_default_log()
        day_offset = random.randint(1, 365)
        for i in range(num_comments):
            comments.append(log_util.create_comment(log.creator, log, 'this is the past',
                            day_offset, past=True))

        response = self.client.get(reverse('logs:detail', args=(log.id,)))
        self.assertNotContains(response, "Be the first to comment.")
        self.assertEqual(response.context['log'], log)
        self.assertQuerysetEqual(response.context['comment_list'], comments, ordered=False)

    def test_valid_delete_log_request(self):
        """
        Only owner of log should be able to delete it
        Deleted log should no longer exist in db or render in templates
        """
        user = account_util.create_default_valid_user()
        self.client.force_login(user)
        log = log_util.create_random_log(user)

        response = self.client.get(reverse('logs:detail', args=[log.id]))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('logs:detail', args=[log.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Log.objects.filter(pk=log.id).exists())

    def test_invalid_delete_log_unauthenticated(self):
        """
        Unauthenticated users should not be allowed to delete logs
        """
        log = log_util.create_default_log()

        response = self.client.get(reverse('logs:detail', args=[log.id]))
        self.assertEqual(response.status_code, 200)

        self.client.post(reverse('logs:detail', args=[log.id]))
        self.assertTrue(Log.objects.filter(pk=log.id).exists())

    def test_invalid_delete_log_unauthorized(self):
        """
        Users should not be allowed to delete logs of other users
        """
        user1 = account_util.create_random_valid_user()
        user2 = account_util.create_random_valid_user()

        log = log_util.create_random_log(user1)

        # Log in user2 and attempt to delete user1's log
        self.client.force_login(user2)
        self.client.post(reverse('logs:detail', args=[log.id]))
        self.assertTrue(Log.objects.filter(pk=log.id).exists())


class LogSessionTests(TestCase):
    # Authentication status messages
    auth_index_mess = f'Hi {valid_uname}! Here are the most recent logs'
    unauth_index_mess = 'Create your own food log'
    unauth_comment_mess = 'to leave a comment'

    def setUp(self):
        log_util.create_user(username=valid_uname, password=valid_pass,
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
        log = log_util.create_default_log()
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
        log = log_util.create_default_log()
        response = self.client.get(reverse('logs:detail', args=(log.id, )))
        self.assertContains(response, self.unauth_comment_mess)

        redirect_path = reverse('access:signup')
        signup_button_html = f'<a href=\"{redirect_path}\">Sign up</a>'
        self.assertContains(response, signup_button_html, html=True)


class CreateLogTests(TestCase):
    food_name = 'test food'
    desc = 'test desc'
    ingredients = 'test ingredients'

    def create_valid_default_log(self, logged_in=True):
        if logged_in:
            login_form = create_login_form(email=valid_email, password=valid_pass)
            self.client.post(reverse('access:login'), login_form.data)

        form_data = {'name': self.food_name, 'desc': self.desc,
                     'ingredients': self.ingredients}
        self.client.post(reverse('logs:create-log'), form_data)

    def setUp(self):
        self.user = account_util.create_default_valid_user()

    def test_log_has_correct_creator(self):
        """
        Ensure created log has the correct associated user
        """
        self.create_valid_default_log(logged_in=True)
        log = Log.objects.get(pk=1)
        self.assertEqual(str(log.creator.username), valid_uname)

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


class CreateLogViewTests(TestCase):
    food_name = 'test food'
    desc = 'test desc'
    ingredients = 'test ingredients'
    calories = 100

    def login_default_user(self):
        login_form = create_login_form(email=valid_email, password=valid_pass)
        self.client.post(reverse('access:login'), login_form.data)

    def populate_log_create_form(self, name=True, desc=True, ingredients=True,
                                 ):
        form_data = {}
        if name:
            form_data['name'] = self.food_name
        if desc:
            form_data['desc'] = self.desc
        if ingredients:
            form_data['ingredients'] = self.ingredients
        return form_data

    def setUp(self):
        account_util.create_default_valid_user()

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

        self.client.post(reverse('logs:create-log'), form_data)
        log = Log.objects.get(pk=1)
        user = CustomUser.objects.get(pk=1)
        self.assertTrue(log)

        self.assertEqual(log.creator, user)
        self.assertEqual(log.food.name, self.food_name)
        self.assertEqual(log.food.desc, self.desc)
        self.assertEqual(log.food.ingredients, self.ingredients)

    def test_valid_log_creation_exists_in_view(self):
        """
        Valid log creation should show correct data in logs index
        """
        self.login_default_user()
        form_data = self.populate_log_create_form()

        self.client.post(reverse('logs:create-log'), form_data)
        response = self.client.get(reverse('logs:index'))
        user = CustomUser.objects.get(pk=1)

        self.assertContains(response, f'{user.username}')
        self.assertContains(response, 'uploaded')
        self.assertContains(response, f'{self.food_name}')
