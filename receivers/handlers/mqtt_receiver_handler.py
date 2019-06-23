import json

import paho.mqtt.client as mqtt

from discovery.libs.utils import retrieve_logger
from receivers.handlers.receiver_handler import MessageReceiverHandler


class MQTTSubscriber(object):
    REDIS_PUBSUB_DEVICES_MESSAGE_CHANNEL = "devices_messages"

    def __init__(self, broker_address):
        self.mqtt = mqtt.Client()
        self.mqtt.on_connect = self._on_connect_callback
        self.mqtt.on_message = self._process_message_received
        self.mqtt.connect(broker_address)

        self.message_receiver_handler = MessageReceiverHandler()

        self.logger = retrieve_logger("device_message_receiver")

    def _on_connect_callback(self, client, userdata, flags, rc):
        self.logger.debug("Connected to MQTT Broker")
        client.connected_flag = True
        self.mqtt.subscribe("devices/+", qos=0)

    def _process_message_received(self, client, user_data, message):
        try:
            self.logger.info("Topic: {}".format(message.topic))
            self.logger.info("QoS: {}".format(message.qos))
            parsed_message = json.loads(message.payload.decode("utf-8"))
            self.logger.info("Message: {}".format(parsed_message))

            self.message_receiver_handler.send_message_to_processing(parsed_message)
            self.logger.info("Message has been sent to be processed")

        except Exception as err:
            print(err)

    def start(self):
        self.mqtt.loop_forever()


if __name__ == '__main__':
    mqtt_subscriber = MQTTSubscriber("127.0.0.1")
    mqtt_subscriber.start()
