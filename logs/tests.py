import datetime
import random

from django.test import TestCase
from django.utils import timezone

from .models import Comment

# Create your tests here.
class CommentModelTests(TestCase):
    def test_comment_is_recent_from_future(self):
        # is_recent should return False if the pub_date is from the future
        time = timezone.now() + datetime.timedelta(days=random.randint(2, 100))
        future_comment = Comment(pub_date=time)

        self.assertIs(future_comment.is_recent(), False)
