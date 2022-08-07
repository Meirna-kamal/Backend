from rest_framework import permissions
from rest_framework.permissions import AllowAny  # <-- Here
from .serializers import LoginUserSerializer
from django.contrib.auth import login
from rest_auth.views import LoginView as RestLoginView

class Login(RestLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super().post(request, format=None)