from datetime import datetime, timedelta

from django.utils import timezone

from access.models import CustomUser
from logs.models import Food, Log, Comment
from test_util.util import generateRandStr
from test_util.account_util import create_random_valid_user, create_user


# Helper functions
def create_default_log():
    food = create_random_food()
    user = create_user('awu', save=True)
    log = create_log(user, food, timezone.now(), save=True)
    return log


def create_random_log(user: CustomUser):
    food = create_random_food()
    log = create_log(user, food, timezone.now(), save=True)

    return log


def create_random_food():
    user = create_random_valid_user()
    name = generateRandStr(5)
    desc = generateRandStr(6)
    food = create_food(user, name, desc, save=True)
    return food


def create_food(creator: CustomUser, name: str, desc: str,
                ingredients: str = '', calories: int = 0, save=False):
    """
    Create a food with the given `name` and `desc`, along with
    optional `ingredients`, and number of calories.
    """
    food = Food(creator=creator, name=name, desc=desc, ingredients=ingredients,
                calories=calories, image=None)

    if save:
        food.save()
    return food


def create_log(creator: CustomUser, food: Food, pub_date: datetime, save=False):
    """
    Create a food log on the given date,
    associated to `creator` and a `food`.
    """
    log = Log(creator=creator, food=food, pub_date=pub_date)

    if save:
        log.save()
    return log


def create_comment(creator: CustomUser, assoc_log: Log, comment_text: str,
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
