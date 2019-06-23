import json

import redis

from configs.config import GASS_REDIS_HOSTNAME, GASS_REDIS_PORT
from discovery.libs.utils import retrieve_logger


class MessageReceiverHandler(object):
    REDIS_PUBSUB_DEVICES_MESSAGE_CHANNEL = "devices_messages"

    def __init__(self, ):
        self.redis_connection = redis.StrictRedis(GASS_REDIS_HOSTNAME, GASS_REDIS_PORT)
        self.redis_connection.pubsub()

        self.logger = retrieve_logger("device_message_receiver")

    def send_message_to_processing(self, message):
        try:
            self.logger.debug("Publish message to channel {}".format(self.REDIS_PUBSUB_DEVICES_MESSAGE_CHANNEL))
            self.redis_connection.publish(self.REDIS_PUBSUB_DEVICES_MESSAGE_CHANNEL, json.dumps(message))

        except Exception as err:
            self.logger.error(err, exc_info=True)
