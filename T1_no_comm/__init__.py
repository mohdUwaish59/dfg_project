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
    name_in_url = 'T1_no_comm'
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
    gender = models.StringField(
        choices=['Male', 'Female', 'Diverse'],
        label='How do you see your own gender?',
        widget=widgets.RadioSelect,
    )
    age = models.IntegerField(label='Your age:')
    semester = models.IntegerField(label='Your semester number:')
    price = models.IntegerField(initial=0,
        label='Set your price (between 0 and 100):',
        min=0,
        max=100,
        blank=True
    )
    profit = models.CurrencyField(initial=c(0))
    consumer_earnings = models.CurrencyField()

class InfoPage(Page):
    form_model = 'player'
    form_fields = ['gender', 'age', 'semester']

class WaitForGrouping(WaitPage):
    group_by_arrival_time = True

class PriceSetting(Page):
    form_model = 'player'
    form_fields = ['price']
    

'''class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_profits'

    @staticmethod
    def set_profits(subsession):
        for group in subsession.get_groups():
            prices = [p.price for p in group.get_players()]
            min_price = min(prices)
            firms_with_min_price = [
                p for p in group.get_players() if p.price == min_price
            ]
            num_firms_with_min_price = len(firms_with_min_price)

            consumers_per_firm = Constants.num_consumers // num_firms_with_min_price
            remaining_consumers = Constants.num_consumers % num_firms_with_min_price

            for player in group.get_players():
                if player.price == min_price:
                    player.profit = min_price * (consumers_per_firm + (1 if remaining_consumers else 0))
                    remaining_consumers -= 1
                else:
                    player.profit = c(0)

                player.consumer_earnings = (
                    Constants.num_consumers * (Constants.consumer_endowment - min_price)
                )'''
                
class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_profits'

    @staticmethod
    def set_profits(subsession):
        for group in subsession.get_groups():
            prices = [p.price or 0 for p in group.get_players()]
            min_price = min(prices)
            firms_with_min_price = [p for p in group.get_players() if p.price == min_price]
            num_firms_with_min_price = len(firms_with_min_price)

            consumers_per_firm = Constants.num_consumers // num_firms_with_min_price
            remaining_consumers = Constants.num_consumers % num_firms_with_min_price

            for player in group.get_players():
                player_price = player.price or 0
                if player_price == min_price:
                    player.profit = player_price * (consumers_per_firm + (1 if remaining_consumers else 0))
                    remaining_consumers -= 1
                else:
                    player.profit = c(0)

                player.consumer_earnings = (
                    Constants.num_consumers * (Constants.consumer_endowment - min_price)
                )

    def after_all_players_arrive(self):
        self.set_profits(self.subsession)




class ResultsPage(Page):
    def vars_for_template(self):
        return {
            'total_profit': sum([p.profit for p in self.group.get_players()]),
            'total_consumer_earnings': sum([p.consumer_earnings for p in self.group.get_players()]),
        }

class FinalPage(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        players = self.group.get_players()
        total_profit = sum([p.profit for p in players])
        total_consumer_earnings = sum([sum(p.consumer_earnings for p in player.in_all_rounds()) for player in players])
        return {
        'total_profit': total_profit,
        'total_consumer_earnings': total_consumer_earnings,
    }



page_sequence = [
    WaitForGrouping,
    InfoPage,
    PriceSetting,
    ResultsWaitPage,
    ResultsPage,
    FinalPage,
]