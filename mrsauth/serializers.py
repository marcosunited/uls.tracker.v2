from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from mrs.models import Profile
from mrsauth.models import User


class PermissionsSerializer(serializers.ModelSerializer):
    content_type = PrimaryKeyRelatedField(many=False, queryset=ContentType.objects.all())

    class Meta:
        model = Permission
        fields = ('id',
                  'name',
                  'content_type',
                  'codename')


class GroupsSerializer(serializers.ModelSerializer):
    permissions = PrimaryKeyRelatedField(many=True, queryset=Permission.objects.all())

    class Meta:
        model = Group
        fields = ('id',
                  'name',
                  'permissions')


class ProfilesSerializer(serializers.ModelSerializer):
    user = PrimaryKeyRelatedField(many=False, queryset=User.objects.all())

    class Meta:
        model = Profile
        fields = ('id',
                  'fullname',
                  'phone',
                  'email',
                  'user')


class UsersSerializer(serializers.ModelSerializer):
    profiles = ProfilesSerializer(many=True, read_only=True)
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
                  'profiles',
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
