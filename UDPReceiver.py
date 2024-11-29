from socket import *
import json
from datetime import datetime
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

def custom_decoder(obj):
    if "timestamp" in obj:
        try:
            obj["timestamp"] = datetime.strptime(obj["timestamp"], "%Y-%m-%d %H:%M")
        except ValueError as e:
            print(f"Error parsing timestamp: {e}")
    return obj
print("The server is ready to receive")
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    
    try:
        json_string = message.decode()
        parsed_message = json.loads(json_string, object_hook=custom_decoder)
        print(f"Parsed data: {parsed_message}")
    except json.JSONDecodeError as e:
        print(f"JSON decoding failed: {e}")
        serverSocket.sendto("Invalid JSON format".encode(), clientAddress)
    except Exception as e:
        print(f"Unexpected error: {e}")
