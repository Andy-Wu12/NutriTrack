
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
        - [ ]  Integrate an API to automatically provide nutrition information based on food name input
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
- [ ]  User Following
    - [ ]  Users should be able to follow other users
    - [ ]  News feed for logs related to users followed
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file:

`SECRET_KEY`, which Django uses for cryptographic signing. 
Read more about this [here](https://docs.gitguardian.com/secrets-detection/detectors/specifics/django_secret_key)


## Demo

https://awuswe.pythonanywhere.com/

