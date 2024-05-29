from salary_service.models.models import User, UserLogin, SalaryResponse

USERS = {
    'user_1' : User(login_data=UserLogin(username='user_1', password='password_1'), salary_inf=SalaryResponse(salary=100, next_promotion="2024-10-01")),
    'user_2' : User(login_data=UserLogin(username='user_2', password='password_2'), salary_inf=SalaryResponse(salary=200, next_promotion="2024-11-11")),
    'user_3' : User(login_data=UserLogin(username='user_3', password='password_3'), salary_inf=SalaryResponse(salary=150, next_promotion="2024-08-28"))
}