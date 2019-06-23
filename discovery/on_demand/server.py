import json
import socket

from discovery.on_demand.request_handler import ClientRequestHandler
from discovery.config import DISCOVERY_RESPONSE_PORT
from discovery.libs.utils import retrieve_logger


class UDPServer(object):
    HOST = ""
    PORT = DISCOVERY_RESPONSE_PORT
    MAX_ATTEMPTS = 20
    RESPONSE_BUFFER_SIZE = 4096

    def __init__(self):
        self.logger = retrieve_logger("on_demand")

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)
        sock.bind((self.HOST, self.PORT))

        attempts = 0
        while True and attempts < self.MAX_ATTEMPTS:
            try:
                data, address = sock.recvfrom(4096)
            except Exception as err:
                print(err)
                attempts += 1
                continue

            data = data.decode("utf-8")
            data = json.loads(data)

            client_response_handler = ClientRequestHandler(data, address, self.logger, )
            client_response_handler.start()
            attempts = 0
