from django.conf.urls import url
from otree.channels.routing import websocket_routes

from ..consumers import MyBackgroundConsumer

websocket_routes += [
    url(r'^background/(?P<params>[\w,]+)/$', MyBackgroundConsumer),
]
