from otree.api import *
import time

doc = """
Market game experiment with dynamic video rooms using Dyte API (client-side integration)
"""

class Constants(BaseConstants):
    name_in_url = 'T4_video_chat'
    players_per_group = 3
    num_rounds = 2
    first_dice_round = 2
    num_consumers = 6
    consumer_endowment = cu(100)
    exchange_rate = 1500

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    min_price = models.IntegerField()  # Add this field to store min_price


class Player(BasePlayer):
    price = models.IntegerField(
        min=0, max=100,
        label="What price (0-100) will you choose in this period?"
    )
    profit = models.CurrencyField(initial=0)
    total_profit = models.CurrencyField(initial=0)

    def firm_name(self):
        return f'Firm {chr(65 + self.id_in_group - 1)}'

# PAGES
class AboutToBegin(Page):
    pass

def group_by_arrival_time_method(subsession, waiting_players):
    grouping = subsession.session.config['gender_grouping']

    if grouping and len(grouping) > 0:
        m_players = [p for p in waiting_players if p.participant.gender == 'Male']
        f_players = [p for p in waiting_players if p.participant.gender == 'Female']

        if grouping.lower() == 'mixed':
            if len(f_players) == len(m_players):
                grouping = ['FFM', 'MMF'][random.randint(0, 1)]
            elif len(f_players) > len(m_players):
                grouping = 'FFM'
            else:
                grouping = 'MMF'

        players = m_players[:grouping.count('M')] + f_players[:grouping.count('F')]

        if len(players) == Constants.players_per_group:
            # Shuffle the list so the players won't appear sorted by gender
            random.shuffle(players)
            return players
    elif len(waiting_players) >= Constants.players_per_group:
        return waiting_players[:Constants.players_per_group]

    # Check if any of the players have been waiting too long
    timeout = subsession.session.config['wait_page_timeout']
    for player in waiting_players:
        if (time.time() - player.participant.wait_page_arrival_time) > timeout:
            # Make a single-player group
            player.participant.waited_too_long = True
            return [player]


class WaitForGrouping(WaitPage):
    group_by_arrival_time = True
    body_text = '''Waiting for the other participants.
<p>
Please note that the experiment requires at least three participants, so we ask that you wait up to 10 minutes.
If no other participant has shown up by then, you will be redirected to another page.
<p>
Thank you for your patience.
'''

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

class WaitedTooLong(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.waited_too_long

    def vars_for_template(player: Player):
        if player.participant.gender == 'Female':
            qualtrics_link = player.session.config['female_qualtrics_link']
        else:
            qualtrics_link = player.session.config['male_qualtrics_link']

        return {
            'qualtrics_link': qualtrics_link
        }

class VideoChatPage(Page):
    timeout_seconds = 80  

    @staticmethod
    def vars_for_template(player: Player):
        other_firms = []
        nicknames = []

        for p in player.group.get_players():
            firm_name = p.firm_name()  # Correctly calling the method
            if p.id_in_group != player.id_in_group:
                other_firms.append(f'<b>{firm_name}</b>')
                nicknames.append(firm_name)  # Append normally
            else:
                nicknames.append(f"{firm_name} (You)")  # Append "(You)" for the current player

        if len(other_firms) == 1:
            other_firms_text = other_firms[0]
        elif len(other_firms) == 2:
            other_firms_text = ' and '.join(other_firms)
        else:
            other_firms_text = ', '.join(other_firms[:-1]) + ' and ' + other_firms[-1]

        return {
            'round_number': player.round_number,
            'id_in_group': player.id_in_group,
            'other_firms': other_firms_text,
            'nicknames': nicknames
        }

    
class PriceSetting(Page):
    timeout_seconds = 180
    form_model = 'player'
    form_fields = ['price']

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        if timeout_happened:
            participant.is_dropout = True

class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        players = group.get_players()
        prices = [p.price for p in players]
        min_price = min(prices)  # Calculate minimum price

        group.min_price = min_price  # Store min_price at group level

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


class TerminateInCaseOfDropout(Page):
    template_name = 'TerminateInCaseOfDropout.html'

    @staticmethod
    def is_displayed(player: Player):
        if any(p.participant.is_dropout for p in player.group.get_players()):
            return True

        return False

class ResultsPage(Page):
    timer_text = "Time left until the beginning of the next round:"
    timeout_seconds = 15

    @staticmethod
    def vars_for_template(player: Player):
        lowest_price = min([p.price for p in player.group.get_players()])
        return {
            'lowest_price': lowest_price,
            'players_info': [
                {'firm_name': p.firm_name(), 'price': p.price}
                for p in player.group.get_players()
            ],
            'earnings': player.profit,
            'each_consumer_subtracted': -lowest_price,
            'group_consumers_subtracted': -(lowest_price * Constants.num_consumers)
        }


class FinalPage(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(player: Player):
        payoff = player.participant.payoff

        other_players = [p for p in player.group.get_players() if p.id_in_group != player.id_in_group]
        other_players_payoffs = [1.5+ p.participant.payoff.to_real_world_currency(player.session) for p in other_players]

        return {
            'payoff_in_real_world_currency': payoff.to_real_world_currency(player.session),
            'other_players_payoffs': other_players_payoffs
        }


class DiceRollPage(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number >= Constants.first_dice_round

    @staticmethod
    def js_vars(player):
        return dict(
            round_number=player.round_number
        )

    def vars_for_template(player: Player):
        if player.round_number < Constants.num_rounds:
            message = "The virtual dice roll determined that the experiment will continue."
        else:
            message = "The outcome of the virtual dice roll determined that the experiment has ended. You will now be directed to the questionnaire. You will see the summary of the payoffs and your earnings after you finish the questionnaire."
        
        return {
            "round_number_message": message
        }

def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        # Initialize 'is_dropout' to False in all participants
        for player in subsession.get_players():
            player.participant.is_dropout = False

page_sequence = [
                 WaitForGrouping,
                 WaitedTooLong,
                 AboutToBegin,
                 VideoChatPage, 
                 PriceSetting, 
                 ResultsWaitPage, 
                 TerminateInCaseOfDropout, 
                 ResultsPage, 
                 DiceRollPage,
                 #FinalPage
                 ]
