from argparse import Action
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from grooveapi.models import GrooveUser
from django.contrib.auth.models import User
from rest_framework.decorators import action
import uuid
from django.core.files.base import ContentFile
import base64


class ProfileSerializer(serializers.ModelSerializer):
    """JSON serializer for profiles
    """

    class Meta:
        model = GrooveUser
        fields = ('id', 'user', 'address',
                  'phone_number', 'profile_image', 'bio')
        depth = 1


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',
                  'email', 'is_staff', 'is_active')


class ProfileView(ViewSet):
    """Groove Profiles list view"""

    def list(self, request):
        """Handle GET requests to get all profiles

        Returns:
            Response -- JSON serialized list of profiles
            """

        profiles = GrooveUser.objects.all()

        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Handle GET requests for single profile

        Returns: 
            Response -- JSON serialized profile"""
        try:
            profile = GrooveUser.objects.get(pk=pk)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)

        except GrooveUser.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk):
        """Handle PUT requests for a user
        
        Returns:
            Response -- Empty body with 204 status code
            """
    @action(methods=['PUT'], detail=True)
    def user_active(self, request, pk):
        user = User.objects.get(pk=pk) 
        user.is_active = not user.is_active
        user.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['PUT'], detail=True)
    def user_status(self, request, pk):
        user = User.objects.get(pk=pk) 
        user.is_staff = request.data["is_staff"] #whats in the fetch body
        user.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['PUT'], detail=True)
    def user_image(self, request, pk):
        user = GrooveUser.objects.get(pk=pk)
        format, imgstr = request.data["profile_image"].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{user.id}-{uuid.uuid4()}.{ext}')
        user.profile_image = data
        user.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
