
# Food Log

Web application that helps users keep track of the food they eat,
along with the associated ingredients and caloric intake.

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

![Code Coverage](https://github.com/Andy-Wu12/Food-Log/actions/workflows/app-cov.yml/badge.svg?event=push) 
![Testing](https://github.com/Andy-Wu12/Food-Log/actions/workflows/django.yml/badge.svg?event=push)
![Commit Activity](https://img.shields.io/github/commit-activity/m/Andy-Wu12/Food-Log)

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)

## Features

- [x]  User Accounts
    - [x]  Sign Up
    - [x]  Login
    - [x]  Upload custom profile picture
    - [x]  Delete account
- [x]  Food Logs
    - [x]  Create logs
        - [x]  Manual input for name, description, ingredients, calories
        - [x]  Integrate an API to automatically provide nutrition information based on food name input
    - [x]  View other users' logs
    - [x]  Comment on logs
- [x]  Indexes
    - [x]  List all users
    - [x]  List all public logs
- [x]  User Settings
    - [x]  Toggle log privacy
        - [x]  Private logs hidden to unauth users
    - [x]  Change password
    - [x]  Change email
- [x]  Search Query
    - [x]  Query users by username
    - [x]  Query logs...
        - [x]  by owner's username
        - [x]  by food name
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file:

1. `SECRET_KEY` - Django uses this for cryptographic signing. 
Read more about this [here](https://docs.gitguardian.com/secrets-detection/detectors/specifics/django_secret_key)
2. `APP_ID` - Generate this key on [Edamam](https://developer.edamam.com/admin/applications) by:
   1. Signing up 
   2. Going to **Accounts**, then **Applications**
   3. Click **Create a new application**
   4. Select **Nutrition Analysis API**
   5. Enter a _name_ and _description_ and click **Create Application**
   6. Copy the value under _Application ID_ and assign it to `APP_ID`
3. `APP_KEY` - On the same page as before, copy the value under _Application Keys_
## Demo

https://awuswe.pythonanywhere.com/

