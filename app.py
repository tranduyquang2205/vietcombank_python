from vietcombank import VietCombank
import json
import requests
import json
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn


app = FastAPI()

class LoginDetails(BaseModel):
    username: str
    password: str
    account_number: str
@app.post('/login', tags=["login"])
def login_api(input: LoginDetails):
        vcb = VietCombank(input.username, input.password, input.account_number)
        get_otp = vcb.doLogin()
        return get_otp
    
class ConfirmDetails(BaseModel):
    username: str
    password: str
    account_number: str
    otp: str
@app.post('/confirm', tags=["confirm"])
def confirm_api(input: LoginDetails):
        vcb = VietCombank(input.username, input.password, input.account_number)
        verify_otp = vcb.submitOtpLogin(input.otp)
        return verify_otp

# @app.post('/get_balance', tags=["get_balance"])
# def get_balance_api(input: LoginDetails):
#         vcb = VietCombank(input.username, input.password, input.account_number)
#         verify_otp = vcb.submitOtpLogin(input.otp)
#         return verify_otp
    
class Transactions(BaseModel):
    username: str
    password: str
    account_number: str
    from_date: str
    to_date: str
    limit: int
    page: int
    
@app.post('/get_transactions', tags=["get_transactions"])
def get_transactions_api(input: Transactions):
        vcb = VietCombank(input.username, input.password, input.account_number)
        history = vcb.getHistories(input.from_date, input.to_date, input.account_number, input.page,input.limit)
        return history


if __name__ == "__main__":
    uvicorn.run(app ,host='0.0.0.0', port=3000)
    
    