from fastapi import FastAPI, Depends, HTTPException, status
#from fastapi_login import LoginManager
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from datetime import datetime, timedelta
import jwt
from .models.models import User, Token, SalaryResponse

USERS = {
    'user_1' : User(id=0, username='user_1', password='password_1', salary_inf=SalaryResponse(salary=100, next_promotion="2024-10-01")),
    'user_2' : User(id=1, username='user_2', password='password_2', salary_inf=SalaryResponse(salary=200, next_promotion="2024-11-11")),
    'user_3' : User(id=2, username='user_3', password='password_3', salary_inf=SalaryResponse(salary=150, next_promotion="2024-08-28"))
}

TOKEN_LIFETIME = 3600
SECRET_KEY = 'SECRET_KEY'
algorithm = 'HS256'
#security = HTTPBasic()
#manager = LoginManager(SECRET_KEY, token_url='/token')

'''
@manager.user_loader()
def load_user(username: str):
    user = {'username', 'password'}
    return user
'''


def user_verification(user: User):
    username = user.username
    password = user.password
    if username not in USERS or USERS[username].password != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверное имя пользователя или пароль'
        )
    return username

'''
def generate_token(username: str):
    token_lifetime = datetime.now() + timedelta(seconds=TOKEN_LIFETIME)
    payload = {'sub': username, 'exp': token_lifetime}
    token = jwt.encode(payload, SECRET_KEY, algorithm)
    return token


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[algorithm])
        username = payload['sub']
        return username
    except jwt.ExpiredSignatureError:
        return 'Срок действия токена истек'
    except jwt.InvalidTokenError:
        return 'Некорректный токен'
'''