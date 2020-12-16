from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from mrs.models import Profile
from mrs.serializers import ProfilesSerializer
from mrsauth.models import User


class PermissionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ('id',
                  'name')


class GroupsSerializer(serializers.ModelSerializer):
    permissions = PermissionsSerializer(many=True)

    class Meta:
        model = Group
        fields = ('id',
                  'name',
                  'permissions')


class UsersSerializer(serializers.ModelSerializer):
    profile = ProfilesSerializer(many=False, read_only=True)
    groups = GroupsSerializer(many=True, read_only=True)

    class Meta:
        fields = ('id',
                  'firstName',
                  'lastName',
                  'nick_name',
                  'salt',
                  'statusId',
                  'createdDate',
                  'updatedDate',
                  'password',
                  'date_of_birth',
                  'profile',
                  'groups')

        model = User
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('auth_token',)

    def create(self, validated_data):
        try:
            user = super(UsersSerializer, self).create(validated_data)
            user.set_password(validated_data['password'])
            user.save()
        except KeyError:
            pass
        return user

    def update(self, instance, validated_data):
        user = super(UsersSerializer, self).update(instance, validated_data)
        try:
            user.set_password(validated_data['password'])
            user.save()
        except KeyError:
            pass
        return user
