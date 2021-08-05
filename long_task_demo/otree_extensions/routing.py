from django.conf.urls import url
from otree.channels.routing import websocket_routes

from ..consumers import TaskResultConsumer

# make sure the websocket route matches your app name!
websocket_routes += [
    url(r'^long_task_demo/(?P<params>[\w,]+)/$',
        TaskResultConsumer),
]
