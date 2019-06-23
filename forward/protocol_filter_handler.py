import json

from walrus import Walrus

from receivers.config import REDIS_PORT, REDIS_HOSTNAME


class ProtocolFilterHandler(object):
    PROTOCOLS_FILTER_QUEUES_NAME = {
        "MQTT": "devices/mqtt",
        "COAP": "devices/coap",
    }

    def __init__(self, logger):
        self.logger = logger

        self.walrus = Walrus(REDIS_HOSTNAME, REDIS_PORT)

    def parse(self, message):
        protocol = message["device_info"]["protocol"]
        protocol_queue_name = self.PROTOCOLS_FILTER_QUEUES_NAME[protocol]
        protocol_queue = self.walrus.List(protocol_queue_name)
        protocol_queue.append(json.dumps(message))

        self.logger.info("Pushed the message {} to queue {}".format(message, protocol_queue_name))
