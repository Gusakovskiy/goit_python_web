import hashlib

from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        ]

    id = serializers.IntegerField(read_only=True, required=False)
    username = serializers.CharField(read_only=True, required=False)

    def validate(self, attrs):
        validate_data = super().validate(attrs)
        if 'username' not in validate_data:
            validate_data['username'] = self.generate_user_name(
                validate_data['first_name'],
                validate_data['last_name'],
            )
        return validate_data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user: User = super().create(validated_data)
        user.set_password(password)
        user.save(update_fields=['password'])
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user: User = super().update(instance, validated_data)
        if password is not None:
            user.set_password(password)
            user.save(update_fields=['password'])
        return user

    @staticmethod
    def generate_user_name(first_name, last_name):
        return f'{first_name}_{last_name}'.lower()
