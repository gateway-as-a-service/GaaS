import json
import time

import redis

from discovery.libs.utils import retrieve_logger, get_traceback
from forward.base_forward import BaseMessageForward

import paho.mqtt.client as mqtt

from receivers.config import REDIS_HOSTNAME, REDIS_PORT, MQTT_HOSTNAME


class MQTTMessageForward(BaseMessageForward):
    MQTT_REDIS_TOPIC = "devices/mqtt"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger = retrieve_logger("mqtt_forward")

        self.mqtt = mqtt.Client()
        self.mqtt.on_connect = self._on_connect_callback
        self.mqtt.on_publish = self._on_publish_callback

        self._connect_to_mqtt_broker()

        self.redis_connection = redis.StrictRedis(REDIS_HOSTNAME, REDIS_PORT)
        self.redis_pub_sub = self.redis_connection.pubsub()
        self.redis_pub_sub.subscribe(self.MQTT_REDIS_TOPIC)

    def _connect_to_mqtt_broker(self):
        while True:
            try:
                self.mqtt.connect(MQTT_HOSTNAME)
                return
            except Exception as err:
                self.logger.error(
                    "Failed to connect to the broker. Reason: {}".format(get_traceback())
                )
                time.sleep(5)

    def _on_connect_callback(self, client, userdata, flags, rc):
        self.logger.debug("Connected to MQTT Broker")
        self.logger.debug("Connected flags" + str(flags) + "result code " + str(rc) + "client1_id ")
        client.connected_flag = True

    def _on_publish_callback(self, client, userdata, mid):
        self.logger.debug("Published data")
        self.logger.debug(client)
        self.logger.debug(userdata)
        self.logger.debug(mid)

    def _get_mqtt_forward_message_topic(self, device_uuid):
        return "devices/{}/forward".format(device_uuid)

    def forward(self, device_info, message):
        device_uuid = device_info["device_uuid"]
        device_mqtt_topic = self._get_mqtt_forward_message_topic(device_uuid)
        body = {
            "message": message,
        }

        attempts = 0
        while attempts < self.MAX_ATTEMPTS:
            self.logger.debug(
                "Attempt {}. Publish message {} to topic {}"
                    .format(attempts, body, device_mqtt_topic)
            )

            try:
                self.mqtt.publish(device_mqtt_topic, json.dumps(body), qos=0)
                self.logger.debug("Message was published to topic: {}".format(device_mqtt_topic))
                return

            except Exception as err:
                self.logger.error("Failed to send the message to the device {}. Reason: {}".format(device_uuid, err))
                self.logger.info("Sleep a period before retrying to send the message to device {}".format(device_uuid))

                attempts += 1
                time.sleep(self.SLEEP_PERIOD)

        raise Exception("Failed to forward the message")

    def run(self):
        self.logger.info("Started MQTT Forward Micro-Service")
        while True:
            message = self.redis_pub_sub.get_message(timeout=120)
            self.logger.debug("Received message: {}".format(message))
            invalid_message = not message or message["type"] != "message"
            if invalid_message:
                continue

            try:
                message_body = json.loads(message['data'].decode("utf-8"))
                self.logger.info("Message: {}".format(message_body))
            except Exception as err:
                self.logger.error(err, exc_info=True)
                continue

            self.logger.debug("Waiting for message")


if __name__ == '__main__':
    mqtt_forward = MQTTMessageForward()
    mqtt_forward.run()
