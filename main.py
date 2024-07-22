from fastapi import FastAPI, APIRouter
from src.controller.transactionController import app_router
from src.controller.accountController import account_router

app = FastAPI()
router = APIRouter()

app.include_router(app_router)
app.include_router(account_router)