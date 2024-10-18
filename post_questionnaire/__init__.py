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

author = 'Your Name'

doc = """
Your experiment description
"""

class Constants(BaseConstants):
    name_in_url = 'post_questionnaire'
    players_per_group = 3
    num_rounds = 1
    num_consumers = 6
    consumer_endowment = c(100)
    exchange_rate = 1500

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    not_accepting_better_grade = models.IntegerField(
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal,
    )
    feeling_bad_about_not_being_more_alert = models.IntegerField(
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal,
    )
    feeling_unhappy_about_coworker_being_blamed = models.IntegerField(
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal,
    )
    willingness_to_take_risks = models.IntegerField(
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        widget=widgets.RadioSelectHorizontal,
    )
    willingness_to_give_to_good_causes = models.IntegerField(
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        widget=widgets.RadioSelectHorizontal,
    )
    competitiveness = models.IntegerField(
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        widget=widgets.RadioSelectHorizontal,
    )
    assuming_best_intentions = models.IntegerField(
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        widget=widgets.RadioSelectHorizontal,
    )
    feeling_betrayed = models.IntegerField(
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        widget=widgets.RadioSelectHorizontal,
    )

class PostExterimentQuestionnaire1(Page):
    form_model = 'player'
    form_fields = [
        'not_accepting_better_grade',
        'feeling_bad_about_not_being_more_alert',
        'feeling_unhappy_about_coworker_being_blamed'
    ]

class PostExterimentQuestionnaire2(Page):
    form_model = 'player'
    form_fields = [
        'willingness_to_take_risks',
        'willingness_to_give_to_good_causes',
        'competitiveness',
        'assuming_best_intentions',
        'feeling_betrayed'
    ]

class FinalPage(Page):
    pass

page_sequence = [
    PostExterimentQuestionnaire1,
    PostExterimentQuestionnaire2,
    FinalPage,
]
