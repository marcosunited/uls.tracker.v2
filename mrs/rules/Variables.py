from business_rules.variables import BaseVariables, numeric_rule_variable


class JobVariables(BaseVariables):
    def __init__(self, job):
        self.job = job

    @numeric_rule_variable
    def lifts_count(self):
        return self.job.lifts


