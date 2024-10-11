import requests
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings

def check_user_existence_in_auth_service(user_id, access_token):
    """Проверка существования пользователя в auth_service через запрос с передачей токена."""
    url = f'http://127.0.0.1:8000/api/profile/{user_id}/'  # URL для запроса к auth_service
    headers = {
        'Authorization': f'Bearer {access_token}',  # Передаем токен в заголовке
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(url, headers=headers)  # Передаем заголовок с токеном
        if response.status_code == 200:
            user_data = response.json()
            print(f"Пользователь найден: {user_data['user']}, {user_data['bio']}")
            return True
        elif response.status_code == 404:
            print(f"Пользователь с ID {user_id} не найден.")
            return False
        else:
            print(f"Ошибка при запросе: {response.status_code}, {response.text}")
            return False
    except requests.RequestException as e:
        print(f"Ошибка запроса к auth_service: {e}")
        return False

class AuthMiddleware(MiddlewareMixin):
    """Middleware для проверки аутентификации через JWT токен"""
    
    def process_request(self, request):
        jwt_authenticator = JWTAuthentication()
        try:
            # Аутентифицируем пользователя через JWTAuthentication
            user, token = jwt_authenticator.authenticate(request)
            
            if user:
                # Проверяем пользователя через auth_service
                user_id = token['user_id']
                if check_user_existence_in_auth_service(user_id, token):
                    print(f"Пользователь успешно аутентифицирован: {user}")
                    request.user_info = user
                else:
                    request.user_info = None
                    print(f"Пользователь с ID {user_id} не найден.")
            else:
                request.user_info = None
        except Exception as e:
            print(f"Ошибка аутентификации: {e}")
            request.user_info = None
