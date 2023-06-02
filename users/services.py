from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

def create_user(username, password, role):
    User = get_user_model()
    user = User.objects.create_user(username=username, password=password, role=role)
    return user

def get_user(user_id):
    User = get_user_model()
    return User.objects.get(id=user_id)

def authenticate_user(username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    else:
        return None
