from fastapi import HTTPException, status
from salary_service.models.models import UserLogin
from salary_service.db import USERS


def user_verification(user: UserLogin):
    username = user.username
    password = user.password
    if username not in USERS or USERS[username].login_data.password != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверное имя пользователя или пароль'
        )
    return username
