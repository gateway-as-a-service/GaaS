import socket
import threading
import time

from discovery.on_demand.server import UDPServer
from discovery.config import BROADCAST_ADDRESS, DISCOVERY_REQUEST_BROADCAST_PORT
from discovery.libs.utils import retrieve_logger


class BroadcastDiscoveryService(object):
    HOST = BROADCAST_ADDRESS
    PORT = DISCOVERY_REQUEST_BROADCAST_PORT
    MAX_ATTEMPTS = 20

    DISCOVERY_REQUEST_MESSAGE = "HELLO I'M THE HUB"

    def __init__(self):
        self.logger = retrieve_logger("discover_device_mechanism")
        self.udp_server = UDPServer()

    def _send_discovery_messages(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        attempts = 0
        address = (self.HOST, self.PORT)
        while attempts < self.MAX_ATTEMPTS:
            self.logger.info("Send discovery message to address: {}".format(address))
            sock.sendto(self.DISCOVERY_REQUEST_MESSAGE.encode("utf-8"), address)
            self.logger.info("Broadcast delivery message")
            time.sleep(0.5)
            attempts += 1

    def start(self):
        self.logger.debug("Starting discovery request sender")
        discovery_request_sender = threading.Thread(target=self._send_discovery_messages, daemon=True)
        discovery_request_sender.start()

        self.logger.debug("Starting UDP server")
        self.udp_server.start()

        self.logger.debug("Waiting to finish sending the broadcast messages")
        discovery_request_sender.join()

        self.logger.debug("Closing")


if __name__ == '__main__':
    broadcast_discovery_service = BroadcastDiscoveryService()
    broadcast_discovery_service.start()
