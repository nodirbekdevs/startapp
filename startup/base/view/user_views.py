from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from ..serializers import UserSerializer, UserSerializerWithToken, UserLoginSerializer


class UserLoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_users(request):
    try:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    except:
        message = {'detail': 'Users do not exists'}
        return Response(message, status=HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_user(request, pk):
    try:
        user = User.objects.get(id=pk)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'User does not exists'}
        return Response(message, status=HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    try:
        user = request.user
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'User does not exists'}
        return Response(message, status=HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    try:
        user = request.user, data = request.data
        serializer = UserSerializerWithToken(user, many=False)
        user.first_name = data['name']
        user.username = data['username']
        user.email = data['email']
        if data['password'] != '':
            user.password = make_password(data['password'])
        user.save()
        return Response(serializer.data)
    except:
        message = {'detail': 'User does not updated'}
        return Response(message, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def make_user(request):
    data = request.data
    try:
        user = User.objects.create(
            first_name=data['name'],
            username=data['username'],
            email=data['email'],
            password=make_password(data['password'])
        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'User with this email already exists'}
        return Response(message, status=HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_user(request, pk):
    try:
        user = User.objects.get(id=pk)
        data = request.data
        user.first_name = data['name']
        user.username = data['username']
        user.email = data['email']
        user.is_staff = data['isAdmin']
        user.save()
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'User does not updated'}
        return Response(message, status=HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_user(request, pk):
    try:
        user = User.objects.get(id=pk)
        user.delete()
        return Response('User was deleted')
    except:
        message = {'detail': 'User does not deleted'}
        return Response(message, status=HTTP_400_BAD_REQUEST)