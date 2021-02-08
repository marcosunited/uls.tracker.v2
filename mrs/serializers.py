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


class AddressesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ('id',
                  'number',
                  'street',
                  'post_code',
                  'suburb',
                  'state')


class ContactsSerializer(serializers.ModelSerializer):
    title = MetadataValuesSerializer(many=False, read_only=True)
    position = MetadataValuesSerializer(many=False, read_only=True)
    address = AddressesSerializer(many=False)

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

    def create(self, validated_data):
        title_data = validated_data.pop('title')
        position_data = validated_data.pop('position')
        title = MetadataValue.objects.get(id=title_data['id'])
        position = MetadataValue.objects.get(id=position_data['id'])

        address_data = validated_data.pop('address')
        address = Address.objects.create(**address_data)

        contact = Contact.objects.create(title=title,
                                         position=position,
                                         address=address, **validated_data)
        return contact

    def update(self, instance, validated_data):
        if "title" in validated_data:
            title_id = validated_data.pop('title')
            title = MetadataValue.objects.get(id=title_id)
            instance.title = title
        if "position" in validated_data:
            position_id = validated_data.pop('position')
            position = MetadataValue.objects.get(id=position_id)
            instance.position = position
        if "address" in validated_data:
            address_data = validated_data.pop('address')
            Address.objects.filter(id=instance.address.id).update(**address_data)
        if "first_name" in validated_data:
            instance.first_name = validated_data.get('first_name', instance.first_name)
        if "last_name" in validated_data:
            instance.last_name = validated_data.get('last_name', instance.first_name)
        if "phone_number" in validated_data:
            instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        if "mobile_number" in validated_data:
            instance.mobile_number = validated_data.get('mobile_number', instance.mobile_number)
        if "email" in validated_data:
            instance.email = validated_data.get('email', instance.email)

        instance.save()

        return Contact.objects.get(id=instance.id)


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
        if "contact" in validated_data:
            contact_data = self.initial_data.pop('contact')
            contact = Contact.objects.get(id=instance.contact.id)
            contact_serializer = ContactsSerializer()
            contact_serializer.update(contact, contact_data)
        if "name" in validated_data:
            instance.name = validated_data.get('name', instance.name)
        if "is_active" in validated_data:
            instance.is_active = validated_data.get('is_active', instance.is_active)
        if "start_datetime" in validated_data:
            instance.start_datetime = validated_data.get('start_datetime', instance.start_datetime)
        if "end_datetime" in validated_data:
            instance.end_datetime = validated_data.get('end_datetime', instance.end_datetime)
        if "stand_by_datetime" in validated_data:
            instance.stand_by_datetime = validated_data.get('stand_by_datetime', instance.stand_by_datetime)
        if "reactive_datetime" in validated_data:
            instance.reactive_datetime = validated_data.get('reactive_datetime', instance.reactive_datetime)
        if "cancel_datetime" in validated_data:
            instance.cancel_datetime = validated_data.get('cancel_datetime', instance.cancel_datetime)
        if "price" in validated_data:
            instance.price = validated_data.get('price', instance.price)
        if "notes" in validated_data:
            instance.notes = validated_data.get('notes', instance.notes)
        if "status" in validated_data:
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
        contact_data = self.initial_data.pop('contact')
        validated_data.pop('contact')
        contact_serializer = ContactsSerializer()
        contact = contact_serializer.create(contact_data)
        agent = Agent.objects.create(contact=contact, **validated_data)
        return agent

    def update(self, instance, validated_data):
        if "contact" in validated_data:
            contact_data = self.initial_data.pop('contact')
            contact = Contact.objects.get(id=instance.contact.id)
            contact_serializer = ContactsSerializer()
            contact_serializer.update(contact, contact_data)
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
                  'un_code',)


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


class TaskTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTemplate
        fields = ('id',
                  'name',
                  'description',
                  'enabled',
                  'project')


class MaintenanceMonthSerializer(serializers.ModelSerializer):
    tasks_templates = TaskTemplateSerializer(many=True)

    class Meta:
        model = MaintenanceMonth
        fields = ('id',
                  'name',
                  'month_number',
                  'task_templates',
                  'project')


class YearMaintenanceTemplateSerializer(serializers.ModelSerializer):
    jan = MaintenanceMonthSerializer(many=False)
    feb = MaintenanceMonthSerializer(many=False)
    mar = MaintenanceMonthSerializer(many=False)
    apr = MaintenanceMonthSerializer(many=False)
    may = MaintenanceMonthSerializer(many=False)
    jun = MaintenanceMonthSerializer(many=False)
    jul = MaintenanceMonthSerializer(many=False)
    aug = MaintenanceMonthSerializer(many=False)
    sep = MaintenanceMonthSerializer(many=False)
    oct = MaintenanceMonthSerializer(many=False)
    nov = MaintenanceMonthSerializer(many=False)
    dec = MaintenanceMonthSerializer(many=False)

    class Meta:
        model = YearMaintenanceTemplate
        fields = ('id',
                  'name',
                  'jan',
                  'feb',
                  'mar',
                  'apr',
                  'may',
                  'jun',
                  'jul',
                  'aug',
                  'sep',
                  'oct',
                  'nov',
                  'dec',
                  'enabled',
                  'project')


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fault
        fields = ('id',
                  'name',
                  'description')


class MaintenancePlansSerializer(serializers.ModelSerializer):
    lift = PrimaryKeyRelatedField(many=False, queryset=Lift.objects.all())

    class Meta:
        model = MaintenancePlan
        fields = ('id',
                  'name')


class WorkordersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workorder
        fields = '__all__'


class WorkordersSerializer(serializers.ModelSerializer):
    technician = TechniciansSerializer(many=False, read_only=True)

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
