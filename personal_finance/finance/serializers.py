from rest_framework import serializers

from .models import FinanceAccount


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceAccount
        fields = [
            'name',
            'type',
        ]

    def create(self, validated_data):
        user = self.context.get('user')
        validated_data['user'] = user
        return super().create(validated_data)