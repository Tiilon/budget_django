from user.serializers import UserSerializer
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import permissions,decorators
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
import jwt, datetime
from django.utils import timezone
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            email = request.data['email']
            contact = request.data['contact']
            password = request.data['password']
            password2 = request.data['password2']

            if password != password2:
                return Response({'error': 'Password do not match'})
            try:
                user = User.objects.get(contact=contact)
                if user:
                    return Response({'error': 'User with this contact already exists'})
            except User.DoesNotExist:
                user = User.objects.create(
                    first_name=first_name, 
                    last_name=last_name, 
                    email=email, 
                    contact=contact
                    )
                user.set_password(password)
                user.save()
           
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([JWTAuthentication])
def login(request):
    if request.method == 'POST':
        serializer = MyTokenObtainPairSerializer
        email = request.data.get('email')
        password = request.data.get('password')
        
        
        try:
            usr = authenticate(username=email, password=password)

            if usr is not None:
                login(request, usr)

            if usr is None:
                return Response({'error':'User not found'}, status=status.HTTP_400_BAD_REQUEST)
            
            if not usr.check_password(password):
                return Response({'error':'Wrong Password'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            pass
        
        payload ={
            'id': usr.id,
            "first_name": usr.first_name,
            "last_name": usr.last_name,
            'exp': datetime.datetime.now() + datetime.timedelta(minutes=60),
            'iat': timezone.now()
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {'jwt': token}

        return response

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
@decorators.permission_classes([permissions.AllowAny])
def blacklist_token_view(request):
    try:
        refresh_token = request.data['refresh_token']
        token = RefreshToken(refresh_token)
        token.blacklist()
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)