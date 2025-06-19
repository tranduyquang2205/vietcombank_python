from vietcombank import VCB
import json

vcb = VCB('0886438795', 'Dqxkv2205.,!', '0621000456871')

#OTP is required first login only, then youn can call action without it after login
result = vcb.login()
print((result))

ben_account_number="024042205"
account_name = "Tran Duy Quang"
amount="10000"
message="123"
bank_code = "MB"
result = vcb.transferBank(bank_code, ben_account_number, amount, message,account_name)
print((result))