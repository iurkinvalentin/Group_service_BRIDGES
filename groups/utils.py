import requests
import logging

AUTH_SERVICE_URL = 'http://127.0.0.1:8000/api/verify-token/'


def get_user_info(token):
    """Отправка токена в auth_service для валидации"""
    headers = {'Authorization': f'Bearer {token}'}
    try:
        # Отправляем POST-запрос в auth_service
        response = requests.post(AUTH_SERVICE_URL, headers=headers, data={'token': token})
        logging.info(f"Отправка запроса в auth_service с токеном: {token}")
        logging.info(f"Статус ответа от auth_service: {response.status_code}")

        # Проверяем, успешен ли ответ
        if response.status_code == 200:
            logging.info("Токен валиден. Данные пользователя получены.")
            return response.json()  # Вернем данные пользователя, если токен валиден
        else:
            logging.error(f"Ошибка валидации токена. Ответ: {response.content}")
            return None
    except Exception as e:
        logging.error(f"Ошибка при отправке запроса в auth_service: {str(e)}")
        return None