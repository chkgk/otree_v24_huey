from os import environ

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
INSTALLED_APPS = ['otree']


# HUEY additions:
# add your app name to this list, replacing "long_task_demo"
EXTENSION_APPS = ['long_task_demo']

INSTALLED_APPS += ['huey.contrib.djhuey']
HUEY = {
    'huey_class': 'huey.RedisHuey' if environ.get('REDIS_URL', False) else 'huey.SqliteHuey',
    'immediate': False,
    'consumer': {
        'workers': 4,  # how many background processes to run in parallel
        'worker_type': 'thread',
        'scheduler_interval': 1,  # Check schedule every second, -s.
        'check_worker_health': True,  # Enable worker health checks.
        'health_check_interval': 1,  # Check worker health every second.
    },
}

