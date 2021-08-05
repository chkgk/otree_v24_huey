from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from .tasks import add


class Calculation(Page):
    def vars_for_template(self):
        # start the task if it is not already running
        if not self.player.result_id:
            result = add(self.player.random_number1, self.player.random_number2)
            self.player.result_id = result.id
        return {}


class Decision(Page):
    pass


class Results(Page):
    pass


page_sequence = [Calculation, Decision, Results]
