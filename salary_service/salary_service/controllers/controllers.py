from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi_jwt_auth import AuthJWT
#from exchange_api.auth.jwt_handler import JWT_ALGORITHM, JWT_SECRET
from salary_service.main import user_verification
from salary_service.models.models import User, Token, SalaryResponse, Settings
from datetime import datetime, timedelta


app = FastAPI(
    title='Get a salary'
)

USERS = {
    'user_1' : User(username='user_1', password='password_1', salary_inf=SalaryResponse(salary=100, next_promotion="2024-10-01")),
    'user_2' : User(username='user_2', password='password_2', salary_inf=SalaryResponse(salary=200, next_promotion="2024-11-11")),
    'user_3' : User(username='user_3', password='password_3', salary_inf=SalaryResponse(salary=150, next_promotion="2024-08-28"))
}


TOKEN_LIFETIME = 3600

@AuthJWT.load_config
def get_config():
    return Settings()

@app.post('/token')
async def login(user: User, Authorize: AuthJWT = Depends()):
    username = user_verification(user)
    token_lifetime = timedelta(seconds=TOKEN_LIFETIME)
    access_token = Authorize.create_access_token(subject=username, expires_time = token_lifetime)
    Authorize.set_access_cookies(access_token)
    return {'msg': 'access_token created'}



@app.get('/salary')
async def get_salary(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    username = Authorize.get_jwt_subject()
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неправильный токен'
        )
    user = USERS.get(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователя нет в базе'
        )
    return user.username, user.salary_inf
