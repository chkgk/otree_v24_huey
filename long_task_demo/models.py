from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import random


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'long_task_demo'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    def creating_session(self):
        for player in self.get_players():
            player.random_number1 = random.randint(1, 10)
            player.random_number2 = random.randint(11, 20)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    random_number1 = models.IntegerField()
    random_number2 = models.IntegerField()

    task_result = models.IntegerField()
    result_id = models.StringField()
