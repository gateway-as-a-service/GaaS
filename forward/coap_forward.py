import json
import time

from coapthon.client.helperclient import HelperClient

from discovery.libs.utils import retrieve_logger
from forward.base_forward import BaseMessageForward
from receivers.handlers.receiver_handler import MessageReceiverHandler


class CoAPMessageForward(BaseMessageForward):
    COAP_BASE_PORT = 5682

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger = retrieve_logger("coap_forward")
        self.message_receiver_handler = MessageReceiverHandler()

    def _get_coap_url(self, device_uuid):
        return "devices-{}".format(device_uuid)

    def forward(self, device_info, new_value):
        device_uuid = device_info["device_uuid"]
        device_ip = device_info["ip"]
        device_coap_port = device_info.get("port") or self.COAP_BASE_PORT
        device_coap_url = self._get_coap_url(device_uuid)
        body = {
            "value": new_value,
        }

        attempts = 0
        while attempts < self.MAX_ATTEMPTS:
            self.logger.info("Attempt {}. Send message {} to coap server {}".format(attempts, new_value, device_ip))

            try:
                coap_client = HelperClient((device_ip, device_coap_port))
                response = coap_client.put(device_coap_url, json.dumps(body))
                if not response:
                    raise Exception("Failed to send the message to the device")

                self.logger.info("Message was sent to device")
                break

            except Exception as err:
                self.logger.error("Failed to send the message to the device {}. Reason: {}".format(device_uuid, err))
                self.logger.info("Sleep a period before retrying to send the message to device {}".format(device_uuid))

                attempts += 1
                time.sleep(self.SLEEP_PERIOD)

        if attempts == self.MAX_ATTEMPTS:
            raise Exception("Failed to forward the message")

        # Message was sent successfully. Send to be processed
        message_to_process = {
            "id": device_uuid,
            "v": new_value
        }
        self.message_receiver_handler.send_message_to_processing(message_to_process)
