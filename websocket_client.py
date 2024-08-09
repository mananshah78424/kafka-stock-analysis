import time

import simplejson as json
from websocket import create_connection

# Create a connection to the WebSocket
ws = create_connection("wss://api.tiingo.com/crypto")

# Prepare the subscription message
subscribe = {
    'eventName': 'subscribe',
    'authorization': '05e81df984e988bfdccfbd00bbbe05019f33e61b',
    'eventData': {
        'thresholdLevel': 5
    }
}

# Send the subscription message
ws.send(json.dumps(subscribe))

# Desired symbol to filter
desired_symbol = "ethusdt"

# Main loop
while True:
    # Receive message from the WebSocket
    message = ws.recv()
    # Parse the message
    parsed_message = json.loads(message)
    
    # Check if the message contains trading data
    if parsed_message.get("service") == "crypto_data" and parsed_message.get("messageType") == "A":
        data = parsed_message.get("data", [])
        symbol = data[1] if len(data) > 1 else None
        
        # Print message if it matches the desired symbol
        if symbol == desired_symbol:
            print(message)
    
    # Optionally, add a sleep to control message processing rate (e.g., every 5 seconds)
    
