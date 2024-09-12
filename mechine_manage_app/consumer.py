import json
from channels.generic.websocket import AsyncWebsocketConsumer


class MachineDataConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling real-time updates of machine data.
    """
    async def connect(self):
        """
        Handle WebSocket connection event. Accept the connection and add the channel to a group.
        """
        print('connected')
        
        await self.accept()
        await self.channel_layer.group_add(
            'machine_data_group',
            self.channel_name
        )
        print(f'Added to group: {self.channel_name}') 

    async def disconnect(self, close_code):
        """
        Handle WebSocket disconnection event. Remove the channel from the group.
        """
        await self.channel_layer.group_discard(
            'machine_data_group',
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Handle incoming WebSocket messages. This method is currently a placeholder and does not process any data.
        """
        pass

    async def send_machine_data(self, event):
        """
        Send machine data to the WebSocket client.
        
        Args:
            event (dict): A dictionary containing machine and axis data to be sent to the client.
        """
        print(f'data received in sending: {event}')
        # Data will be sent based on the axis of the machine (machine id and the axis name are mentioned in the type)
        response = {
            'type': f"Machine {event['data']['machine']['machine_id']} with axis: {event['data']['axis_name']}",
            'data': event['data']  
        }
        await self.send(text_data=json.dumps(response))
