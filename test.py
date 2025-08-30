from vietcombank import VCB
import json

vcb = VCB('0886438795', 'Dqxkv2205.,!@', '0621000456871')

#OTP is required first login only, then youn can call action without it after login
result = vcb.login()
print((result))
result = vcb.get_balance()
print((result))
# OTP is required first login only, then youn can call action without it after login
# import time
# st = time.time()
# while True:
#     result = vcb.get_balance()
#     print((result))
#     time.sleep(5)
#     print(time.time()-st)
# result = vcb.get_balance()
# print((result))
result = vcb.getHistories("15/01/2024", "15/01/2024", '0621000456871', 0)
print((result))
# account_number="024042205"
# amount="50000"
# message="123"
# bank_code = "970422"
# result = vcb.transfer_money(bank_code, account_number, amount, message)
# print((result))