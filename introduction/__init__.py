from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
    Page,  # Add this import
    WaitPage,  # Add this import
)

import time

author = 'Your Name'

doc = """
Your experiment description
"""

class Constants(BaseConstants):
    name_in_url = 'introduction'
    players_per_group = 3
    num_rounds = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    prolific_id = models.StringField(
        label="Prolific ID"
    )
    gender = models.StringField(
        choices=['Male', 'Female', 'Diverse'],
        label='How do you see your own gender?',
        widget=widgets.RadioSelect,
    )
    age = models.IntegerField(label='Your age:')
    education = models.StringField(
        choices=['High school', 'Bachelor', 'Master', 'PhD'],
        label='Your highest educational qualification:',
        widget=widgets.RadioSelect,
    )
    comprehension1_which_firm = models.IntegerField(
        label="Which firm will set the market price?",
        choices=[
            [1, "Firm A"],
            [2, "Firm B"],
            [3, "Firm C"]
        ],
        widget=widgets.RadioSelect,
    )
    comprehension1_profit_firm_a = models.IntegerField(
        label="What is the profit of Firm A?",
        choices=[
            [0,   "0 ECU"],
            [85,  "85 ECU"],
            [510, "510 ECU"]
        ],
        widget=widgets.RadioSelect,
    )
    comprehension1_consumer_expenditures = models.IntegerField(
        label="What are the expenditures of the consumers?",
        choices=[
            [0,  "All consumers lose 0 ECU"],
            [50, "Each consumer is deducted 50 ECU, thus all six consumers lose 300 ECU"],
            [75, "Each consumer is deducted 75 ECU, thus all six consumers lose 450 ECU"]
        ],
        widget=widgets.RadioSelect,
    )
    comprehension2_profit_firm_a = models.IntegerField(
        label="What is the profit of Firm A?",
        choices=[
            [0,   "0 ECU"],
            [70,  "70 ECU"],
            [140, "140 ECU"]
        ],
        widget=widgets.RadioSelect,
    )
    comprehension2_profit_firm_c = models.IntegerField(
        label="What is the profit of Firm C?",
        choices=[
            [0,   "0 ECU"],
            [70,  "70 ECU"],
            [140, "140 ECU"]
        ],
        widget=widgets.RadioSelect,
    )
    comprehension2_consumer_expenditures = models.IntegerField(
        label="What are the expenditures of the consumers?",
        choices=[
            [0,  "All consumers lose 0 ECU"],
            [70, "Each consumer is deducted 70 ECU, thus all six consumers lose 420 ECU"],
            [35, "Each consumer is deducted 35 ECU, thus all six consumers lose 216 ECU"]
        ],
        widget=widgets.RadioSelect,
    )

    @staticmethod
    def before_next_page(player, timeout_happened):
        # Store gender in participant vars so it can be accessed in any app
        player.participant.vars['gender'] = player.gender


class WelcomePageF3(Page):
    form_model = 'player'

    def vars_for_template(self):
        fee = self.session.config['participation_fee']
        return { 'participation_fee': fee }
 
    @staticmethod
    def is_displayed(player):
        return player.session.config['name'] in ['T1_no_comm_no_gender','T2_chat_comm_no_gender', 'T3_text_chat_gender']

class WelcomePageVideo(Page):
    form_model = 'player'

    def vars_for_template(self):
        fee = self.session.config['participation_fee']
        return { 'participation_fee': fee }

    @staticmethod
    def is_displayed(player):
        return player.session.config['name'] == 'T4_video_chat'

class InfoPage(Page):
    form_model = 'player'
    form_fields = ['gender', 'age', 'education']

    @staticmethod
    def error_message(player, values):
        if values['age'] < 18:
            return 'You must be at least 18 years old to participate'

        if values['age'] > 60:
            return 'You must be below 60 to participate'

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.gender = player.gender
        player.participant.age = player.age
        player.participant.education = player.education

class GeneralSetting(Page):
    def vars_for_template(self):
        rate = 1.0 / self.session.config['real_world_currency_per_point']
        return { 'conversion_rate': int(rate) }

class HowToEarnMoney(Page):
    pass

class TextChatStage(Page):
    @staticmethod
    def is_displayed(player):
        return player.session.config['name'] in ['T2_chat_comm_no_gender', 'T3_text_chat_gender'] 

class VideoChatStage(Page):
    @staticmethod
    def is_displayed(player):
        return player.session.config['name'] == 'T4_video_chat'

class ComprehensionQuestions1(Page):
    form_model = 'player'
    form_fields = ['comprehension1_which_firm']
    template_name = 'introduction/ComprehensionQuestionsSet1.html'

    @staticmethod
    def error_message(player, values):
        if values['comprehension1_which_firm'] != 2:
            return 'The answer was wrong. Note, Firm B will set the market price, as it has chosen the lowest price.'

class ComprehensionQuestions2(Page):
    form_model = 'player'
    form_fields = ['comprehension1_profit_firm_a']
    template_name = 'introduction/ComprehensionQuestionsSet1.html'

    @staticmethod
    def error_message(player, values):
        if values['comprehension1_profit_firm_a'] != 0:
            return 'The answer was wrong. Since Firm A has not set the lowest price, it will earn 0 ECU.'

class ComprehensionQuestions3(Page):
    form_model = 'player'
    form_fields = ['comprehension1_consumer_expenditures']
    template_name = 'introduction/ComprehensionQuestionsSet1.html'

    @staticmethod
    def error_message(player, values):
        if values['comprehension1_consumer_expenditures'] != 75:
            return 'The answer was wrong. Each consumer is deducted 75 ECU, leading to a total loss of 450 ECU for the group of six consumers.'

class ComprehensionQuestions4(Page):
    form_model = 'player'
    form_fields = ['comprehension2_profit_firm_a']
    template_name = 'introduction/ComprehensionQuestionsSet2.html'

    @staticmethod
    def error_message(player, values):
        if values['comprehension2_profit_firm_a'] != 140:
            return 'The answer was wrong. Since all three firms set the same price, they share the six consumers equally. Thus, each firm serves two consumers at a market price of 70 ECU. Firm A will earn 2 &times; 70 ECU = 140 ECU.'

class ComprehensionQuestions5(Page):
    form_model = 'player'
    form_fields = ['comprehension2_profit_firm_c']
    template_name = 'introduction/ComprehensionQuestionsSet2.html'

    @staticmethod
    def error_message(player, values):
        if values['comprehension2_profit_firm_c'] != 140:
            return 'The answer was wrong. Since all three firms set the same price, they share the six consumers equally. Thus, each firm serves two consumers at a market price of 70 ECU. Firm C will earn 2 &times; 70 ECU = 140 ECU.'

class ComprehensionQuestions6(Page):
    form_model = 'player'
    form_fields = ['comprehension2_consumer_expenditures']
    template_name = 'introduction/ComprehensionQuestionsSet2.html'

    @staticmethod
    def error_message(player, values):
        if values['comprehension2_consumer_expenditures'] != 70:
            return 'The answer was wrong. Each consumer is deducted 70 ECU, leading to a total loss of 420 ECU for the group of six consumers'

    @staticmethod
    def before_next_page(player, timeout_happened):
        # Set wait_page_arrival time, since this is the final page in this app
        player.participant.vars['wait_page_arrival_time'] = time.time()
        player.participant.vars['waited_too_long'] = False

class ConsentForm(Page):
    form_model = 'player'
    form_fields = ['prolific_id']

    def vars_for_template(self):
        fee = self.session.config['participation_fee']
        return { 'participation_fee': fee }

    @staticmethod
    def is_displayed(player):
        return player.session.config['name'] in ['T1_no_comm_no_gender','T2_chat_comm_no_gender', 'T3_text_chat_gender']

class DataProcessingPolicy(Page):
    @staticmethod
    def is_displayed(player):
        return player.session.config['name'] in ['T1_no_comm_no_gender','T2_chat_comm_no_gender', 'T3_text_chat_gender']

class ConsentFormVideo(Page):
    form_model = 'player'
    form_fields = ['prolific_id']

    def vars_for_template(self):
        fee = self.session.config['participation_fee']
        return { 'participation_fee': fee }

    @staticmethod
    def is_displayed(player):
        return player.session.config['name'] == 'T4_video_chat'

class DataProcessingPolicyVideo(Page):
    @staticmethod
    def is_displayed(player):
        return player.session.config['name'] == 'T4_video_chat'
    template_name = 'introduction/DataProcessingPolicyVideo.html'
    
class AllocationMachine(Page):
    pass
    


page_sequence = [
    WelcomePageF3,
    WelcomePageVideo,
    AllocationMachine,
    ConsentForm,
    DataProcessingPolicy,
    ConsentFormVideo,
    DataProcessingPolicyVideo,
    InfoPage,
    GeneralSetting,
    HowToEarnMoney,
    TextChatStage,
    VideoChatStage,
    ComprehensionQuestions1,
    ComprehensionQuestions2,
    ComprehensionQuestions3,
    ComprehensionQuestions4,
    ComprehensionQuestions5,
    ComprehensionQuestions6,
]
