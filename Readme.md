# oTree 2.4 and Huey

## Info
Run a background task in huey and store the result in oTree. Compatible with oTree 2.4.5.

## Setup
- mind the additional lines in settings.py
- add the otree_extensions folder to your app
- add consumers.py to your app
- add tasks.py to your app and change it so that it contains / calls your long running task


## Develop Locally
- when the environment variable REDIS_URL is not set, huey uses SQLite as the result storage
- when the environment variable REDIS_URL is set, huey uses redis as the result storage
- run in first terminal: otree devserver
- run in second terminal: python manage.py run_huey

## Heroku
- activate the second and third dyno (this may cost something)
- make sure redis addon is installed (but should be anyway with otree 2.4)
