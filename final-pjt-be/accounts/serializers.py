from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .utils import get_user_profile_image

User = get_user_model()

class UserInfoSerializer(serializers.ModelSerializer):
    userprofile = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id','username','userprofile']
    
    def get_user(self, obj):
        return obj.user.username
    
    def get_userprofile(self, obj):
        if hasattr(obj, 'profile') and obj.profile.image:
            return obj.profile.image.url
        return None