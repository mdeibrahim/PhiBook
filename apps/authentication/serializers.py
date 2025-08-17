from rest_framework import serializers
from apps.users.models import CustomUser
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # Step 1: Check if user exists
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        # Step 2: Check password
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid password.")

        # Step 3: Check if active
        if not user.is_active:
            raise serializers.ValidationError("Account not active. Please verify your email.")

        # Step 4: Authenticate (for DRF tokens or sessions)
        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Unable to authenticate user.")

        return user