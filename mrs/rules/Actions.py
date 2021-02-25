from background_task import background
from business_rules.actions import BaseActions, rule_action
from business_rules.fields import FIELD_NUMERIC


class JobActions(BaseActions):
    def __init__(self, job):
        self.job = job

    @rule_action(params={"contract_addition": FIELD_NUMERIC})
    def update_contract(self, contract_addition):
        print('action executed, task scheduled')
        self.test(creator=self.job)


    #@background(schedule=2)
    def test(self):
        print("task executed")
