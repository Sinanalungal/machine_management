from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Axis
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .serializers import WebsocketDataSerailizer 
import json

@receiver(post_save, sender=Axis)
def send_axis_datas(sender, instance, **kwargs):
    """
    Signal handler to send axis data to a WebSocket group when an Axis instance is saved.
    
    Args:
        sender: The model class that sent the signal.
        instance: The instance of the model that was saved.
        **kwargs: Additional keyword arguments.
        
    Sends serialized Axis data to the 'machine_data_group' WebSocket group.
    Handles exceptions and prints errors if sending fails.
    """
    print('Entering signal handler')
    channel_layer = get_channel_layer()
    # print(channel_layer,'this is the channel layer')
    # print(instance)
    
    chat_room = 'machine_data_group' 

    try:
        serializer = WebsocketDataSerailizer(instance)
        data = serializer.data
        
        async_to_sync(channel_layer.group_send)(
            chat_room,
            {
                'type': 'send_machine_data',
                'data': data 
            }
        )

        print('data sent to chat room')
    except Exception as e:
        print(f'Error sending message: {e}')
