from vietcombank import VietCombank
import json

vcb = VietCombank('0326533531', 'Anhtam456#', '3326533531')

#OTP is required first login only, then youn can call action without it after login
get_otp = vcb.doLogin()
print(get_otp)
if "data" in get_otp and 'mid' in get_otp["data"] and get_otp["data"]['mid']== '3010':
        otp = input("challenge_CODE:"+get_otp["data"]['challenge']+" | Enter SMART OTP: ")
        verify_otp = vcb.submitOtpLogin(otp)
        print(verify_otp)
        if "success" in verify_otp and verify_otp["success"] == True and 'd' in verify_otp:
            print('ACTIVE SUCCESSFULL')
        else:
            print(f"OTP verification failed: {verify_otp['des']}")
        
# OTP is required first login only, then youn can call action without it after login
result = vcb.getHistories("15/01/2024", "15/01/2024", '3326533531', 0)
print((result))
# account_number="0621000456871"
# amount="50000"
# message="123"
# result = vcb.createTranferInVietCombank(account_number, amount, message)
# print((result))