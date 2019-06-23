import numpy as np


def computer_percentiles(file_location, percentiles):
    values = []
    with open(file_location, mode="rt") as file_handler:
        for line in file_handler:
            latency = line.strip()
            if not latency:
                continue

            latency = float(latency)
            values.append(latency)

    return np.percentile(values, percentiles)


if __name__ == '__main__':
    parameters = [
        # ("../receivers/latencies/latency_1_device.txt", "Latency 1 Device"),
        # ("../receivers/latencies/latency_2_device.txt", "Latency 2 Device"),
        # ("../receivers/latencies/latency_3_device.txt", "Latency 3 Device"),
        # ("../receivers/latencies/latency_4_device.txt", "Latency 4 Device"),
        # ("../receivers/latencies/latency_5_device.txt", "Latency 5 Device"),
        # ("../receivers/latencies/latency_10_device.txt", "Latency 10 Device"),

        ("../receivers/mqtt/latency_1_device.txt", "[MQTT} Latency 1 Device"),
        ("../receivers/mqtt/latency_2_devices.txt", "[MQTT} Latency 2 Device"),
        ("../receivers/mqtt/latency_3_devices.txt", "[MQTT} Latency 3 Device"),
        ("../receivers/mqtt/latency_4_devices.txt", "[MQTT} Latency 4 Device"),
        ("../receivers/mqtt/latency_5_devices.txt", "[MQTT} Latency 5 Device"),
        ("../receivers/mqtt/latency_10_devices.txt", "[MQTT} Latency 10 Device"),

        ("../receivers/coap/latency_1_device.txt", "[CoAP] Latency 1 Device"),
        ("../receivers/coap/latency_2_devices.txt", "[CoAP] Latency 2 Device"),
        ("../receivers/coap/latency_3_devices.txt", "[CoAP] Latency 3 Device"),
        ("../receivers/coap/latency_4_devices.txt", "[CoAP] Latency 4 Device"),
        ("../receivers/coap/latency_5_devices.txt", "[CoAP] Latency 5 Device"),
        ("../receivers/coap/latency_10_devices.txt", "[CoAP] Latency 10 Device"),

        # ("../receivers/latency_1_device.txt", "[NEW] Latency 1 Device"),
        # ("../receivers/latency_2_devices.txt", "[NEW] Latency 2 Devices"),
        # ("../receivers/latency_3_devices.txt", "[NEW] Latency 3 Devices"),
        # ("../receivers/latency_4_devices.txt", "[NEW] Latency 4 Devices"),
        # ("../receivers/latency_5_devices.txt", "[NEW] Latency 5 Devices"),
        # ("../receivers/latency_10_devices.txt", "[NEW] Latency 10 Devices"),

        # ("../receivers/latencies/latency_rule_1_device.txt", "Latency Rule 1 Device"),
        # ("../receivers/latencies/latency_rule_2_devices.txt", "Latency Rule 2 Device"),
        # ("../receivers/latencies/latency_rule_3_device.txt", "Latencry Rule 3 Device"),
        # ("../receivers/latencies/latency_rule_4_device.txt", "Latency Rule 4 Device"),
        # ("../receivers/latencies/latency_rule_5_device.txt", "Latency Rules 5 Device"),

        ("../receivers/rules_local_mqtt/latency_rule_1_device.txt", "[RULE-MQTT] Latency 1 Device"),
        ("../receivers/rules_local_mqtt/latency_rule_2_devices.txt", "[RULE-MQTT] Latency 2 Device"),
        ("../receivers/rules_local_mqtt/latency_rule_3_devices.txt", "[RULE-MQTT] Latency 3 Device"),
        ("../receivers/rules_local_mqtt/latency_rule_4_devices.txt", "[RULE-MQTT] Latency 4 Device"),
        ("../receivers/rules_local_mqtt/latency_rule_5_devices.txt", "[RULE-MQTT] Latency 5 Device"),
        ("../receivers/rules_local_mqtt/latency_rule_10_devices.txt", "[RULE-MQTT] Latency 10 Device"),

        ("../receivers/rules_local_coap/latency_rule_1_device.txt", "[RULE-CoAP] Latency 1 Device"),
        ("../receivers/rules_local_coap/latency_rule_2_devices.txt", "[RULE-CoAP] Latency 2 Device"),
        ("../receivers/rules_local_coap/latency_rule_3_devices.txt", "[RULE-CoAP] Latency 3 Device"),
        ("../receivers/rules_local_coap/latency_rule_4_devices.txt", "[RULE-CoAP] Latency 4 Device"),
        ("../receivers/rules_local_coap/latency_rule_5_devices.txt", "[RULE-CoAP] Latency 5 Device"),
        ("../receivers/rules_local_coap/latency_rule_10_devices.txt", "[RULE-CoAP] Latency 10 Device"),

        ("../receivers/rules_server_mqtt/latency_rule_1_device.txt", "[RULE-SERVER-MQTT] Latency 1 Device"),
        ("../receivers/rules_server_mqtt/latency_rule_2_devices.txt", "[RULE-SERVER-MQTT] Latency 2 Device"),
        ("../receivers/rules_server_mqtt/latency_rule_3_devices.txt", "[RULE-SERVER-MQTT] Latency 3 Device"),
        ("../receivers/rules_server_mqtt/latency_rule_4_devices.txt", "[RULE-SERVER-MQTT] Latency 4 Device"),
        ("../receivers/rules_server_mqtt/latency_rule_5_devices.txt", "[RULE-SERVER-MQTT] Latency 5 Device"),
        ("../receivers/rules_server_mqtt/latency_rule_10_devices.txt", "[RULE-SERVER-MQTT] Latency 10 Device"),

        ("../receivers/latency_rule_1_device.txt", "[RULE-SERVER-COAP] Latency 1 Device"),
        ("../receivers/latency_rule_2_devices.txt", "[RULE-SERVER-COAP] Latency 2 Devices"),
        ("../receivers/latency_rule_3_devices.txt", "[RULE-SERVER-COAP] Latency 3 Devices"),
        ("../receivers/latency_rule_4_devices.txt", "[RULE-SERVER-COAP] Latency 4 Devices"),
        ("../receivers/latency_rule_5_devices.txt", "[RULE-SERVER-COAP] Latency 5 Devices"),
        ("../receivers/latency_rule_10_devices.txt", "[RULE-SERVER-COAP] Latency 10 Devices"),
    ]

    percentiles = [50, 95, 99]
    for location, name in parameters:
        print(name, computer_percentiles(location, percentiles))
