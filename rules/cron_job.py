import datetime
import time

from discovery.libs.utils import retrieve_logger
from rules.rules_executor import RulesExecutor
from services.rules_service import RulesService


class RulesCronJob(object):
    def __init__(self):
        self.logger = retrieve_logger("rules_cron_job")

        self.rules_service = RulesService(logger=self.logger)
        self.rules_executor = RulesExecutor(logger=self.logger)

    def _sleep(self, start_date):
        end_date = datetime.datetime.now()
        sleep_period = self._get_sleep_time(start_date, end_date)
        print(sleep_period)
        self.logger.debug("Sleep....")
        time.sleep(sleep_period)

    def _get_sleep_time(self, start_date, end_date):
        """
            Function that returns the number of seconds until the cron job should start again
        :param start_date:
        :param end_date:
        :return:
        """
        if start_date.minute == end_date.minute:
            return 60 - end_date.second - (1 - start_date.microsecond / 1000000)

        return 0

    def start(self):
        self.logger.debug("Rule Cron job has started")

        while True:
            start_date = datetime.datetime.now()
            self.logger.debug("Start job for: {}".format(start_date))

            rules_to_check = list(self.rules_service.find_with_trigger_timestamp(start_date))
            self.logger.debug("Have to check {} rule(s) should be triggered".format(len(rules_to_check)))
            if not rules_to_check:
                self._sleep(start_date)
                continue

            performed_actions = self.rules_executor.execute(rules_to_check)
            self.logger.debug("Performed actions: {}".format(performed_actions))
            self._sleep(start_date)


if __name__ == '__main__':
    rules_cron_job = RulesCronJob()
    rules_cron_job.start()
