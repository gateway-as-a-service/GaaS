import abc

from discovery.libs.utils import FakeLogger


class BaseMessageForward(metaclass=abc.ABCMeta):
    SLEEP_PERIOD = 5

    MAX_ATTEMPTS = 50

    def __init__(self, *args, **kwargs):
        self.logger = kwargs.get("logger") or FakeLogger()

    @abc.abstractmethod
    def forward(self, device_info, message):
        pass
