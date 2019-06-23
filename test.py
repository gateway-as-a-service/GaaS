import subprocess

if __name__ == '__main__':
    command = 'start "MQTT Micro-service" docker run gass/mqtt_forward'
    handler = subprocess.Popen(
        command,
        shell=True
    )
