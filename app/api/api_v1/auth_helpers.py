from datetime import datetime, timedelta
import os
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
import hmac
import hashlib

from pydantic import BaseModel

# Переменные окружения для логина и пароля
ADMIN_LOGIN = os.getenv('ADMIN_LOGIN')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
SECRET_KEY = os.getenv('SECRET_KEY')

# Контекст для хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Создание и проверка хэша пароля
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# Создание хэша для куки
def create_hashed_cookie(login: str, secret_key: str):
    return hmac.new(secret_key.encode(), login.encode(), hashlib.sha256).hexdigest()

# Проверка хэша куки
def verify_hashed_cookie(cookie_value: str, login: str, secret_key: str):
    return hmac.compare_digest(cookie_value, create_hashed_cookie(login, secret_key))

# Класс для авторизационных данных
class LoginData(BaseModel):
    username: str
    password: str