from pydantic import BaseModel
from datetime import date


class SalaryResponse(BaseModel):
    salary: float
    next_promotion: date


class UserLogin(BaseModel):
    username: str
    password: str

class User(BaseModel):
    login_data: UserLogin
    salary_inf: SalaryResponse


class Settings(BaseModel):
    authjwt_secret_key: str = 'secret'
    authjwt_token_location: set = {'cookies'}
    authjwt_cookie_csrf_protect: bool = False