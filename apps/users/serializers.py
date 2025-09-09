from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.DateField(
        input_formats=['%d-%m-%Y'],
        error_messages={
            'invalid': 'Date of birth must be in format: DD-MM-YYYY'
        }
    )
    class Meta:
        model = Profile
        fields = ['id', 'user', 'full_name','username', 'profile_picture', 'date_of_birth', 'location', 'phone_number', 'bio']
        read_only_fields = ['id', 'user']
    
    def validate_username(self, value):
        """
        Validate that username contains only lowercase letters and no spaces
        """
        if not value.islower():
            raise serializers.ValidationError("Username must contain only lowercase letters.")
        
        if ' ' in value:
            raise serializers.ValidationError("Username cannot contain spaces.")
        
        
        if not value.isalnum():
            raise serializers.ValidationError("Username can only contain letters and numbers.")
        
        return value

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.username = validated_data.get('username', instance.username)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.username = validated_data.get('username', instance.username)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.location = validated_data.get('location', instance.location)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()
        return instance
        