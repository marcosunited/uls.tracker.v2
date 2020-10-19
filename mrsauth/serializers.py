from rest_framework import serializers

from mrsauth.models import User


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id',
                  'firstName',
                  'lastName',
                  'nick_name',
                  'salt',
                  'statusId',
                  'createdDate',
                  'updatedDate',
                  'password',
                  'date_of_birth')

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
