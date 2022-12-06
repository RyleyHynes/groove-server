from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from grooveapi.models import GrooveUser


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    '''Handles the authentication of a user

    Method arguments:
      request -- The full HTTP request object
    '''
    username = request.data['username']
    password = request.data['password']
    

    authenticated_user = authenticate(username=username, password=password)

    if authenticated_user is not None:
        token = Token.objects.get(user=authenticated_user)
        # Returning information to client
        data = {
            'valid': True,
            'token': token.key,
            'user_id': authenticated_user.id,
            'is_staff': authenticated_user.is_staff
        }
        return Response(data)
    else:
        data = { 'valid': False }
        return Response(data)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    '''Handles the creation of a new groove user for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    # Creating a new user
    new_user = User.objects.create_user(
        username=request.data['username'],
        password=request.data['password'],
        first_name=request.data['first_name'],
        last_name=request.data['last_name'],
        email=request.data['email']
    )

    # using a model with a 1 to 1 relationship to the django user to created an object
    groove_user = GrooveUser.objects.create(
        bio=request.data['bio'],
        user=new_user
    )
    
    token = Token.objects.create(user=groove_user.user)
    
    # List of information to send to the client
    data = { 'token': token.key, 'user_id': new_user.id, 'is_staff': new_user.is_staff, "valid": True }
    return Response(data, status=status.HTTP_201_CREATED)