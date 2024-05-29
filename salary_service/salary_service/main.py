from fastapi import FastAPI
from .routes import routes


app = FastAPI(title='Get a salary')
app.include_router(routes.api_router)