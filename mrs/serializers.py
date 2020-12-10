from django_filters.utils import get_all_model_fields
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from mrs.models import *
from mrs.utils.filter import DynamicFieldsModelSerializer


class MetadataTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetadataType
        fields = ('id',
                  'name',)


class MetadataValuesSerializer(serializers.ModelSerializer):
    type = PrimaryKeyRelatedField(many=False, queryset=MetadataType.objects.all())

    class Meta:
        model = MetadataValue
        fields = ('id',
                  'type',
                  'value',)


class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id',
                  'name',
                  'is_active',
                  'description',)


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id',
                  'title',
                  'position',
                  'first_name',
                  'last_name',
                  'phone_number',
                  'mobile_number',
                  'email',
                  'address')


class ContractFrequenciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractFrequency
        fields = ('id',
                  'name')


class ContractsSerializer(serializers.ModelSerializer):
    contract_frequency = PrimaryKeyRelatedField(many=False, queryset=ContractFrequency.objects.all())
    contact = PrimaryKeyRelatedField(many=False, queryset=Contact.objects.all())

    class Meta:
        model = Contract
        fields = ('id',
                  'name',
                  'is_active',
                  'start_datetime',
                  'end_datetime',
                  'stand_by_datetime',
                  'reactive_datetime',
                  'cancel_datetime',
                  'price',
                  'frequency_mtn_id',
                  'contact',
                  'contract_frequency',
                  'notes')


class LiftsSerializer(serializers.ModelSerializer):
    job = PrimaryKeyRelatedField(many=False, queryset=Job.objects.all())
    brand = PrimaryKeyRelatedField(many=False, queryset=Brand.objects.all())

    class Meta:
        model = Lift
        fields = ('id',
                  'name',
                  'phone',
                  'job',
                  'model',
                  'is_active',
                  'brand',
                  'registration_number',
                  'floor',
                  'drive',
                  'has_light_trays',
                  'speed',
                  'installed_date',
                  'status')


class AgentsSerializer(serializers.ModelSerializer):
    contact = ContactsSerializer(many=False)

    class Meta:
        model = Agent
        fields = ('id',
                  'name',
                  'contact')

class CalloutsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Callout
        fields = ('__all__')

class MaintenancesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Maintenance
        fields = ('__all__')

class RepairsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Repair
        fields = ('__all__')

class JobsSerializer(DynamicFieldsModelSerializer):
    contract = PrimaryKeyRelatedField(many=False, queryset=Contract.objects.all())
    contact = PrimaryKeyRelatedField(many=False, queryset=Contact.objects.all())
    project = PrimaryKeyRelatedField(many=False, queryset=Project.objects.all())
    agent = AgentsSerializer(many=False)
    round = PrimaryKeyRelatedField(many=False, queryset=Round.objects.all())
    lifts = LiftsSerializer(many=True, read_only=True, source='lift_set')

    class Meta:
        model = Job
        fields = ('id',
                  'number',
                  'name',
                  'contact',
                  'contract',
                  'project',
                  'agent',
                  'round',
                  'lifts',
                  'notes',
                  'suburb',
                  'address')


class TechniciansSerializer(serializers.ModelSerializer):
    profile = PrimaryKeyRelatedField(many=False, queryset=Profile.objects.all())

    class Meta:
        model = Technician
        fields = ('id',
                  'profile',
                  'notes',)


class RoundsSerializer(serializers.ModelSerializer):
    technicians = TechniciansSerializer(many=True)

    class Meta:
        model = Round
        fields = ('id',
                  'name',
                  'is_active',
                  'colour',
                  'polygon',
                  'technicians')





class CorrectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Correction
        fields = ('id',
                  'name',
                  'description',
                  'service_target_id')


class FaultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fault
        fields = ('id',
                  'name',
                  'description')


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fault
        fields = ('id',
                  'name',
                  'description')


class ProceduresSerializer(serializers.ModelSerializer):
    tasks = TasksSerializer(many=True)

    class Meta:
        model = Fault
        fields = ('id',
                  'name',
                  'description',
                  'tasks',
                  'service_target')

class NotesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = ('__all__')


class ReportHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportHistory
        fields = ('__all__')

"""
SYSTEM SERIALIZERS
"""


class RulesSerializer(serializers.ModelSerializer):
    content_type = PrimaryKeyRelatedField(many=False, queryset=ContentType.objects.all())

    class Meta:
        model = Rule
        fields = ('id',
                  'content_type',
                  'name',
                  'description',
                  'conditions')


def getDynamicSerializer(model):
    return type(model.__name__ + 'DynamicSerializer',
                (serializers.ModelSerializer,),
                {'Meta':
                     type('Meta', (object,), {
                         'model': model,
                         'fields': get_all_model_fields(
                             model)
                     })
                 })

