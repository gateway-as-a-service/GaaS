# Our base image
FROM python:3-onbuild

# Run application
CMD ["python", "./forward/mqtt_forward.py"]
