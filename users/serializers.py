# 9. Buat serializers untuk autentikasi di users/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .services import UserService

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return UserService.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user_data = UserService.authenticate_user(data['username'], data['password'])  # Pastikan indentasi benar
        if not user_data:
            raise serializers.ValidationError({"error": "Invalid username or password"})

        return user_data  # Pastikan return juga sejajar dengan blok di atasnya



        
