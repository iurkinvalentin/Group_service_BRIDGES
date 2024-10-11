import requests
import logging
logger = logging.getLogger('my_logger')

AUTH_SERVICE_URL = 'http://127.0.0.1:8000/api/verify-token/'


def get_user_info(token):
    """Отправка токена в auth_service для валидации"""
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(AUTH_SERVICE_URL, headers=headers, data={'token': token})
    if response.status_code == 200:
        return response.json()  # Вернем данные пользователя
    else:
        return None