from huey.contrib.djhuey import result as huey_result
from .otree_extensions.base_consumers import BackgroundConsumer
from .models import Player


class MyBackgroundConsumer(BackgroundConsumer):
    def post_receive_json(self, content, subsession_id, round_number, group_id, player_id):
        player = Player.objects.get(
            subsession_id=subsession_id,
            group_id=group_id,
            round_number=round_number,
            id_in_group=player_id
        )

        res = huey_result(player.result_id)
        if res:
            player.task_result = res
            player.save()
            reply = {
                'message': 'got_result',
            }

            self.send_json(reply)
