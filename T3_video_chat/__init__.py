from otree.api import *

doc = """
Market game experiment with dynamic video rooms using Dyte API (client-side integration)
"""

class Constants(BaseConstants):
    name_in_url = 'market_game_dyte'
    players_per_group = 3
    num_rounds = 20
    num_consumers = 6
    consumer_endowment = cu(100)
    exchange_rate = 1500

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    price = models.IntegerField(
        min=0, max=100,
        label="What price (0-100) will you choose in this period?"
    )
    profit = models.CurrencyField(initial=0)
    total_profit = models.CurrencyField(initial=0)
    consumer_earnings = models.CurrencyField(initial=0)

    def firm_name(self):
        return f'Firm {chr(65 + self.id_in_group - 1)}'

# PAGES
class WaitForGrouping(WaitPage):
    group_by_arrival_time = True

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1



class VideoChatPage(Page):
    timeout_seconds = 80  
        
    @staticmethod
    def vars_for_template(player):
        return {
            'round_number': player.round_number,
            'id_in_group': player.id_in_group,
        }
    
class PriceSetting(Page):
    form_model = 'player'
    form_fields = ['price']


class ResultsWaitPage(WaitPage):
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
                player.profit = cu(player.price * (consumers_per_firm + (1 if remaining_consumers > 0 else 0)))
                remaining_consumers -= 1
            else:
                player.profit = cu(0)

            player.payoff += player.profit
            player.total_profit += player.profit
            player.consumer_earnings = cu(Constants.num_consumers * (Constants.consumer_endowment - min_price))

class ResultsPage(Page):
    timeout_seconds = 10
    def vars_for_template(self):
        return {
            'players_info': [
                {'firm_name': p.firm_name(), 'price': p.price}
                for p in self.group.get_players()
            ],
            'earnings': self.profit,
            'each_consumer_subtracted': -self.consumer_earnings / Constants.num_consumers,
            'group_consumers_subtracted': -self.consumer_earnings
        }

class FinalPage(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'total_earnings': player.total_profit,
            'earnings_in_real_world_currency': player.total_profit.to_real_world_currency(player.session)
        }

page_sequence = [WaitForGrouping, VideoChatPage, PriceSetting, ResultsWaitPage, ResultsPage, FinalPage]
