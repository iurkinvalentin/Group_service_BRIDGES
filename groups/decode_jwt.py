import jwt
import datetime
import requests

def decode_jwt_token(token):
    """Функция для декодирования токена и проверки времени истечения."""
    try:
        # Декодируем токен без проверки подписи, чтобы посмотреть содержимое
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        print("Декодированный токен:", decoded_token)
        return decoded_token
    except jwt.ExpiredSignatureError:
        print("Токен истек")
    except jwt.InvalidTokenError:
        print("Неверный токен")

def verify_jwt_token(token, secret_key):
    """Функция для верификации токена с проверкой подписи."""
    try:
        # Декодируем токен с проверкой подписи
        decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        print("Верифицированный токен:", decoded_token)
        return decoded_token
    except jwt.ExpiredSignatureError:
        print("Токен истек")
    except jwt.InvalidTokenError:
        print("Неверный токен")

def check_token_expiration(exp_timestamp):
    """Проверка, истек ли токен."""
    exp_time = datetime.datetime.utcfromtimestamp(exp_timestamp)
    current_time = datetime.datetime.utcnow()
    
    print(f"Время истечения токена: {exp_time}")
    print(f"Текущее время: {current_time}")
    
    if current_time > exp_time:
        print("Токен уже истек.")
        return False
    else:
        print("Токен еще действителен.")
        return True

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

# Пример использования
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI4NjUwOTU1LCJpYXQiOjE3Mjg2NDkxNTUsImp0aSI6ImM2M2Q4NmI3ZDEwNjRmYzdiODVkYWExOWFiNzM2YTJkIiwidXNlcl9pZCI6MX0.66_smrGBp-e-VMl9EuBpB7okIISgXS0Bk2GCTaKk_LU"
secret_key = "django-insecure-yhkditmuf(g-py^yqfx0ryfo!3ld36(+a*+2a(0z005l*n01tz"

# 1. Декодируем токен и получаем его содержимое
decoded_token = decode_jwt_token(access_token)

if decoded_token:
    # 2. Верифицируем токен с проверкой подписи
    verified_token = verify_jwt_token(access_token, secret_key)
    
    if verified_token:
        # 3. Проверяем, истек ли токен
        exp_timestamp = decoded_token.get("exp")
        if exp_timestamp and check_token_expiration(exp_timestamp):
            # 4. Проверяем, существует ли пользователь с user_id через auth_service
            user_id = decoded_token.get("user_id")
            if user_id and check_user_existence_in_auth_service(user_id, access_token):
                print("Все проверки пройдены успешно!")
            else:
                print("Пользователь не найден.")
        else:
            print("Токен истек.")
    else:
        print("Ошибка при верификации токена.")
else:
    print("Невозможно декодировать токен.")
