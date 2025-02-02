from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserInfoSerializer, UserProfileSerializer
from django.contrib.auth import get_user_model

# 사용자 정보 조회 함수
User = get_user_model()
@api_view(['GET'])
def user_info(request):
    user = request.user
    if user:
        serializer = UserInfoSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_page(request):
    user = request.user
    if user.is_authenticated:
        # serializer = UserProfileSerializer(user)
        serializer = UserProfileSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)