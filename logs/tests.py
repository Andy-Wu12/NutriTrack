import random
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from .models import Comment

# Create your tests here.
class CommentModelTests(TestCase):
    def test_comment_is_recent_from_future(self):
        # is_recent is False if pub_date is from the future
        time = timezone.now() + timedelta(days=random.randint(2, 100))
        future_comment = Comment(pub_date=time)

        self.assertIs(future_comment.is_recent(), False)

    def test_comment_is_recent_from_far_past(self):
        # is_recent is False if pub_date is more than a day in the past (> 24h)
        time = timezone.now() - timedelta(days=random.randint(2, 100))
        far_past_comment = Comment(pub_date=time)

        self.assertIs(far_past_comment.is_recent(), False)

    def test_comment_is_recent_from_recent_timespan(self):
        # is_recent is True if pub_date is within 24h range in the past
        rand_hour_diff = random.randint(0, 23)
        rand_minute_diff = random.randint(0, 59)
        rand_second_diff = random.randint(0, 59)
        time = timezone.now() - timedelta(hours=rand_hour_diff,
                                          minutes=rand_minute_diff,
                                          seconds=rand_second_diff)

        recent_comment = Comment(pub_date=time)

        self.assertIs(recent_comment.is_recent(), True)
