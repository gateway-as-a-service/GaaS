import requests

from configs.config import GATEWAY_UUID, GATEWAY_NAME, GATEWAY_DESCRIPTION, GASS_SERVER_API_URL, HTTPStatusCodes
from discovery.libs.utils import get_external_ip_address, FakeLogger


class RegisterService(object):
    def __init__(self, *args, **kwargs):
        self.logger = kwargs.get("logger") or FakeLogger()

    def register_gateway(self):
        gateway_data = {
            "uuid": GATEWAY_UUID,
            "name": GATEWAY_NAME,
            "description": GATEWAY_DESCRIPTION,
            "ip": get_external_ip_address(),
            "port": 6001
        }
        self.logger.debug("Gateway Server Info: {}".format(gateway_data))
        try:
            url = "{}/gateways".format(GASS_SERVER_API_URL)
            response = requests.post(url, json=gateway_data)
            if response.status_code == HTTPStatusCodes.CREATED:
                self.logger.debug("Gateway has been registered")
                return True

            if response.status_code == HTTPStatusCodes.CONFLICT:
                self.logger.debug("Gateway has already been registered")
                return True

            return False
        except Exception as err:
            self.logger.error("Failed to register the gateway. Reason: {}".format(err))
            return True

    def register_device(self, device):
        self.logger.debug("Register the device to GasS Server: {}".format(device))
        try:
            url = "{}/devices".format(GASS_SERVER_API_URL)
            response = requests.post(url, json=device)
            if response.status_code == HTTPStatusCodes.CREATED:
                self.logger.info("The device has been registered")
                return True

            if response.status_code == HTTPStatusCodes.CONFLICT:
                self.logger.info("The device has already been registered")
                return True

            return False
        except Exception as err:
            self.logger.error(
                "Failed to register the device {}. Reason: {}".format(device, err))
            return False

    def register_rule(self, rule):
        pass
