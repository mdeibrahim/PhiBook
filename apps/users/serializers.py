from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'full_name', 'profile_picture', 'date_of_birth', 'location', 'phone_number', 'bio']
        read_only_fields = ['id', 'user']
    

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.location = validated_data.get('location', instance.location)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()
        return instance