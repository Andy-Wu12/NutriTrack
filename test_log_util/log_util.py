from datetime import datetime, timedelta

from django.utils import timezone
from django.contrib.auth.hashers import make_password

from access.models import CustomUser
from logs.models import Food, Log, Comment


# Valid user account fields
valid_uname = "appTester01"
valid_pass = "s3cureP@ssword054!"
valid_email = "apptester@foodlog.com"


# Helper functions
def create_default_valid_user():
    username = valid_uname
    email = valid_email
    password = valid_pass
    CustomUser.objects.create_user(username, email, password)


def create_user(username: str, password: str = '', fname: str = '', lname: str = '',
                email: str = '', save=False):
    """
    Create a user with the given `username`, and optional `password`,
    first name `fname`, last name `lname`, and `email`.
    These parameters are optional for testing purposes.
    """
    user = CustomUser(username=username, email=email, password=make_password(password),
                      first_name=fname, last_name=lname)

    if save:
        user.save()
    return user


def create_food(name: str, desc: str, ingredients: str = '', calories: int = 0, save=False):
    """
    Create a food with the given `name` and `desc`, along with
    optional `ingredients`, and number of calories.
    """
    food = Food(name=name, desc=desc, ingredients=ingredients,
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


def create_default_food():
    food = create_food('test food', 'test desc', save=True)
    return food


def create_default_log():
    food = create_default_food()
    user = create_user('awu', save=True)
    log = create_log(user, food, timezone.now(), save=True)
    return log