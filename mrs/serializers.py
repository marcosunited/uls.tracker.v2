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
    contract_mtn_frequency = PrimaryKeyRelatedField(many=False, queryset=ContractFrequency.objects.all())
    contact = ContactsSerializer(many=False)
    status = PrimaryKeyRelatedField(many=False, queryset=ProcessTypeStatus.objects.all())

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
                  'status')

    def create(self, validated_data):
        contact_data = validated_data.pop('contact')
        contact = Contact.objects.create(**contact_data)
        contract = Contract.objects.create(contact=contact, **validated_data)
        return contract

    def update(self, instance, validated_data):
        contact_data = validated_data.pop('contact')
        Contact.objects.update(**contact_data)
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
        contact_data = validated_data.pop('contact')
        Contact.objects.update(**contact_data)
        instance.name = validated_data.get('name', instance.name)
        instance.project = validated_data.get('project', instance.project)
        instance.save()
        return instance


class JobsSerializer(DynamicFieldsModelSerializer):
    contract = PrimaryKeyRelatedField(many=False, queryset=Contract.objects.all())
    project = PrimaryKeyRelatedField(many=False, queryset=Project.objects.all())
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


class TitlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = ('id',
                  'name',)


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
    title = TitlesSerializer(many=False, read_only=True)
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
        Profile.objects.update(**profile_data)
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
