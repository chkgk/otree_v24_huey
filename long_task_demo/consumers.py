from .copy_consumer import _OTreeJsonWebsocketConsumer, get_models_module
from django.conf import settings
from asgiref.sync import async_to_sync
import json


class TaskResultConsumer(_OTreeJsonWebsocketConsumer):
    def long_task_demo_message(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps(event))

    # parse the parameters passed in the websockets URL and return a dict with name: value pairs
    def clean_kwargs(self, params):
        subsession_id, round_number, group_id, player_id = params.split(',')
        return {
            'subsession_id': subsession_id,
            'round_number': int(round_number),
            'group_id': int(group_id),
            'player_id': int(player_id)
        }

    # return a unique group_name for the channel_layer so that each oTree group gets its own channel_layer
    def group_name(self, subsession_id, round_number, group_id, player_id):
        return f"ws-{subsession_id}-{round_number}-{group_id}"

    def post_connect(self, subsession_id, round_number, group_id, player_id):
        # add them to the channel_layer
        self.room_group_name = self.group_name(subsession_id, round_number, group_id, player_id)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

    # perform any actions necessary before removing a subject from the channel_layer.  In our case there's nothing to do but
    # discard them from the channel layer
    def pre_disconnect(self, subsession_id, round_number, group_id, player_id):

        # remove the player from their channel_layer
        self.room_group_name = self.group_name(subsession_id, round_number, group_id, player_id)
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # handle non-connect and non-disconnect messages.  We only expect one message, one with the 'message' of 'done'
    # When we receive that, update the group object's "firstpage_done" field to True, save it to the db, and send a
    # message to the rest of the channel_layer telling them we're done
    def post_receive_json(self, content, subsession_id, round_number, group_id, player_id):
        # print("ws_receive called", subsession_id, round_number, group_id, player_id, content['message'])

        models_module = get_models_module('long_task_demo')

        player = models_module.Player.objects.get(subsession_id=subsession_id, group_id=group_id, round_number=round_number, id_in_group=player_id)
        res = settings.HUEY.result(player.result_id)
        print('checked:', player.result_id, res)
        if res:
            player.task_result = res
            player.save()
            reply = {
                'message': 'got_result',
            }

            self.send_json(reply)
        # async_to_sync(self.channel_layer.group_send)(
        #     self.room_group_name,
        #     reply
        # )
