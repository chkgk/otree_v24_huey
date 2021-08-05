from django.conf import settings
from channels.generic.websocket import JsonWebsocketConsumer
from importlib import import_module
from asgiref.sync import async_to_sync

import json
import logging
import otree.channels.utils as channel_utils

ALWAYS_UNRESTRICTED = 'ALWAYS_UNRESTRICTED'
UNRESTRICTED_IN_DEMO_MODE = 'UNRESTRICTED_IN_DEMO_MODE'

logger = logging.getLogger(__name__)


def get_models_module(app_name):
    module_name = '{}.models'.format(app_name)
    return import_module(module_name)

#  Copied from otree.channels.consumers.py - where Chris asks not to directly subclass but rather copy this over
#  It provides a basic implementation of a consumer with several functions to be defined by the implementing class
class _OTreeJsonWebsocketConsumer(JsonWebsocketConsumer):
    '''
    THIS IS NOT PUBLIC API.
    Third party apps should not subclass this.
    Either copy this class into your code,
    or subclass directly from JsonWebsocketConsumer,
    '''

    def group_send_channel(self, type: str, groups=None, **event):
        print('in group_send_channel')
        for group in (groups or self.groups):
            channel_utils.sync_group_send(group, {'type': type, **event})
            #print('call_args', channel_utils.sync_group_send.call_args)
            #assert channel_utils.sync_group_send.call_args

    def clean_kwargs(self, **kwargs):
        '''
        subclasses should override if the route receives a comma-separated params arg.
        otherwise, this just passes the route kwargs as is (usually there is just one).
        The output of this method is passed to self.group_name(), self.post_connect,
        and self.pre_disconnect, so within each class, all 3 of those methods must
        accept the same args (or at least take a **kwargs wildcard, if the args aren't used)
        '''
        return kwargs

    def group_name(self, **kwargs):
        raise NotImplementedError()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cleaned_kwargs = self.clean_kwargs(**self.scope['url_route']['kwargs'])
        self.groups = self.connection_groups()

    def connection_groups(self, **kwargs):
        group_name = self.group_name(**self.cleaned_kwargs)
        return [group_name]

    unrestricted_when = ''

    # there is no login_required for channels
    # so we need to make our own
    # https://github.com/django/channels/issues/1241
    def connect(self):
        # need to accept no matter what, so we can at least send
        # an error message
        self.accept()

        AUTH_LEVEL = settings.AUTH_LEVEL

        auth_required = (
            (not self.unrestricted_when) and AUTH_LEVEL
            or
            self.unrestricted_when == UNRESTRICTED_IN_DEMO_MODE and AUTH_LEVEL == 'STUDY'
        )

        if auth_required and not self.scope['user'].is_staff:
            msg = 'rejected un-authenticated access to websocket'
            logger.warning(msg)
            # it's good to send an explanation so we understand e.g.
            # test failures
            self.send_json({'unauthenticated_websocket': msg})
            return
        else:
            self.post_connect(**self.cleaned_kwargs)

    def post_connect(self, **kwargs):
        pass

    def disconnect(self, message, **kwargs):
        self.pre_disconnect(**self.cleaned_kwargs)

    def pre_disconnect(self, **kwargs):
        pass

    def receive_json(self, content, **etc):
        self.post_receive_json(content, **self.cleaned_kwargs)

    def post_receive_json(self, content, **kwargs):
        pass


# In this class, you only need to change the "post_receive_json" function
class BackgroundConsumer(_OTreeJsonWebsocketConsumer):
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

    def post_receive_json(self, content, subsession_id, round_number, group_id, player_id):
        raise NotImplementedError()
