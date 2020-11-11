from business_rules.actions import BaseActions, rule_action
from business_rules.fields import FIELD_NUMERIC


class JobActions(BaseActions):
    def __init__(self, job):
        self.job = job

    @rule_action(params={"contract_addition": FIELD_NUMERIC})
    def update_contract(self, contract_addition):
        print('contract addition ' + contract_addition + str(self.job.id))
