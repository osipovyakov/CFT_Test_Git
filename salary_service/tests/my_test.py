import pytest
import requests
from fastapi.testclient import TestClient
from fastapi import HTTPException, status
from unittest.mock import MagicMock
from salary_service.routes.routes import api_router


@pytest.fixture
def client():
    return TestClient(api_router)


@pytest.fixture(scope='session')
def access_token():
    user_data = {
        'username': 'user_1',
        'password': 'password_1'
    }
    response = requests.post('http://127.0.0.1:8000/token', json=user_data)
    access_token = response.cookies.get('access_token_cookie')
    print (access_token)
    return access_token


@pytest.mark.asyncio
async def test_login_endpoint(client):
    user_data = {
        'username': 'user_1',
        'password': 'password_1'
    }

    response = client.post('/token', json=user_data)
    assert response.status_code == 200
    assert 'Токен успешно создан' in response.json()


@pytest.mark.asyncio
async def test_invalid_password_login():
    from salary_service.utiles.verification_util import user_verification
    from salary_service.models.models import UserLogin
    from salary_service.db import USERS


    user = UserLogin(username='user_1', password='wrong_password')
    with pytest.raises(HTTPException) as exc_info:
        USERS = MagicMock()
        user_verification(user)
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == 'Неверное имя пользователя или пароль'


@pytest.mark.asyncio
async def test_invalid_username_login():
    from salary_service.utiles.verification_util import user_verification
    from salary_service.models.models import UserLogin
    from salary_service.db import USERS

    user = UserLogin(username='wrong_user', password='password_1')
    with pytest.raises(HTTPException) as exc_info:
        USERS = MagicMock()
        user_verification(user)
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == 'Неверное имя пользователя или пароль'


@pytest.mark.asyncio
async def test_authenticated_endpoint(access_token):
    cookies = {'access_token_cookie': access_token}
    response = requests.get('http://127.0.0.1:8000/salary', cookies=cookies)
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) == 2
    user, salary_info = response_data
    assert isinstance(user, str)
    assert isinstance(salary_info, dict)
    assert user == 'user_1'
    assert salary_info == {'next_promotion': '2024-10-01', 'salary': 100}


@pytest.mark.asyncio
async def test_get_salary_without_token():
    response = requests.get('http://127.0.0.1:8000/salary')
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


@pytest.mark.asyncio
async def test_get_salary_with_invalid_token():
    cookies = {'access_token_cookie': 'invalid_token'}
    response = requests.get('http://127.0.0.1:8000/salary', cookies=cookies)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
