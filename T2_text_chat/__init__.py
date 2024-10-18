from otree.api import *

doc = """
Market game experiment with a text chat
"""

class Constants(BaseConstants):
    name_in_url = 'market_game'
    players_per_group = 3
    num_rounds = 20
    num_consumers = 6
    consumer_endowment = cu(100)

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    price = models.IntegerField(initial=0,
        label='What price (0-100) will you choose in this round?',
        min=0,
        max=100,
        blank=True
    )
    nickname = models.StringField()

# Base class for the wait pages
class WaitPageBase(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        for player in group.get_players():
            player.nickname = 'Firm ' + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[player.id_in_group - 1]

# Wait page to be shown before the first round
# This page assigned players to groups in the order they arrival at the page
class WaitForGrouping1(WaitPageBase):
    group_by_arrival_time = True

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

# Wait page to be shown before subsequent rounds
# This page doesn't reassign groups, since we want them to persist across rounds
class WaitForGrouping2(WaitPageBase):
    @staticmethod
    def is_displayed(player):
        return player.round_number != 1

class Chat(Page):
    timeout_seconds = 60

    def vars_for_template(self):
        other_firms = []
        nicknames = []

        for player in self.group.get_players():
            if player.id_in_group != self.id_in_group:
                other_firms.append('<b>' + player.nickname + '</b>')
                nicknames.append(player.nickname)
            else:
                nicknames.append(player.nickname + ' (You)')

        if len(other_firms) == 1:
            other_firms_text = other_firms[0] 
        elif len(other_firms) == 2:
            other_firms_text = ' and '.join(other_firms)
        else:
            other_firms_text = ', '.join(other_firms[:-1]) + ' and ' + other_firms[-1]

        return {
            'other_firms': other_firms_text,
            'nicknames': nicknames
        }

class PriceSetting(Page):
    form_model = 'player'
    form_fields = ['price']

class ResultsWaitPage(WaitPage):
    body_text = "Please wait until all other firms in your market have reached their decisions."

    @staticmethod 
    def after_all_players_arrive(group: Group):
        players = group.get_players()
        prices = [p.price for p in players]
        min_price = min(prices)
        firms_with_min_price = [p for p in players if p.price == min_price]
        num_firms_with_min_price = len(firms_with_min_price)

        consumers_per_firm = Constants.num_consumers // num_firms_with_min_price
        remaining_consumers = Constants.num_consumers % num_firms_with_min_price

        for player in players:
            if player.price == min_price:
                player.payoff = cu(player.price * (consumers_per_firm + (1 if remaining_consumers > 0 else 0)))
                remaining_consumers -= (1 if remaining_consumers > 0 else 0)
            else:
                player.payoff = cu(0)

class ResultsPage(Page):
    timeout_seconds = 10
    timer_text = 'Time until the next round begins:'

    def vars_for_template(player: Player):
        lowest_price = min([p.price for p in player.group.get_players()])
        return {
            'each_consumer_subtracted': -lowest_price,
            'group_consumers_subtracted': -(lowest_price * Constants.num_consumers)
        }

class FinalPage(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(player: Player):
        payoff = player.participant.payoff
        return {
            'payoff_in_real_world_currency': payoff.to_real_world_currency(player.session),
        }

page_sequence = [
    WaitForGrouping1,
    WaitForGrouping2,
    Chat,
    PriceSetting,
    ResultsWaitPage,
    ResultsPage,
    FinalPage,
]
