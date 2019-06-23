import json
import socket
import threading
import time

from discovery.config import DISCOVERY_RESPONSE_PORT
from discovery.libs.utils import retrieve_logger, get_ip_address
from discovery.on_demand.request_handler import ClientRequestHandler


class UDPServer(object):
    HOST = ""
    PORT = DISCOVERY_RESPONSE_PORT
    MAX_ATTEMPTS = 20
    RESPONSE_BUFFER_SIZE = 4096
    DISCOVERY_MESSAGE = {
        "message": "HELLO, I'M THE HUB",
        "port": 7001,
        "ip": get_ip_address(),
    }

    def __init__(self, *args, **kwargs):
        self.logger = retrieve_logger("on_demand")
        self.timeout = kwargs.get("timeout", 20)

    def _send_discovery_mechanism(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.logger.info("Start broadcasting discovery messages")
        broadcast_address = ("255.255.255.255", 9000)
        while True:
            sock.sendto(json.dumps(self.DISCOVERY_MESSAGE).encode("utf-8"), broadcast_address)
            time.sleep(1)

    def start(self):

        threading.Thread(target=self._send_discovery_mechanism, daemon=True).start()

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(self.timeout)
        sock.bind((self.HOST, self.PORT))

        self.logger.debug("Waiting connection at {}".format(self.PORT))
        while True:
            try:
                data, address = sock.recvfrom(4096)
            except:
                # self.logger.info("Timeout for socket read")
                continue

            client_response_handler = ClientRequestHandler(data, address, self.logger)
            client_response_handler.start()


if __name__ == '__main__':
    server = UDPServer()
    server.start()
