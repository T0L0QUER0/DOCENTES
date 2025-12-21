# mi_app/backends.py

from django.contrib.auth.backends import BaseBackend
from .models import Division

class DivisionBackend(BaseBackend):
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None
        try:
            user = Division.objects.get(correo_administrador=username)
        except Division.DoesNotExist:
            return None
        
        if user.check_password(password):
            return user
        return None 

    def get_user(self, user_id):
        try:
            return Division.objects.get(pk=user_id)
        except Division.DoesNotExist:
            return None