from rest_framework import serializers
from .models import Post, Comment, Like
from apps.users.models import Profile, CustomUser

class UserSerializer(serializers.ModelSerializer):
    # Include all profile data
    full_name = serializers.CharField(source='profile.full_name', read_only=True)
    profile_picture = serializers.ImageField(source='profile.profile_picture', read_only=True)
    date_of_birth = serializers.DateField(source='profile.date_of_birth', read_only=True)
    location = serializers.CharField(source='profile.location', read_only=True)
    phone_number = serializers.CharField(source='profile.phone_number', read_only=True)
    bio = serializers.CharField(source='profile.bio', read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 
            'name', 
            'email', 
            'date_joined',
            'full_name', 
            'profile_picture', 
            'date_of_birth', 
            'location', 
            'phone_number', 
            'bio'
        ]

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'user', 'comment', 'created_at']
        

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    total_likes = serializers.IntegerField(read_only=True)  # No longer uses property
    total_comments = serializers.IntegerField(read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'user', 'text', 'image', 'image_url', 'video_url',
            'created_at', 'total_likes', 'total_comments', 'comments'
        ]

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            if request is not None:
                return request.build_absolute_uri(obj.image.url)
            else:
                return obj.image.url
        return None

    def get_video_url(self, obj):
        request = self.context.get('request')
        if obj.video_url:
            if request is not None:
                return request.build_absolute_uri(obj.video_url)
            else:
                return obj.video_url
        return None
