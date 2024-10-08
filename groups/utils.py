import requests


AUTH_SERVICE_URL = "http://127.0.0.1:8000/api/profile/"


def get_user_info(user_id):
    """
    Получает информацию о пользователе из auth_service по его user_id.
    Возвращает JSON с данными пользователя или None в случае ошибки.
    """
    try:
        response = requests.get(f"{AUTH_SERVICE_URL}{user_id}/")
        if response.status_code == 200:
            return response.json()  # Возвращаем данные о пользователе
        return None  # Если пользователь не найден или возникла ошибка
    except requests.RequestException:
        return None
