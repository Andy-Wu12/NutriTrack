import shutil
import tempfile

from django.urls import reverse

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from test_util import image_upload_util, log_util, account_util

MEDIA_ROOT = tempfile.mkdtemp() + "/media"
MEDIA_URL = "/media/"


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
@override_settings(MEDIA_URL=MEDIA_URL)
class LogImageUploadTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.user = account_util.create_default_valid_user()
        self.client.force_login(self.user)

    def test_log_with_image_renders_img_tag(self):
        """
        A log with an image should be have an img tag in it's response HTML
        """
        log_image = image_upload_util.get_default_valid_image()
        uploaded_image = SimpleUploadedFile('img.gif', log_image, content_type='image/gif')
        log = log_util.create_random_log(self.user, uploaded_image)

        response = self.client.get(reverse('logs:detail', args=[log.id]))
        self.assertContains(response, '<img ')

    def test_log_has_correct_uploaded_image(self):
        """
        Test that a log with an associated image should be rendered with the correct path
        """
        log_image = image_upload_util.get_default_valid_image()
        uploaded_image = SimpleUploadedFile('img.gif', log_image, content_type='image/gif')
        log = log_util.create_random_log(self.user, uploaded_image)

        response = self.client.get(reverse('logs:detail', args=[log.id]))
        self.assertContains(response, f'src=\'{MEDIA_URL}{log.food.image}\'')

    def test_log_with_no_image_renders_no_img(self):
        """
        Logs with no associated image should not return an img tag in the GET response
        """
        log = log_util.create_random_log(self.user)

        response = self.client.get(reverse('logs:detail', args=[log.id]))
        self.assertNotContains(response, '<img ')
        # But is still actually the log itself
        self.assertContains(response, log.food.name)
        self.assertContains(response, log.food.desc)

    def test_create_log_with_image_redirects_to_logs_index(self):
        """
        Valid log creation should redirect user to logs index
        """
        food_form = {
            'name': log_util.generateRandStr(5),
            'desc': log_util.generateRandStr(5),
            'ingredients': log_util.generateRandStr(10),
            'calories': 200
        }

        log_image = image_upload_util.get_default_valid_image()
        uploaded_image = SimpleUploadedFile('img.gif', log_image, content_type='image/gif')
        food_form['image'] = uploaded_image

        response = self.client.post(reverse('logs:create-log'), food_form)
        self.assertRedirects(response, reverse('logs:index'))

        response = self.client.get(reverse('logs:index'))
        self.assertContains(response, food_form['name'])

    def test_create_log_with_no_image_is_valid(self):
        """
        Log creation should be valid even if no image is provided
        """
        food_form = {
            'name': log_util.generateRandStr(5),
            'desc': log_util.generateRandStr(5),
            'ingredients': log_util.generateRandStr(10),
            'calories': 200
        }

        response = self.client.post(reverse('logs:create-log'), food_form)
        self.assertRedirects(response, reverse('logs:index'))

        response = self.client.get(reverse('logs:index'))
        self.assertContains(response, food_form['name'])
