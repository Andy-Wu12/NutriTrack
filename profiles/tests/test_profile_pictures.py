import shutil
import tempfile

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from test_util import image_upload_util, account_util
from access.models import CustomUser

MEDIA_ROOT = tempfile.mkdtemp() + "/media"
MEDIA_URL = "/media/"


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
@override_settings(MEDIA_URL=MEDIA_URL)
class ProfileImageUploadTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.user = account_util.create_random_valid_user()
        self.client.force_login(self.user)
        self.user_profile_path = reverse('profiles:user', args=[self.user.id])

    def test_log_has_correct_uploaded_image(self):
        """
        Test that a custom profile picture is rendered with the correct path
        """
        profile_image = image_upload_util.get_default_valid_image()
        uploaded_image = SimpleUploadedFile('img.gif', profile_image, content_type='image/gif')
        response = self.client.post(self.user_profile_path, {'profile_picture': uploaded_image})
        self.assertRedirects(response, self.user_profile_path)

        response = self.client.get(self.user_profile_path)
        updated_user = CustomUser.objects.get(pk=self.user.id)
        self.assertContains(response, f'src=\'{MEDIA_URL}{updated_user.profile_picture}\'')

    def test_picture_upload_only_valid_for_current_user(self):
        """
        Test that a user is the only one allowed to change their own profile picture
        """
        user2 = account_util.create_random_valid_user()

        # User 1 uploads their picture
        profile_image = image_upload_util.get_default_valid_image()
        uploaded_image = SimpleUploadedFile('img.gif', profile_image, content_type='image/gif')
        self.client.post(self.user_profile_path, {'profile_picture': uploaded_image})

        # Use for comparison in upcoming lines
        updated_user = CustomUser.objects.get(pk=self.user.id)
        user1_image_path = updated_user.profile_picture
        self.client.logout()

        # User 2 attempts to change user1's profile picture
        self.client.force_login(user2)
        image_2_name = 'img2.gif'
        uploaded_image_2 = SimpleUploadedFile(image_2_name, profile_image, content_type='image/gif')
        response = self.client.post(self.user_profile_path, {'profile_picture': uploaded_image_2})
        self.assertRedirects(response, self.user_profile_path)

        # User1's profile picture should not be changed
        updated_user = CustomUser.objects.get(pk=self.user.id)
        self.assertEqual(user1_image_path, updated_user.profile_picture)

    def test_upload_form_hidden_for_other_users(self):
        """
        Upload form should only be shown if you are on your own profile
        """
        user2 = account_util.create_random_valid_user()
        self.client.logout()
        self.client.force_login(user2)

        response = self.client.get(self.user_profile_path)
        self.assertNotContains(response, '<form ')
        self.assertNotContains(response, '<button type=\"submit\">')

    def test_upload_form_hidden_for_unauth_users(self):
        """
        Anyone not logged in should not have access to the form upload
        """
        self.client.logout()

        response = self.client.get(self.user_profile_path)
        self.assertNotContains(response, '<form ')
        self.assertNotContains(response, '<button type=\"submit\">')
