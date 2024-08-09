from vietcombank import VietCombank
import json
import requests
import json
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import sys
import traceback
from api_response import APIResponse


app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "World"}
class LoginDetails(BaseModel):
    username: str
    password: str
    account_number: str
    verify_type: str
@app.post('/login', tags=["login"])
def login_api(input: LoginDetails):
    try:
        vcb = VietCombank(input.username, input.password, input.account_number)
        response = vcb.doLogin(input.verify_type)
        return APIResponse.json_format(response)
    except Exception as e:
        response = str(e)
        print(traceback.format_exc())
        print(sys.exc_info()[2])
        return APIResponse.json_format(response)    
class ConfirmDetails(BaseModel):
    username: str
    password: str
    account_number: str
    otp: str
    verify_type: str
@app.post('/confirm', tags=["confirm"])
def confirm_api(input: ConfirmDetails):
    try:
        vcb = VietCombank(input.username, input.password, input.account_number)
        if input.verify_type == "smart_otp":
            response = vcb.submitOtpLogin(input.otp)
        elif input.verify_type == "sms_otp":
            response = vcb.submitOtpSMS(input.otp)
        return APIResponse.json_format(response)
    except Exception as e:
        response = str(e)
        print(traceback.format_exc())
        print(sys.exc_info()[2])
        return APIResponse.json_format(response)
@app.post('/balance', tags=["balance"])
def confirm_api(input: LoginDetails):
    try:
        vcb = VietCombank(input.username, input.password, input.account_number)
        response = vcb.get_balance()
        return APIResponse.json_format(response)
    except Exception as e:
        response = str(e)
        print(traceback.format_exc())
        print(sys.exc_info()[2])
        return APIResponse.json_format(response)
    
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
    try:
        vcb = VietCombank(input.username, input.password, input.account_number)
        response = vcb.getHistories(input.from_date, input.to_date, input.account_number, input.page,input.limit)
        return APIResponse.json_format(response)
    except Exception as e:
        response = str(e)
        print(traceback.format_exc())
        print(sys.exc_info()[2])
        return APIResponse.json_format(response)

if __name__ == "__main__":
    uvicorn.run(app ,host='0.0.0.0', port=3000)
    
    