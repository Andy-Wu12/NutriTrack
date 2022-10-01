import os

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q

from .models import Food, Log, Comment
from .forms import FoodForm, LogSearchForm
from settings.models import Privacy

import requests

# Should list all logs globally like some sort of home page feed
# Taking into account user privacy settings
def index(request):
    context = {}

    public_log_filter = get_privacy_settings(True)
    latest_logs = Log.objects.filter(
        pub_date__lte=timezone.now(), creator__in=public_log_filter).order_by('-pub_date')

    if request.method == 'POST':
        query_form = LogSearchForm(request.POST)
        if query_form.is_valid():
            # Might be better to separate query options into separate forms
            query = query_form.cleaned_data['query']
            latest_logs = latest_logs.filter(
                Q(creator__username__icontains=query) | Q(food__name__icontains=query)
            ).order_by('-pub_date')

    context['latest_logs'] = latest_logs
    context['form'] = LogSearchForm(request.POST)
    return render(request, 'logs/index.html', context)


def detail(request, log_id):
    context = {}

    log = get_object_or_404(Log, pk=log_id)
    log_privacy = Privacy.objects.get(user=log.creator.id)
    comments = log.comment_set.filter(pub_date__lte=timezone.now())

    if not log_privacy.show_logs and request.user.id != log.creator.id:
        context['privacyMessage'] = 'You do not have permission to view this log!'
    else:
        context['log'] = log
        context['comment_list'] = comments

    if request.method == 'POST':
        if request.user == log.creator:
            # One to one in log means log depends on food.
            # Deleting food will cascade log, but not vice versa
            log.food.delete()
            return HttpResponseRedirect(reverse('logs:index'))

    return render(request, 'logs/detail.html', context)


def create_log(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('access:signup'))

    if request.method == 'POST':
        # Create form instance and populate it with data from request
        form = FoodForm(request.POST, request.FILES)
        if form.is_valid():
            # Process data in form.cleaned_data
            food_name = form.cleaned_data['name']
            desc = form.cleaned_data['desc']
            ingreds = form.cleaned_data['ingredients']
            img = form.cleaned_data.get('image')

            # Calculate calories based off ingredients provided
            ingred_json = fetchIngredientData(ingreds)
            calories = parseCalorieData(ingred_json)

            food_obj = Food(creator=request.user, name=food_name, desc=desc,
                            ingredients=ingreds, calories=calories, image=img)
            food_obj.save()

            log = Log(creator=request.user, food=food_obj, pub_date=timezone.now())
            log.save()
            return HttpResponseRedirect(reverse('logs:index'))

        # Redirect to same page and render error message
        return render(request, 'logs/create-log.html',
                      {'form': form}, status=400)

    form = FoodForm()

    return render(request, 'logs/create-log.html', {'form': form})


def comment(request, log_id):
    if not request.method == 'POST':
        return HttpResponseRedirect(reverse('logs:detail', args=(log_id,)))

    # Unauthenticated cannot comment
    if request.user.is_authenticated:
        log = get_object_or_404(Log, pk=log_id)
        # Authenticated user cannot comment on other users' PRIVATE logs
        log_privacy = Privacy.objects.get(user=log.creator.id)
        if not log_privacy.show_logs and request.user != log.creator:
            return HttpResponseRedirect(reverse('logs:index'))

        try:
            comment_data = request.POST['comment-text']
        except (KeyError, Comment.DoesNotExist):
            error_message = 'Error getting comment data. Please try again!'
            return render(request, 'logs/detail.html', {'log': log,
                                                        'comment_list': log.comment_set.all(),
                                                        'error_message': error_message})
        # Get user currently signed in
        if len(comment_data.strip()) > 0:
            # request.user exists due to session cookie
            # created after login/signup
            commenter = request.user
            log = Log.objects.get(pk=log_id)

            new_comment = Comment(creator=commenter, log=log, comment=comment_data,
                                  pub_date=timezone.now())

            new_comment.save()
    # Redirect to prevent post data from being reused in case of back button click
    return HttpResponseRedirect(reverse('logs:detail', args=(log_id,)))


def get_privacy_settings(privacy_setting: bool):
    return Privacy.objects.filter(show_logs=privacy_setting).values_list('id')

def fetchIngredientData(ingredientsStr: str):
    ingredients = ingredientsStr.split(',')
    # URL encode ' '
    ingred_query = '%20and%20'.join(ingredients)

    # Get the Parsed response
    query_url = 'https://api.edamam.com/api/food-database/v2/parser'
    query_url += f'?app_id={os.getenv("APP_ID")}&app_key={os.getenv("APP_KEY")}'
    query_url += f'&ingr={ingred_query}&nutrition-type=cooking'

    response_json = requests.get(query_url).json()
    ingred_json = response_json.get('parsed')

    return ingred_json

def parseCalorieData(ingredientsInfo):
    calories = 0
    return calories
