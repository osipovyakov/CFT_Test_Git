from pydantic import BaseModel
from datetime import date

class Token(BaseModel):
    token: str


class SalaryResponse(BaseModel):
    salary: float
    next_promotion: date


class User(BaseModel):
    username: str
    password: str
    salary_inf: SalaryResponse


class Settings(BaseModel):
    authjwt_secret_key: str = 'secret'
    authjwt_token_location: set = {'cookies'}
    authjwt_cookie_csrf_protect: bool = False