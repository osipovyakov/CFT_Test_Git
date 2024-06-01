from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from salary_service.utiles.verification_util import user_verification
from salary_service.models.models import UserLogin, Settings
from datetime import timedelta
from salary_service.db import USERS

api_router = APIRouter()
TOKEN_LIFETIME = 3600


@AuthJWT.load_config
def get_config():
    return Settings()


@api_router.post('/token')
async def login(user: UserLogin, Authorize: AuthJWT = Depends()):
    username = user_verification(user)
    token_lifetime = timedelta(seconds=TOKEN_LIFETIME)
    access_token = Authorize.create_access_token(subject=username, expires_time = token_lifetime)
    Authorize.set_access_cookies(access_token)
    return {'Токен успешно создан'}



@api_router.get('/salary')
async def get_salary(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    user = Authorize.get_jwt_subject()
    return user, USERS[user].salary_inf