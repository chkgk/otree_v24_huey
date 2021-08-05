from os import environ
from huey import RedisHuey, SqliteHuey

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

SESSION_CONFIGS = [
    dict(
       name='long_task_demo',
       display_name="long_task_demo",
       num_demo_participants=2,
       app_sequence=['long_task_demo']
    ),
]


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = 'knmws4id-5zk$&x3b=*=jsf^a0_^jm)fgo%0f9)ce)7j=q_bb4'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree', 'huey.contrib.djhuey']
EXTENSION_APPS = ['long_task_demo']

if environ.get('REDIS_URL', False):
    HUEY = RedisHuey()
else:
    HUEY = SqliteHuey()

