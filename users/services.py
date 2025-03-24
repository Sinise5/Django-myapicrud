from django.contrib.auth import get_user_model, authenticate  # Pastikan authenticate diimpor
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserService:
    @staticmethod
    def create_user(username, email, password):
        return User.objects.create_user(username=username, email=email, password=password)

    @staticmethod
    def authenticate_user(username, password):
        user = authenticate(username=username, password=password)  # Gunakan authenticate()
        if user and user.is_active:  # Pastikan user aktif
            refresh = RefreshToken.for_user(user)
            return {
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                },
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        return None
