import json
from concurrent.futures.thread import ThreadPoolExecutor

import redis

from configs.config import MESSAGE_FORWARD_REDIS_PUBSUB
from discovery.libs.utils import retrieve_logger
from forward.coap_forward import CoAPMessageForward
from forward.mqtt_forward import MQTTMessageForward
from receivers.config import REDIS_PORT, REDIS_HOSTNAME
from services.devices_services import DevicesService


class MessageForwardDaemon(object):
    MAX_WORKERS = 25

    def __init__(self):
        self.logger = retrieve_logger("message_forward")
        self.devices_service = DevicesService(logger=self.logger)

        self.redis_connection = redis_connection = redis.StrictRedis(REDIS_HOSTNAME, REDIS_PORT)
        self.redis_pub_sub = redis_connection.pubsub()
        self.redis_pub_sub.subscribe(MESSAGE_FORWARD_REDIS_PUBSUB)

        self.thread_pool_executor = ThreadPoolExecutor(max_workers=self.MAX_WORKERS)

        self.message_forward_helper = {
            "MQTT": MQTTMessageForward(),
            "COAP": CoAPMessageForward(),
        }

    def _forward_message(self, message):
        protocol = message["device_info"]["protocol"]
        if protocol not in self.message_forward_helper:
            raise Exception("Unknown protocol {}".format(protocol))

        try:
            self.message_forward_helper[protocol].forward(message["device_info"], message["value"])
        except Exception as err:
            self.logger.error("Failed to send the message to the device. Reason: {}".format(err))
            self._notify_forward_failure(message)
            return

    def _notify_forward_failure(self, message):
        # TODO: Send message to GASS that failed to send the message to the device
        self.logger.critical(message)

    def start(self):
        self.logger.debug("Waiting for command messages")

        while True:

            message = self.redis_pub_sub.get_message(timeout=120)
            self.logger.debug("Received message: {}".format(message))
            invalid_message = not message or message["type"] != "message"
            if invalid_message:
                continue

            try:
                message_body = json.loads(message['data'].decode("utf-8"))
                self.thread_pool_executor.submit(self._forward_message, message_body)

            except Exception as err:
                self.logger.error(err)
                continue

            self.logger.debug("Waiting for command messages")


if __name__ == '__main__':
    message_forward_daemon = MessageForwardDaemon()
    message_forward_daemon.start()
