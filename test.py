from vietcombank import VietCombank
import json

vcb = VietCombank('0969838595', 'Line688688@', '9969838595')

#OTP is required first login only, then youn can call action without it after login
get_otp = vcb.doLogin()
verify_type = vcb.verify_type
print(get_otp)
if "data" in get_otp and 'mid' in get_otp["data"] and get_otp["data"]['mid']== '3010':
    if verify_type == "5":
        otp = input("challenge_CODE:"+get_otp["data"]['challenge']+" | Enter SMART OTP: ")
        verify_otp = vcb.submitOtpLogin(otp)
    else:
        otp = input("Enter SMS OTP:")
        verify_otp = vcb.submitOtpSMS(otp)
        print(verify_otp)
        if "success" in verify_otp and verify_otp["success"] == True and 'session' in verify_otp:
            print('ACTIVE SUCCESSFULL')
        else:
            print(f"OTP verification failed: {verify_otp['des']}")
        
# OTP is required first login only, then youn can call action without it after login
# import time
# st = time.time()
# while True:
#     result = vcb.get_balance()
#     print((result))
#     time.sleep(5)
#     print(time.time()-st)
result = vcb.get_balance()
print((result))
result = vcb.getHistories("15/01/2024", "15/01/2024", '9969838595', 0)
print((result))
# account_number="0621000456871"
# amount="50000"
# message="123"
# result = vcb.createTranferInVietCombank(account_number, amount, message)
# print((result))