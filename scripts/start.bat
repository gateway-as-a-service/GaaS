SET PYTHON_EXE="E:\VirtualEnvs\Python3\GaaS\Scripts\python.exe"


start "Gateway API" %PYTHON_EXE% "../api/start.py"

:: Devices Discovery Server
start "Discovery Service" %PYTHON_EXE% "../discovery/automate/server.py"

timeout 2

start "Docker Monitor" %PYTHON_EXE% "../services/docker_monitor.py"

:: Messages Processor
start "Messages Processor" %PYTHON_EXE% "../receivers/processor.py"

