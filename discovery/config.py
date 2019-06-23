import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGS_FOLDER = os.path.join(PROJECT_ROOT, "logs")

DISCOVERY_REQUEST_BROADCAST_PORT = 7000
DISCOVERY_RESPONSE_PORT = 7001

BROADCAST_ADDRESS = "255.255.255.255"
