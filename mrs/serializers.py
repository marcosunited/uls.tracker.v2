from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from mrs.models import *
from mrs.utils.filter import DynamicFieldsModelSerializer


class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id',
                  'name',
                  'is_active',
                  'description',
                  'key_name')


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id',
                  'title',
                  'position',
                  'first_name',
                  'last_name)',
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
        model = Job
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


class JobsSerializer(DynamicFieldsModelSerializer):
    contract = PrimaryKeyRelatedField(many=False, queryset=Contract.objects.all())
    contact = PrimaryKeyRelatedField(many=False, queryset=Contact.objects.all())
    project = PrimaryKeyRelatedField(many=False, queryset=Project.objects.all())
    agent = PrimaryKeyRelatedField(many=False, queryset=Agent.objects.all())
    round = PrimaryKeyRelatedField(many=False, queryset=Round.objects.all())

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
                  'service_type_id',
                  'lifts')


class TechniciansSerializer(serializers.ModelSerializer):
    profile = PrimaryKeyRelatedField(many=False, queryset=Profile.objects.all())

    class Meta:
        model = Technician
        fields = ('id',
                  'profile',
                  'notes')


class RoundsSerializer(serializers.ModelSerializer):
    technicians = TechniciansSerializer(read_only=True, many=True)

    class Meta:
        model = Round
        fields = ('id',
                  'name',
                  'is_active',
                  'colour',
                  'polygon',
                  'technicians')


class AgentsSerializer(serializers.ModelSerializer):
    contact = PrimaryKeyRelatedField(many=False, queryset=Contact.objects.all())

    class Meta:
        model = Agent
        fields = ('id',
                  'name',
                  'contact')


"""
SYSTEM SERIALIZERS
"""
