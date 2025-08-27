from rest_framework import serializers
from main.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        password = data['password']
        confirm_password = data['confirm_password']

        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError('Passwords are do not match!')
        data.pop('confirm_password')

        return data