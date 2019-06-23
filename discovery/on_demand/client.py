import socket
import json
import uuid

from discovery.config import DISCOVERY_REQUEST_BROADCAST_PORT, DISCOVERY_RESPONSE_PORT
from discovery.libs.utils import get_ip_address

DEVICE_INFO = {
    'id': str(uuid.uuid4()),
    "type": "ON/OFF DEVICE",
    "name": "First Device",
    "protocol": "MQTT",
    "ip": get_ip_address(),
}

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", DISCOVERY_REQUEST_BROADCAST_PORT))

    print("Waiting connection at {}".format(DISCOVERY_REQUEST_BROADCAST_PORT))
    while True:
        data, address = sock.recvfrom(4096)
        data = str(data.decode('UTF-8'))
        print('Received ' + str(len(data)) + ' bytes from ' + str(address))
        print('Data:' + data)

        print('responding...')
        response_address = (address[0], DISCOVERY_RESPONSE_PORT)
        sent = sock.sendto(json.dumps(DEVICE_INFO).encode(), response_address)
        print('Sent confirmation back')

        data, address = sock.recvfrom(4096)
        print("Received the confirmation of device registration")
        print(data, address)
        break
