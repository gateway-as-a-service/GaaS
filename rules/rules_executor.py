from discovery.libs.utils import FakeLogger
from receivers.config import ACTIONS_TYPES
from receivers.utils import get_utc_timestamp
from rules.rules_engine import RulesEngine
from services.devices_services import DevicesService


class RulesExecutor(object):

    def __init__(self, *args, **kwars):
        self.logger = kwars.get("logger") or FakeLogger()

        self.rules_engine = RulesEngine(logger=self.logger)
        self.devices_service = DevicesService(logger=self.logger)

    def execute(self, rules):
        if not rules:
            return [], []

        performed_actions = []
        devices_new_values = []
        rules_to_check = list(rules)
        for rule in rules_to_check:
            rule_id = str(rule["_id"])
            self.logger.debug("Process rule {}".format(rule_id))

            devices = self.devices_service.find_multiple_devices(rule["devices_involved"])
            device_id_to_value = {device["id"]: device["value"] for device in devices}
            missing_devices = set(rule["devices_involved"]) - device_id_to_value.keys()
            if missing_devices:
                self.logger.error("Some devices are missing {}".format(missing_devices))
                continue

            rule_was_triggered = self.rules_engine.evaluate_rule(rule, device_id_to_value)
            if not rule_was_triggered:
                self.logger.debug("Rule {} has been evaluated and wasn't triggered".format(rule_id))
                continue

            performed_actions.append(
                {"type": ACTIONS_TYPES.RULE_TRIGGERED, "rule": rule_id, "timestamp": get_utc_timestamp()}
            )
            self.logger.debug(
                "Rule {} has been evaluated and it was triggered. Perform the in cause actions"
                    .format(rule_id)
            )
            actions_to_do = rule["actions"]
            if not actions_to_do:
                self.logger.debug("No actions has to be performed for rule {}".format(rule_id))
                continue

            for device_id, new_value in actions_to_do.items():
                devices_new_values.append(
                    {"id": device_id, "value": new_value}
                )

        return devices_new_values, performed_actions
