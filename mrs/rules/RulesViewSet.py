from mrs.models import Rule, MrsOperator
from mrs.serializers import RulesSerializer
from mrs.utils.filter import FilteredModelViewSet


class RulesViewSet(FilteredModelViewSet):
    queryset = Rule.objects.all()
    serializer_class = RulesSerializer

    operators = {}
    operators_decode = {}

    def __init__(self, **kwargs):
        super(RulesViewSet, self).__init__(**kwargs)
        if not RulesViewSet.operators.keys():
            operators_setting = MrsOperator.objects.all()
            for operator in operators_setting:
                RulesViewSet.operators.update({operator.code: operator.rules_operator})
                RulesViewSet.operators_decode.update({operator.rules_operator: operator.code})

    def create(self, request, pk=None):
        rule_count = 0
        for rule in request.data["conditions"]["rules"]:
            entry_count = 0
            for entry in rule["conditions"]["all"]:
                engine_operator = RulesViewSet.operators[entry["operator"]]
                request.data["conditions"]["rules"][rule_count]["conditions"]["all"][entry_count][
                    "operator"] = engine_operator
                entry_count = entry_count + 1
            rule_count = rule_count + 1

        return super(RulesViewSet, self).create(request, pk=None)

    def list(self, request, *args, **kwargs):
        r = super(RulesViewSet, self).list(request, *args, **kwargs)
        results_count = 0
        for result in r.data["results"]:
            rule_count = 0
            try:
                for rule in result["conditions"]["rules"]:
                    entry_count = 0
                    for entry in rule["conditions"]["all"]:
                        gui_operator = RulesViewSet.operators_decode[entry["operator"]]
                        r.data["results"][results_count]["conditions"]["rules"][rule_count]["conditions"]["all"][entry_count][
                            "operator"] = gui_operator
                        entry_count = entry_count + 1
                    rule_count = rule_count + 1
                results_count = results_count + 1
            except KeyError as e:
                results_count = results_count + 1
                print('empty rule ' + str(e))
        return r

    def retrieve(self, request, pk):
        r = super(RulesViewSet, self).retrieve(request, pk)
        rule_count = 0
        try:
            for rule in r.data["conditions"]["rules"]:
                entry_count = 0
                for entry in rule["conditions"]["all"]:
                    gui_operator = RulesViewSet.operators_decode[entry["operator"]]
                    r.data["conditions"]["rules"][rule_count]["conditions"]["all"][entry_count][
                        "operator"] = gui_operator
                    entry_count = entry_count + 1
                rule_count = rule_count + 1
        except KeyError as e:
            rule_count = rule_count + 1
            print('empty rule ' + str(e))
        return r
        return r
