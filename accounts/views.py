from .models import BearerAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from rest_framework import parsers, renderers
from .serializers import AuthTokenSerializer, RegisterSerializer, ChangePasswordSerializer
from rest_framework import generics

User = get_user_model()


# view to test authentication
class HelloView(APIView):
    """
        Returns a list of Categories available
    """
    authentication_classes = (BearerAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({'Hello': 'View'})


class RegisterView(APIView):
    """Register users"""
    permission_classes = [permissions.AllowAny, ]

    def post(self, request, format=None):
        data = self.request.data
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        password = data['password']
        password2 = data['password2']

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            if password == password2:
                if User.objects.filter(email=email).exists():
                    return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    if len(password) < 6:
                        return Response({'error': 'Password must be at least 6 characters in length'},
                                        status=status.HTTP_400_BAD_REQUEST)
                    elif email == '':
                        return Response({'error': 'Email field can not be empty'}, status=status.HTTP_400_BAD_REQUEST)
                    elif first_name == '':
                        return Response({'error': 'first_name field can not be empty'},
                                        status=status.HTTP_400_BAD_REQUEST)
                    elif last_name == '':
                        return Response({'error': 'last_name field can not be empty'},
                                        status=status.HTTP_400_BAD_REQUEST)
                    else:
                        user = User.objects.create_user(
                            email=email, password=password, first_name=first_name, last_name=last_name)
                        # could use this to create token during registration or using signals
                        # Token.objects.create(user=user).key
                        user.save()
                        return Response(serializer.data,
                                        status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        # token = Token.objects.get(user=user)
        # in case need to create token during logging in
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {'token': token.key,
             'email': user.email,
             'first_name': user.first_name,
             'last_name': user.last_name})


class LogOut(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response({'logout': 'User Logged out successfully'})


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BearerAuthentication,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = self.request.data
        old_password = data['old_password']
        new_password = data['new_password']
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # check password in database if it matches to password given by user
            if not self.object.check_password(old_password):
                return Response({'wrong password': 'Wrong Password. Did you forget your password'})
            else:
                # set_password will hash the password from the user
                self.object.set_password(new_password)
                self.object.save()
                return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)