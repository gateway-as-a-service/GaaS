from discovery.libs.utils import FakeLogger, get_ip_address
from receivers.utils import MongoUtils


class DevicesService(object):
    def __init__(self, *args, **kwargs):
        self.logger = kwargs.get("logger") or FakeLogger()
        self.devices_collection = MongoUtils.devices

    def create(self, device):
        try:
            return self \
                .devices_collection \
                .insert_one(device) \
                .inserted_id

        except Exception as err:
            self.logger.error(err)
            return None

    def find_by_device_id(self, device_id):
        try:
            device = self \
                .devices_collection \
                .find_one({"id": device_id})

            return device
        except Exception as err:
            self.logger.error(err)
            return None

    def find_multiple_devices(self, devices_ids):
        try:
            devices = self \
                .devices_collection \
                .find({"id": {"$in": devices_ids}})

            return devices

        except Exception as err:
            self.logger.error("Failed to retrieve the following devices : {}. Reason: {}".format(devices_ids, err))
            return []

    def update(self, device_id, new_value):
        try:
            return self \
                .devices_collection \
                .update_one({"id": device_id}, {"$set": {"value": new_value}}) \
                .matched_count

        except Exception as err:
            self.logger.error(err)
            return 0

    def update_multiple(self, device_id_to_value: dict):
        if not device_id_to_value:
            return 0

        updated_rows = 0
        for device_id, new_value in device_id_to_value.items():
            updated_rows += self.update(device_id, new_value)

        return updated_rows


if __name__ == '__main__':
    devices_service = DevicesService()
    DEVICE_INFO = {
        'id': '0e8fc944-93e4-4c91-80ba-9f82cb979976',
        "type": "ON/OFF DEVICE",
        "name": "First Device",
        "protocol": "MQTT",
        "ip": get_ip_address(),
    }
    # print(devices_service.create(DEVICE_INFO))
    # print(devices_service.find_by_device_id(DEVICE_INFO["id"]))
    print(devices_service.update(DEVICE_INFO["id"], 55))
