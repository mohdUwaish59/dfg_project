from os import environ

SESSION_CONFIGS = [
    {
        'name': 'T1_no_comm_no_gender',
        'display_name': 'Treatment 1: No communication - No Gender Information',
        'num_demo_participants': 150,
        'app_sequence': ['introduction', 'T1_no_comm_no_gender', 'post_questionnaire'],
    },
    {
        'name': 'T1_no_comm_no_gender_ffm',
        'display_name': 'Treatment 1: No communication - No Gender Information - FFM',
        'num_demo_participants': 150,
        'gender_grouping': 'FFM',
        'app_sequence': ['introduction', 'T1_no_comm_no_gender', 'post_questionnaire'],
    },
    {
        'name': 'T1_no_comm_no_gender_mmf',
        'display_name': 'Treatment 1: No communication - No Gender Information - MMF',
        'num_demo_participants': 150,
        'gender_grouping': 'MMF',
        'app_sequence': ['introduction', 'T1_no_comm_no_gender', 'post_questionnaire'],
    },
    {
        'name': 'T1_no_comm_no_gender_mixed',
        'display_name': 'Treatment 1: No communication - No Gender Information - FFM/MMF',
        'num_demo_participants': 150,
        'gender_grouping': 'mixed',
        'app_sequence': ['introduction', 'T1_no_comm_no_gender', 'post_questionnaire'],
    },
    {
        'name': 'T2_chat_comm_no_gender',
        'display_name': 'Treatment 2: Chat Communication - No Gender Information',
        'num_demo_participants': 150,
        'app_sequence': ['introduction', 'T2_chat_comm_no_gender', 'post_questionnaire'],
    },
    {
        'name': 'T2_chat_comm_no_gender_ffm',
        'display_name': 'Treatment 2: Chat Communication - No Gender Information - FFM',
        'num_demo_participants': 150,
        'gender_grouping': 'FFM',
        'app_sequence': ['introduction', 'T2_chat_comm_no_gender', 'post_questionnaire'],
    },
    {
        'name': 'T2_chat_comm_no_gender_mmf',
        'display_name': 'Treatment 2: Chat Communication - No Gender Information - MMF',
        'num_demo_participants': 150,
        'gender_grouping': 'MMF',
        'app_sequence': ['introduction', 'T2_chat_comm_no_gender', 'post_questionnaire'],
    },
    {
        'name': 'T2_chat_comm_no_gender_mixed',
        'display_name': 'Treatment 2: Chat Communication - No Gender Information - FFM/MMF',
        'num_demo_participants': 150,
        'gender_grouping': 'mixed',
        'app_sequence': ['introduction', 'T2_chat_comm_no_gender', 'post_questionnaire'],
    },
    {
        'name': 'T3_text_chat_gender',
        'display_name': 'Treatment 3: Chat communication - Gender Information',
        'num_demo_participants': 150,
        'app_sequence': ['introduction', 'T3_text_chat_gender', 'post_questionnaire'],
    },
    {
        'name': 'T3_text_chat_gender_ffm',
        'display_name': 'Treatment 3: Chat communication - Gender Information - FFM',
        'num_demo_participants': 150,
        'gender_grouping': 'FFM',
        'app_sequence': ['introduction', 'T3_text_chat_gender', 'post_questionnaire'],
    },
    {
        'name': 'T3_text_chat_gender_mmf',
        'display_name': 'Treatment 3: Chat communication - Gender Information - MMF',
        'num_demo_participants': 150,
        'gender_grouping': 'MMF',
        'app_sequence': ['introduction', 'T3_text_chat_gender', 'post_questionnaire'],
    },
    {
        'name': 'T3_text_chat_gender_mixed',
        'display_name': 'Treatment 3: Chat communication - Gender Information - FFM/MMF',
        'num_demo_participants': 150,
        'gender_grouping': 'mixed',
        'app_sequence': ['introduction', 'T3_text_chat_gender', 'post_questionnaire'],
    },
    {
        'name': 'T4_video_chat',
        'display_name': 'Treatment 4: Video chat Communication',
        'num_demo_participants': 150,
        'app_sequence': ['introduction', 'T4_video_chat', 'post_questionnaire'],
    },
    {
        'name': 'T4_video_chat_ffm',
        'display_name': 'Treatment 4: Video chat Communication - FFM',
        'num_demo_participants': 150,
        'gender_grouping': 'FFM',
        'app_sequence': ['introduction', 'T4_video_chat', 'post_questionnaire'],
    },
    {
        'name': 'T4_video_chat_mmf',
        'display_name': 'Treatment 4: Video chat Communication - MMF',
        'num_demo_participants': 150,
        'gender_grouping': 'MMF',
        'app_sequence': ['introduction', 'T4_video_chat', 'post_questionnaire'],
    },
    {
        'name': 'T4_video_chat_mixed',
        'display_name': 'Treatment 4: Video chat Communication - FFM/MMF',
        'num_demo_participants': 150,
        'gender_grouping': 'mixed',
        'app_sequence': ['introduction', 'T4_video_chat', 'post_questionnaire'],
    },
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.001,
    participation_fee=3.50, # PARTICIPATION FEE updated by Mohd Uwaish on 14.08.2025
    gender_grouping=None,
    wait_page_timeout=10*60,
    female_qualtrics_link='https://wiwigoettingen.eu.qualtrics.com/jfe/form/SV_2tUCLjdfI4nGrJ4',
    male_qualtrics_link='https://wiwigoettingen.eu.qualtrics.com/jfe/form/SV_3HMQ5bldvibtgea',
    doc=""
)

PARTICIPANT_FIELDS = ['gender', 'age', 'education', 'is_dropout', 'wait_page_arrival_time', 'waited_too_long', 'total_payoff_in_real_world_currency']
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
