import datetime
import json
import time
from concurrent.futures.thread import ThreadPoolExecutor

import requests
from walrus import Walrus

from configs.config import GATEWAY_UUID, GASS_SERVER_API_URL, HTTPStatusCodes
from discovery.libs.utils import retrieve_logger
from forward.protocol_filter_handler import ProtocolFilterHandler
from receivers.config import REDIS_HOSTNAME, REDIS_PORT, ACTIONS_TYPES
from receivers.utils import get_utc_timestamp
from rules.rules_executor import RulesExecutor
from services.devices_services import DevicesService
from services.rules_service import RulesService


class DevicesMessagesProcessor(object):
    MAX_WORKERS = 50

    GASS_SERVER_GATEWAY_DEVICES_PERFORMED_ACTIONS = "{}/gateways/{}/devices/actions" \
        .format(GASS_SERVER_API_URL, GATEWAY_UUID)
    GASS_SERVER_GATEWAY_DEVICES_RECEIVED_ACTIONS = "{}/gateways/{}/devices/actions/test" \
        .format(GASS_SERVER_API_URL, GATEWAY_UUID)

    def __init__(self):
        self.logger = retrieve_logger("messages_processor")

        self.walrus = Walrus(host=REDIS_HOSTNAME, port=REDIS_PORT)
        self.devices_messages = self.walrus.List('devices_messages')

        self.thread_pool_executor = ThreadPoolExecutor(max_workers=self.MAX_WORKERS, )

        self.devices_service = DevicesService(logger=self.logger)
        self.rules_service = RulesService(logger=self.logger)
        self.rules_executor = RulesExecutor(logger=self.logger)
        self.protocol_filter_handler = ProtocolFilterHandler(self.logger)

    def _rule_is_inside_activation_interval(self, interval_start, interval_end):
        current_date = datetime.datetime.utcnow()
        weekday_inside_interval = interval_start["weekday"] <= current_date.weekday() <= interval_end["weekday"]
        if not weekday_inside_interval:
            return False

        hour_inside_interval = interval_start["hour"] <= current_date.hour <= interval_end["hour"]
        if not hour_inside_interval:
            return False

        minute_inside_interval = interval_start["minute"] <= current_date.minute <= interval_end["minute"]
        if not minute_inside_interval:
            return False

        return True

    def _filter_rules_by_active_interval(self, rules):
        if not rules:
            return []

        valid_rules = []
        for rule in rules:
            if not rule.get("interval"):
                valid_rules.append(rule)
                continue

            interval_start = rule["interval"]["start"]
            interval_end = rule["interval"]["end"]
            if not self._rule_is_inside_activation_interval(interval_start, interval_end):
                self.logger.error(
                    "The rule {} should not be verified because at the moment rule isn't active"
                        .format(str(rule["_id"]))
                )
                continue

            valid_rules.append(rule)

        return valid_rules

    def _send_performed_actions(self, performed_actions):
        body = performed_actions
        attempts = 0
        while True:
            self.logger.info("Attempts {} to send to GaaS-Server the performed actions".format(attempts))
            try:
                response = requests.post(self.GASS_SERVER_GATEWAY_DEVICES_PERFORMED_ACTIONS, json=body)
                if response.status_code == HTTPStatusCodes.CREATED:
                    self.logger.debug("The performed actions has been sent successfully to the Gass Server")
                    return

                attempts += 1
            except Exception as err:
                self.logger.error(
                    "Failed to send the performed actions to the GaaS Server. Reason: {}".format(err),
                )

                self.logger.info("Sleeping...")
                time.sleep(5)
                attempts += 1
                self.logger.info("Retry sending the performed actions to the GaSS Server")

    def _test_forward_receive_actions(self, actions):
        body = actions
        attempts = 0

        while True:
            self.logger.info("Attempts {} to send to GaaS-Server the received actions")
            try:
                response = requests.post(self.GASS_SERVER_GATEWAY_DEVICES_RECEIVED_ACTIONS, json=body)
                if response.status_code == HTTPStatusCodes.CREATED:
                    self.logger.debug("The performed actions has been sent successfully to the Gass Server")
                    return

                attempts += 1
            except Exception as err:
                self.logger.error(
                    "Failed to send the performed actions to the GaaS Server. Reason: {}".format(err), exc_info=True,
                )

                self.logger.info("Sleeping...")
                time.sleep(5)
                attempts += 1
                self.logger.info("Retry sending the performed actions to the GaSS Server")

    def _send_devices_new_values(self, devices_new_values):
        devices_ids = [device['id'] for device in devices_new_values]
        devices = list(self.devices_service.find_multiple_devices(devices_ids))
        device_id_to_device_info = {
            device["id"]: device for device in devices
        }

        for device_new_value in devices_new_values:
            device_id, device_value = device_new_value["id"], device_new_value["value"]
            device_info = device_id_to_device_info[device_id]
            message = {
                "device_info": {
                    "device_uuid": device_id,
                    "protocol": device_info["protocol"],
                    "ip": device_info["ip"],
                    "port": device_info.get("port", 0)
                },
                "value": device_value
            }
            self.protocol_filter_handler.parse(message)

    def _parse_message(self, message):
        try:
            self.logger.debug("Received message: {}".format(message))

            device_id, new_value = message["id"], message["v"]
            updated = self.devices_service.update(device_id, new_value)
            if not updated:
                self.logger.debug("Failed to update the sensor's value")
                return

            performed_actions = [
                {
                    "type": ACTIONS_TYPES.CHANGE_VALUE, "device": device_id,
                    "value": new_value, "timestamp": get_utc_timestamp(),
                }
            ]
            self.logger.debug("Device has been updated")

            rules_to_check = list(self.rules_service.find_that_involves_devices([device_id]))
            rules_to_check = self._filter_rules_by_active_interval(rules_to_check)
            self.logger.debug("Have to check {} rules".format(len(rules_to_check)))

            devices_new_values, performed_actions_by_rules = self.rules_executor.execute(rules_to_check)
            performed_actions.extend(performed_actions_by_rules)
            self.logger.debug("Performed actions: {}".format(performed_actions))

            self.logger.debug("Send the performed actions to the server")
            self._send_performed_actions(performed_actions)

            # Send the new values to devices to update their state
            self.logger.debug("Devices new values: {}".format(devices_new_values))
            if not devices_new_values:
                return

            self._send_devices_new_values(devices_new_values)
            self.logger.debug("The new values have been sent to the devices")

        except Exception as err:
            self.logger.error(
                "Some error occurred while the message received from device was parsed. Reason: {}"
                    .format(err), exc_info=True
            )

    def _write_request_latency(self, emit_time):
        now = time.time()
        latency = now - emit_time

        with open("latency.txt", mode="a") as file_handler:
            file_handler.write("{}\n".format(latency))

        self.logger.info("Current Average Latency: {}".format(latency))

    def start(self):
        self.logger.debug("Waiting for messages from devices")

        while True:
            message = self.devices_messages.bpopleft(timeout=120)
            if not message:
                continue

            message = json.loads(message.decode())
            self.logger.info("Received message: {}".format(message))
            self.thread_pool_executor.submit(self._parse_message, message)


if __name__ == '__main__':
    devices_message_processor = DevicesMessagesProcessor()
    devices_message_processor.start()
