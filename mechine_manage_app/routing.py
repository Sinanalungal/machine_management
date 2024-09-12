from . import consumer
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r'^ws/machine_data/$', consumer.MachineDataConsumer.as_asgi()),
]