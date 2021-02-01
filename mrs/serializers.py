from django_filters.utils import get_all_model_fields
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from mrs.models import *
from mrs.utils.filter import DynamicFieldsModelSerializer


class JhaItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JhaItem
        fields = ('id',
                  'name',
                  'description',
                  'is_active',
                  'is_ticked_default',)


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


class ServiceAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceArea
        fields = ('id',
                  'name')


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = ('id',
                  'name')


class ServiceTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceTarget
        fields = ('id',
                  'name',
                  'key_name')


class PrioritiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = ('id',
                  'name',
                  'level')


class ProcessTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessType
        fields = ('id',
                  'name',
                  'description',
                  'project')


class ProcessTypeStatusSerializer(serializers.ModelSerializer):
    process_type = PrimaryKeyRelatedField(queryset=ProcessType.objects.all(), many=False)

    class Meta:
        model = ProcessTypeStatus
        fields = ('id',
                  'name',
                  'description',
                  'is_active',
                  'is_initial',
                  'is_final',
                  'sequence_number',
                  'process_type'
                  'project')


class ContactsSerializer(serializers.ModelSerializer):
    title = MetadataValuesSerializer(many=False)
    position = MetadataValuesSerializer(many=False)

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
    contract_mtn_frequency = PrimaryKeyRelatedField(many=False, queryset=ContractFrequency.objects.all())
    contact = ContactsSerializer(many=False)
    status = PrimaryKeyRelatedField(many=False, queryset=ProcessTypeStatus.objects.all())
    project = PrimaryKeyRelatedField(many=False, queryset=Project.objects.all())

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
                  'contact',
                  'contract_mtn_frequency',
                  'notes',
                  'status',
                  'project')

    def create(self, validated_data):
        contact_data = validated_data.pop('contact')
        contact = Contact.objects.create(**contact_data)
        contract = Contract.objects.create(contact=contact, **validated_data)
        return contract

    def update(self, instance, validated_data):
        contact_data = validated_data.pop('contact')
        Contact.objects.filter(id=instance.contact.id).update(**contact_data)
        instance.name = validated_data.get('name', instance.name)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.start_datetime = validated_data.get('start_datetime', instance.start_datetime)
        instance.end_datetime = validated_data.get('end_datetime', instance.end_datetime)
        instance.stand_by_datetime = validated_data.get('stand_by_datetime', instance.stand_by_datetime)
        instance.reactive_datetime = validated_data.get('reactive_datetime', instance.reactive_datetime)
        instance.cancel_datetime = validated_data.get('cancel_datetime', instance.cancel_datetime)
        instance.price = validated_data.get('price', instance.price)
        instance.notes = validated_data.get('notes', instance.notes)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


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
    project = PrimaryKeyRelatedField(many=False, queryset=Project.objects.all())

    class Meta:
        model = Agent
        fields = ('id',
                  'name',
                  'contact',
                  'project')

    def create(self, validated_data):
        contact_data = validated_data.pop('contact')
        contact = Contact.objects.create(**contact_data)
        agent = Agent.objects.create(contact=contact, **validated_data)
        return agent

    def update(self, instance, validated_data):
        if "contact" in validated_data:
            contact_data = validated_data.pop('contact')
            Contact.objects.filter(id=instance.contact.id).update(**contact_data)
        if "name" in validated_data:
            instance.name = validated_data.get('name', instance.name)
        if "project" in validated_data:
            instance.project = validated_data.get('project', instance.project)
        instance.save()

        return Agent.objects.get(id=instance.id)


class JobsSerializer(DynamicFieldsModelSerializer):
    contract = PrimaryKeyRelatedField(many=False, queryset=Contract.objects.all())
    project = PrimaryKeyRelatedField(many=False, queryset=Project.objects.all())
    group = PrimaryKeyRelatedField(many=False, queryset=Group.objects.all())
    agent = PrimaryKeyRelatedField(many=False, queryset=Agent.objects.all())
    round = PrimaryKeyRelatedField(many=False, queryset=Round.objects.all())
    lifts = LiftsSerializer(many=True, read_only=True, source='lift_set')

    class Meta:
        model = Job
        fields = ('id',
                  'number',
                  'name',
                  'contract',
                  'agent',
                  'round',
                  'floors',
                  'postcode',
                  'key_access_details',
                  'notes',
                  'position',
                  'address',
                  'suburb',
                  'group',
                  'owner_details',
                  'status',
                  'documents',
                  'project',
                  'lifts')


class GroupsSerializer(serializers.ModelSerializer):
    jobs = JobsSerializer(many=True, read_only=True, source='job_set')

    class Meta:
        model = Group
        fields = ('id',
                  'name',
                  'project',
                  'jobs')


class CountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id',
                  'name',
                  'currency_code',
                  'unlocode',)


class ProfilesSerializer(serializers.ModelSerializer):
    user = PrimaryKeyRelatedField(many=False, queryset=User.objects.all())
    projects = PrimaryKeyRelatedField(many=True, queryset=Project.objects.all())
    default_project = PrimaryKeyRelatedField(many=False, queryset=Project.objects.all())
    country = CountriesSerializer(many=False, read_only=True)

    class Meta:
        model = Profile
        fields = ('id',
                  'user',
                  'fullname',
                  'phone',
                  'email',
                  'email_verified',
                  'alternative_email',
                  'title',
                  'street_address',
                  'country',
                  'phone_verified',
                  'last_position',
                  'localization_code',
                  'currency_code',
                  'projects',
                  'default_project',
                  'is_active',
                  'avatar')


class ProjectProfilesSerializer(serializers.ModelSerializer):
    user = PrimaryKeyRelatedField(many=False, queryset=User.objects.all())

    class Meta:
        model = Profile
        fields = ('id',
                  'user',
                  'fullname')


class TechniciansSerializer(serializers.ModelSerializer):
    profile = ProfilesSerializer(many=False)

    class Meta:
        model = Technician
        fields = ('id',
                  'profile',
                  'notes',)

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        profile = Profile.objects.create(**profile_data)
        technician = Technician.objects.create(profile=profile, **validated_data)
        return technician

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        Profile.objects.filter(id=instance.profile.id).update(**profile_data)

        instance.notes = validated_data.get('notes', instance.notes)
        instance.save()
        return instance


class RoundsSerializer(serializers.ModelSerializer):
    technicians = TechniciansSerializer(many=True, read_only=True)
    project = PrimaryKeyRelatedField(many=False, queryset=Project.objects.all())

    class Meta:
        model = Round
        fields = ('id',
                  'name',
                  'is_active',
                  'colour',
                  'polygon',
                  'technicians',
                  'project')


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
                  'full_name',
                  'description')


class ServiceTargetSerializer(serializers.ModelSerializer):
    corrections = CorrectionsSerializer(many=True, source='correction_set')
    faults = FaultsSerializer(many=True, source='fault_set')

    class Meta:
        model = ServiceTarget
        fields = ('id',
                  'name',
                  'key_name',
                  'corrections',
                  'faults')


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fault
        fields = ('id',
                  'name',
                  'description')


class ProceduresSerializer(serializers.ModelSerializer):
    tasks = TasksSerializer(many=True)

    class Meta:
        model = Procedure
        fields = ('id',
                  'name',
                  'description',
                  'tasks',
                  'service_target')


class MaintenancePlansSerializer(serializers.ModelSerializer):
    lift = PrimaryKeyRelatedField(many=False, queryset=Lift.objects.all())

    class Meta:
        model = MaintenancePlan
        fields = ('id',
                  'name',
                  'lift')


class ScheduleEntriesSerializer(serializers.ModelSerializer):
    maintenance_plan = PrimaryKeyRelatedField(many=False, queryset=MaintenancePlan.objects.all())
    procedure = PrimaryKeyRelatedField(many=False, queryset=Procedure.objects.all())

    class Meta:
        model = ScheduleEntry
        fields = ('id',
                  'notes',
                  'maintenance_plan',
                  'procedure',
                  'schedule_date',
                  'workorder')


class WorkordersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workorder
        fields = '__all__'


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'


class ReportHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportHistory
        fields = '__all__'


class ProjectsSerializer(serializers.ModelSerializer):
    profiles = ProjectProfilesSerializer(many=True, source='profile_set', required=False)

    class Meta:
        model = Project
        fields = ('id',
                  'name',
                  'is_active',
                  'description',
                  'profiles')


class OperationsSerializer(serializers.ModelSerializer):
    procedure = PrimaryKeyRelatedField(many=False,
                                       queryset=Procedure.objects.all())
    schedule_entry = PrimaryKeyRelatedField(many=False,
                                            queryset=ScheduleEntry.objects.all())
    workorder = PrimaryKeyRelatedField(many=False,
                                       queryset=Workorder.objects.all())
    status = PrimaryKeyRelatedField(many=False,
                                    queryset=ProcessTypeStatus.objects.all())
    jha_check_list = JhaItemsSerializer(many=True)

    class Meta:
        model = Operation
        fields = ('id',
                  'type',
                  'notes',
                  'procedure',
                  'schedule_entry',
                  'workorder',
                  'start_datetime',
                  'end_datetime',
                  'status',
                  'jha_check_list')


class ActionsSerializer(serializers.ModelSerializer):
    operation = PrimaryKeyRelatedField(many=False,
                                       queryset=Operation.objects.all())
    task = PrimaryKeyRelatedField(many=False, queryset=Task.objects.all())
    status = PrimaryKeyRelatedField(many=False,
                                    queryset=ProcessTypeStatus.objects.all())

    class Meta:
        model = Action
        fields = ('id',
                  'operation',
                  'task',
                  'status')


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
