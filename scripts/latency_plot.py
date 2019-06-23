import matplotlib.pylab as plt

concurrent_messages = [1, 2, 3, 4, 5, 10]


def draw_percentile_mqtt():
    p99 = [339.66034, 351.30277, 385.72147, 389.82571, 442.15806, 621.68658]
    plt.plot(concurrent_messages, p99, "b", marker=".")

    p95 = [260.93750, 271.89570, 273.73451, 275.84834, 270.82471, 423.16405]
    plt.plot(concurrent_messages, p95, "y", marker=".")

    p50 = [244.62419, 247.19176, 248.56739, 247.07565, 248.97828, 250.75953]
    plt.plot(concurrent_messages, p50, "r", marker=".")

    plt.legend(['p99', 'p95', 'p50'], loc="upper left")
    plt.xlabel("Concurrent Messages")
    plt.ylabel("Milliseconds")
    plt.title("MQTT Messages Latency")

    plt.savefig("mqtt_latency.png")
    plt.show()


def draw_percentiles_coap():
    p99 = [401.53395, 401.97725, 417.50659, 436.09796, 450.42357, 494.00815]
    plt.plot(concurrent_messages, p99, "b", marker=".")

    p95 = [291.25986, 296.83069, 293.17284, 309.48843, 297.69202, 304.05540]
    plt.plot(concurrent_messages, p95, "y", marker=".")

    p50 = [264.01906, 264.56652, 263.80305, 266.69121, 265.93924, 266.49742]
    plt.plot(concurrent_messages, p50, "r", marker=".")

    plt.legend(['p99', 'p95', 'p50'], loc="upper left")
    plt.xlabel("Concurrent Messages")
    plt.ylabel("Milliseconds")
    plt.title("CoAP Messages Latency")

    plt.savefig("coap_latency.png")
    plt.show()


def draw_rules_local_mqtt():
    p99 = [25.86411, 25.98237, 26.78396, 27.59734, 28.02451, 32.00608]
    plt.plot(concurrent_messages, p99, "b", marker=".")

    p95 = [23.97443, 24.88645, 24.03966, 24.87272, 24.07440, 25.83878]
    plt.plot(concurrent_messages, p95, "y", marker=".")

    p50 = [9.03118, 9.84943, 9.96733, 9.86467, 9.83441, 9.99331]
    plt.plot(concurrent_messages, p50, "r", marker=".")

    plt.legend(['p99', 'p95', 'p50'], loc="upper left")
    plt.xlabel("Concurrent Messages")
    plt.ylabel("Milliseconds")
    plt.title("Gateway Rule Trigger Latency - MQTT")

    plt.savefig("gateway_rule_mqtt_latency.png")
    plt.show()


def draw_rules_local_coap():
    p99 = [52.00702, 52.01944, 52.03728, 52.03185, 52.01031, 52.98525]
    plt.plot(concurrent_messages, p99, "b", marker=".")

    p95 = [34.02001, 34.00555, 34.97182, 35.73335, 34.97523, 36.00502]
    plt.plot(concurrent_messages, p95, "y", marker=".")

    p50 = [12.00151, 12.00688, 12.05778, 12.91096, 12.61103, 13.02385]
    plt.plot(concurrent_messages, p50, "r", marker=".")

    plt.legend(['p99', 'p95', 'p50'], loc="upper left")
    plt.xlabel("Concurrent Messages")
    plt.ylabel("Milliseconds")
    plt.title("Gateway Rule Trigger Latency - CoAP")

    plt.savefig("gateway_rule_coap_latency.png")
    plt.show()


def draw_rules_server_mqtt():
    p99 = [241.10837, 253.04449, 255.99993, 256.59786, 271.05926, 305.06939]
    plt.plot(concurrent_messages, p99, "b", marker=".")

    p95 = [198.58073, 201.17823, 202.51538, 203.12480, 204.00528, 215.85538]
    plt.plot(concurrent_messages, p95, "y", marker=".")

    p50 = [184.07290, 184.83806, 184.68428, 184.31377, 184.39531, 184.90186]
    plt.plot(concurrent_messages, p50, "r", marker=".")

    plt.legend(['p99', 'p95', 'p50'], loc="upper left")
    plt.xlabel("Concurrent Messages")
    plt.ylabel("Milliseconds")
    plt.title("Server Rule Trigger Latency - MQTT")

    plt.savefig("server_mqtt_mqtt_latency.png")
    plt.show()


def draw_rules_server_coap():
    p99 = [259.44956, 262.94452, 264.66730, 271.73949, 300.70874, 312.31365]
    plt.plot(concurrent_messages, p99, "b", marker=".")
    p95 = [212.21839, 212.46725, 215.48322, 217.22366, 218.93442, 221.08186]
    plt.plot(concurrent_messages, p95, "y", marker=".")

    p50 = [189.69703, 188.92109, 189.15367, 189.36920, 188.91966, 188.44140]
    plt.plot(concurrent_messages, p50, "r", marker=".")

    plt.legend(['p99', 'p95', 'p50'], loc="upper left")
    plt.xlabel("Concurrent Messages")
    plt.ylabel("Milliseconds")
    plt.title("Server Rule Trigger Latency - CoAP")

    plt.savefig("server_coap_mqtt_latency.png")
    plt.show()


if __name__ == '__main__':
    draw_percentile_mqtt()
    draw_percentiles_coap()
    draw_rules_local_mqtt()
    draw_rules_local_coap()
    draw_rules_server_mqtt()
    draw_rules_server_coap()
