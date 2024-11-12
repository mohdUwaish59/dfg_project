from os import environ

SESSION_CONFIGS = [
    {
        'name': 'T1_no_comm',
        'display_name': 'No communication',
        'num_demo_participants': 3,
        'app_sequence': ['introduction', 'T1_no_comm', 'post_questionnaire'],
    },
    {
        'name': 'T2_text_chat',
        'display_name': 'Text chat',
        'num_demo_participants': 3,
        'app_sequence': ['introduction', 'T2_text_chat', 'post_questionnaire'],
    },
    {
        'name': 'T3_video_chat',
        'display_name': 'Video chat',
        'num_demo_participants': 3,
        'app_sequence': ['introduction', 'T3_video_chat', 'post_questionnaire'],
    },
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.0008333333333333333, participation_fee=2.00, doc=""
)

PARTICIPANT_FIELDS = ['gender', 'age', 'education']
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'GBP'
POINTS_CUSTOM_NAME = 'ECU'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '7520647312265'
