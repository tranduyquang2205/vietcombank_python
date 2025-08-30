
import hashlib
import requests
import json
import base64
import random
import string
import base64
import json
import os
import time
import time, binascii
import unidecode
list_bank = []
import time
banks_mapping = None
with open('banks.json','r', encoding='utf-8') as f:
    banks_mapping = json.load(f)
def mapping_bank_code(bank_code):
    global banks_mapping
    for bank in banks_mapping['data']:
        if bank['code'] == bank_code:
            return {'shortName': bank['shortName'], 'displayNameVi': bank['name'], 'bank_code': bank['bin']}

    return None
with open('list_bank_vcb.json', 'r',encoding='utf-8') as json_file:
    list_bank = json.load(json_file)
class VCB:
    def __init__(self, username, password, account_number,proxy_list=None):
        self.is_login = False
        self.time_login = time.time()
        self.file = f"db/users/{username}.json"
        self.verify_type = '5'
        self.x_lim_id = self.generate_sha256(username)
        self.url = {
            "getCaptcha": "https://digiapp.vietcombank.com.vn/utility-service/v2/captcha/MASS/",
            "login": "https://digiapp.vietcombank.com.vn/authen-service/v1/login",
            "authen-service": "https://digiapp.vietcombank.com.vn/authen-service/v1/api-",
            "getHistories": "https://digiapp.vietcombank.com.vn/bank-service/v1/transaction-history",
            "tranferOut_1": "https://digiapp.vietcombank.com.vn/napas-service/v1/get-channel-transfer-intersea",
            "tranferOut_2": "https://digiapp.vietcombank.com.vn/napas-service/v2/init-fast-transfer-via-accountno",
            "genOtpOut": "https://digiapp.vietcombank.com.vn/napas-service/v1/transfer-gen-otp",
            "genOtpIn": "https://digiapp.vietcombank.com.vn/transfer-service/v1/transfer-gen-otp",
            "confirmTranferOut": "https://digiapp.vietcombank.com.vn/napas-service/v1/transfer-confirm-otp",
            "confirmTranferIn": "https://digiapp.vietcombank.com.vn/transfer-service/v1/transfer-confirm-otp",
            "tranferIn": "https://digiapp.vietcombank.com.vn/transfer-service/v2/init-internal-transfer",
            "getBanks": "https://digiapp.vietcombank.com.vn/utility-service/v1/get-banks",
            "getAccountDeltail": "https://digiapp.vietcombank.com.vn/bank-service/v1/get-account-detail",
            "getlistAccount": "https://digiapp.vietcombank.com.vn/bank-service/v2/get-list-account-via-cif",
            "getlistDDAccount": "https://digiapp.vietcombank.com.vn/bank-service/v1/get-list-ddaccount",
            "get_bank_name_in": "https://digiapp.vietcombank.com.vn/transfer-service/v1/get-bene-internal-cusname",
            "get_bank_name_out": "https://digiapp.vietcombank.com.vn/napas-service/v1/inquiry-holdername",
        }
        self.lang = 'vi'
        self._timeout = 60
        self.DT = "Windows"
        self.OV = "10"
        self.appVersion = ""
        self.PM = "Edge 135.0.0.0"
        self.checkAcctPkg = "1"
        self.captcha1st = ""
        self.challenge = ""
        self.proxy_list = proxy_list
        if self.proxy_list:
            self.proxy_info = random.choice(self.proxy_list)
            proxy_host, proxy_port, username_proxy, password_proxy = self.proxy_info.split(':')
            self.proxies = {
                'http': f'http://{username_proxy}:{password_proxy}@{proxy_host}:{proxy_port}',
                'https': f'http://{username_proxy}:{password_proxy}@{proxy_host}:{proxy_port}'
            }
        else:
            self.proxies = None

        if not os.path.exists(self.file):
            self.username = username
            self.password = password
            self.account_number = account_number
            self.sessionId = ""
            self.mobileId = ""
            self.clientId = ""
            self.cif = None
            self.res = ""
            self.browserToken = ""
            self.E = ""
            self.tranId = ""
            self.browserId = hashlib.md5(self.username.encode()).hexdigest()
            self.save_data()
            
        else:
            self.parse_data()
            self.username = username
            self.password = password
            self.account_number = account_number
    def generate_sha256(self,username):
        salt = "6q93-@u9"
        data = (username + salt).encode()  # Chuyển thành bytes
        return hashlib.sha256(data).hexdigest()
    def save_data(self):
        data = {
            'username': self.username,
            'password': self.password,
            'account_number': self.account_number,
            'sessionId': getattr(self, 'sessionId', ''),
            'mobileId': getattr(self, 'mobileId', ''),
            'clientId': self.clientId,
            'cif': getattr(self, 'cif', ''),
            'E': getattr(self, 'E', ''),
            'res': getattr(self, 'res', ''),
            'tranId': getattr(self, 'tranId', ''),
            'browserToken': getattr(self, 'browserToken', ''),
            'browserId': self.browserId,
            'verify_type': self.verify_type,
            'time_login': self.time_login,
            'is_login': self.is_login,
        }
        with open(self.file, 'w') as f:
            json.dump(data, f)

    def parse_data(self):
        with open(self.file, 'r') as f:
            data = json.load(f)
        self.username = data.get('username', '')
        self.password = data.get('password', '')
        self.account_number = data.get('account_number', '')
        self.sessionId = data.get('sessionId', '')
        self.mobileId = data.get('mobileId', '')
        self.clientId = data.get('clientId', '')
        self.token = data.get('token', '')
        self.accessToken = data.get('accessToken', '')
        self.authToken = data.get('authToken', '')
        self.cif = data.get('cif', '')
        self.res = data.get('res', '')
        self.tranId = data.get('tranId', '')
        self.browserToken = data.get('browserToken', '')
        self.browserId = data.get('browserId', '')
        self.E = data.get('E', '')
        self.verify_type = data.get("verify_type", "")
        self.time_login = data.get("time_login", "")
        self.is_login = data.get("is_login", "")
        
    def createTaskCaptcha(self, base64_img):
        url = 'http://103.72.96.214:8277/api/captcha/vietcombank'
        # url = 'https://captcha.pay2world.vip/vcb'
        print(base64_img)
        payload = json.dumps({
        "base64": base64_img
        })
        headers = {
        'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, data=payload)
        return response.text

    def solveCaptcha(self):
        captchaToken = ''.join(random.choices(string.ascii_uppercase + string.digits, k=30))
        url = self.url['getCaptcha'] + captchaToken
        response = requests.get(url)
        base64_captcha_img = base64.b64encode(response.content).decode('utf-8')
        task = self.createTaskCaptcha(base64_captcha_img)
        print('task',task)
        # captchaText = self.checkProgressCaptcha(json.loads(task)['taskId'])
        res_captcha = json.loads(task)
        captchaText =res_captcha['captcha'] if 'captcha' in  res_captcha else res_captcha['prediction']
        return {"status": True, "key": captchaToken, "captcha": captchaText}

    def encrypt_data(self, data):
        """
        https://vcbbiz1.pay2world.vip/vietcombank/encrypt_biz
        https://tcbbcp1.pay2world.vip/vietcombank/encrypt
        https://encrypt1.pay2world.vip/api.php?act=encrypt_viettin
        """
        
        url_1 = 'https://vcbbiz1.pay2world.vip/vietcombank/encrypt'
        url_3 = 'https://vcbbiz.pay2world.vip/vietcombank/encrypt'
        
        payload = json.dumps(data)
        headers = {
            'Content-Type': 'application/json',
        }
        
        for _url in [url_1, url_3]:
            try:
                response = requests.request("POST", _url, headers=headers, data=payload, timeout=10)
                if response.status_code in [404, 502]:
                    continue
                return json.loads(response.text)
            except:
                continue
        return {}
    
    def decrypt_data(self, cipher):
        """
        https://vcbbiz1.pay2world.vip/vietcombank/encrypt_biz
        https://tcbbcp1.pay2world.vip/vietcombank/encrypt
        https://encrypt1.pay2world.vip/api.php?act=encrypt_viettin
        """
        
        url_1 = 'https://vcbbiz1.pay2world.vip/vietcombank/decrypt'
        url_3 = 'https://vcbbiz.pay2world.vip/vietcombank/decrypt'
        
        payload = json.dumps(cipher)
        headers = {
            'Content-Type': 'application/json',
        }
        
        for _url in [url_1, url_3]:
            try:
                response = requests.request("POST", _url, headers=headers, data=payload, timeout=10)
                if response.status_code in [404, 502]:
                    continue
                return json.loads(response.text)
            except:
                continue
        return {}

    def curlPost(self, url, data):
        encryptedData = self.encrypt_data(data)
        # print(encryptedData)
        headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://vcbdigibank.vietcombank.com.vn',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://vcbdigibank.vietcombank.com.vn/',
        'sec-ch-ua': '"Chromium";v="135", "Not:A-Brand";v="8", "Microsoft Edge";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
        'x-channel': 'Web',
        'x-lim-id': self.x_lim_id,
        'x-request-id': str(int(time.time() * 1000)) + str(int(random.random() * 100)) + format(binascii.crc_hqx(b'some_input', 0), 'x'),
        }
        # print('proxy',self.proxies)
        response = requests.post(url, headers=headers, data=json.dumps(encryptedData),proxies=self.proxies)
        try:
            result = self.decrypt_data(response.json())
            if 'code' in result and result['code'] == '108':
                self.is_login = False
                self.save_data()
        except:
            result = response.text
        
        return result

    def checkBrowser(self, type='1'):
        param = {
            "DT": self.DT,
            "OV": self.OV,
            "PM": self.PM,
            "E": self.getE() or "",
            "browserId": self.browserId,
            "lang": self.lang,
            "mid": 3008,
            "cif": "",
            "clientId": "",
            "mobileId": "",
            "sessionId": "",
            "browserToken": self.browserToken,
            "user": self.username
        }
        result = self.curlPost(self.url['authen-service'] + "3008", param)
        print(result)
        if "tranId" in result["transaction"]:
            types = result["transaction"]['listMethods']
            if '5' in types:
                self.verify_type = '5'
                return self.chooseOtpType(result["transaction"]["tranId"], '5')
            else:
                self.verify_type = '1'
                return self.chooseOtpType(result["transaction"]["tranId"], '1')
        else:
            return {
                'code': 400,
                'success': True,
                'message': "checkBrowser failed",
                "param": param,
                'data': result or ""
            }

    def chooseOtpType(self, tranID, type='1'):
        param = {
            "DT": self.DT,
            "OV": self.OV,
            "PM": self.PM,
            "E": self.getE() or "",
            "browserId": self.browserId,
            "lang": self.lang,
            "appVersion": "",
            "mid": 3010,
            "cif": "",
            "clientId": "",
            "mobileId": "",
            "sessionId": "",
            "browserToken": self.browserToken,
            "tranId": tranID,
            "type": type,  # 1 la sms,5 la smart
            "user": self.username
        }
        result = self.curlPost(self.url['authen-service'] + "3010", param)
        if result["code"] == "00":
            self.tranId = tranID
            self.save_data()
            self.challenge = result.get("challenge", "")
            return {
                    'code': 200,
                    'success': True,
                    'message': 'Thành công',
                "result": {
                    "browserToken": self.browserToken,
                    "tranId": result.get("tranId", ""),
                    "challenge": result.get("challenge", "")
                },
                "param": param,
                'data': result or ""
            }
        else:
            return {
                'code': 400,
                'success': False,
                'message': result["des"],
                "param": param,
                'data': result or ""
            }

    def submitOtpLogin(self, otp):
        param = {
            "DT": self.DT,
            "OV": self.OV,
            "PM": self.PM,
            "E": self.getE() or "",
            "browserId": self.browserId,
            "lang": self.lang,
            "mid": 3011,
            "appVersion": "",
            "cif": "",
            "clientId": "",
            "mobileId": "",
            "sessionId": "",
            "browserToken": self.browserToken,
            "tranId": self.tranId,
            "otp": otp,
            "challenge": self.challenge,
            "user": self.username
        }
        result = self.curlPost(self.url['authen-service'] + "3011", param)
        if result["code"] == "00":
            self.sessionId = result["sessionId"]
            self.mobileId = result["userInfo"]["mobileId"]
            self.clientId = result["userInfo"]["clientId"]
            self.cif = result["userInfo"]["cif"]
            session = {"sessionId": self.sessionId, "mobileId": self.mobileId, "clientId": self.clientId, "cif": self.cif}
            self.res = result
            self.is_login = True
            self.time_login = time.time()
            self.save_data()
            if result["allowSave"]:
                sv = self.saveBrowser()
                if sv["code"] == "00":
                    return {
                        'code': 200,
                        'success': True,
                        'message': 'Thành công',
                        'saved_browser': True,
                        "d": sv,
                        'session': session,
                        'data': result or ""
                    }
                else:
                    return {
                        'code': 400,
                        'success': False,
                        'message': sv["des"],
                        "param": param,
                        'data': sv or ""
                    }
            else:
                return {
                        'code': 200,
                        'success': True,
                        'message': 'Thành công',
                        'saved_browser': False,
                        'session': session,
                        'data': result or ""
                    }
        else:
            return {
                'code': 500,
                'success': False,
                'message': result["des"],
                "param": param,
                'data': result or ""
            }
    def submitOtpSMS(self, otp):
        param = {
            "DT": self.DT,
            "OV": self.OV,
            "PM": self.PM,
            "E": self.getE() or "",
            "browserId": self.browserId,
            "lang": self.lang,
            "mid": 3011,
            "appVersion": "",
            "cif": "",
            "clientId": "",
            "mobileId": "",
            "sessionId": "",
            "browserToken": self.browserToken,
            "tranId": self.tranId,
            "otp": otp,
            "user": self.username
        }
        result = self.curlPost(self.url['authen-service'] + "3011", param)
        if result["code"] == "00":
            self.sessionId = result["sessionId"]
            self.mobileId = result["userInfo"]["mobileId"]
            self.clientId = result["userInfo"]["clientId"]
            self.cif = result["userInfo"]["cif"]
            session = {"sessionId": self.sessionId, "mobileId": self.mobileId, "clientId": self.clientId, "cif": self.cif}
            self.res = result
            self.is_login = True
            self.time_login = time.time()
            self.save_data()
            if result["allowSave"]:
                sv = self.saveBrowser()
                print('sv',sv)
                if sv["code"] == "00":
                    
                    return {
                        'code': 200,
                        'success': True,
                        'message': 'Thành công',
                        'saved_browser': True,
                        "d": sv,
                        'session': session,
                        'data': result or ""
                    }
                else:
                    return {
                        'code': 400,
                        'success': False,
                        'message': sv["des"],
                        "param": param,
                        'data': sv or ""
                    }
            else:
                return {
                        'code': 200,
                        'success': True,
                        'message': 'Thành công',
                        'saved_browser': False,
                        'session': session,
                        'data': result or ""
                    }
        else:
            return {
                'code': 500,
                'success': False,
                'message': result["des"],
                "param": param,
                'data': result or ""
            }
    def saveBrowser(self):
        param = {
            "DT": self.DT,
            "OV": self.OV,
            "PM": self.PM,
            "E": self.getE() or "",
            "browserId": self.browserId,
            "browserName": "Edge 135.0.0.0",
            "lang": self.lang,
            "mid": 3009,
            "cif": self.cif,
            "clientId": self.clientId,
            "mobileId": self.mobileId,
            "sessionId": self.sessionId,
            "user": self.username
        }
        result = self.curlPost(self.url['authen-service'] + "3009", param)
        return result

    def doLogin(self):
        solveCaptcha = self.solveCaptcha()
        if not solveCaptcha["status"]:
            return solveCaptcha
        param = {
            "DT": self.DT,
            "OV": self.OV,
            "PM": self.PM,
            "E": None,
            "appVersion": self.appVersion,
            
            "browserId": self.browserId,
            "captchaToken": solveCaptcha["key"],
            "captchaValue": solveCaptcha["captcha"],
            
            "cif": self.cif,
            # "clientId": self.clientId,
            
            # "mobileId": self.mobileId,
            "lang": self.lang,
            "mid": 6,
            "password": self.password,
            "user": self.username,
            # "sessionId": self.sessionId
            
        }
        result = self.curlPost(self.url['login'], param)
        print(result)
        if 'code' in result and result["code"] == '00':
            self.sessionId = result["sessionId"]
            print('set sessionId',self.sessionId)
            self.mobileId = result["userInfo"]["mobileId"]
            self.clientId = result["userInfo"]["clientId"]
            self.cif = result["userInfo"]["cif"]
            session = {"sessionId": self.sessionId, "mobileId": self.mobileId, "clientId": self.clientId, "cif": self.cif}
            self.is_login = True
            self.time_login = time.time()
            self.save_data()
            return {
                'code': 200,
                'success': True,
                'message': 'Đăng nhập thành công',
                'session': session,
                'data': result or ""
            }
        elif result["code"] == '20231' and result["mid"] == '6':
            self.browserToken = result["browserToken"]
            return self.checkBrowser() 
        else:
            return {
                'success': False,
                'message': result["des"],
                "param": param,
                'data': result or ""
            }
    def login(self):
        if not self.is_login or time.time() - self.time_login > 1800:
            login = self.doLogin()
            verify_type = self.verify_type
            if 'success' not in login or not login['success']:
                return login
            if "data" in login and 'mid' in login["data"] and login["data"]['mid']== '3010':
                if verify_type == "5":
                    otp = input("challenge_code:"+login["data"]['challenge']+" | Enter SMART OTP: ")
                    verify_otp = self.submitOtpLogin(otp)
                else:
                    otp = input("Enter SMS OTP:")
                    verify_otp = self.submitOtpSMS(otp)
                return verify_otp
            return login
        return {
                'code': 200,
                'success': True,
                'message': 'Đăng nhập thành công'
            }
    def getE(self):
        ahash = hashlib.md5(self.username.encode()).hexdigest()
        imei = '-'.join([ahash[i:i+4] for i in range(0, len(ahash), 4)])
        return imei.upper()

    def getCaptcha(self):
        captchaToken = ''.join(random.choices(string.ascii_uppercase + string.digits, k=30))
        url = self.url['getCaptcha'] + captchaToken
        response = requests.get(url)
        result = base64.b64encode(response.content).decode('utf-8')
        return result
    # def get_balance(self, retry = False):
    #     try:
    #         print(self.is_login, time.time() - self.time_login > 900)
    #         if not self.is_login or time.time() - self.time_login > 900:
    #             print('relogin')
    #             login = self.login()
    #             if 'success' not in login or not login['success']:
    #                 return login
    #         """
    #         Retrieves the available balance for a given account number from the provided data.

    #         Parameters:
    #         account_number (str): The account number to search for.

    #         Returns:
    #         str: The available balance for the specified account number, or an error message if not found.
    #         """
    #         data = self.getlistAccount()
    #         # if data and 'code' in data and data['code'] == '00' and 'DDAccounts' in data:
    #         #     for account in data.get('DDAccounts', []):
    #         #         if account['accountNumber'] == self.account_number:
    #         #             return account
    #         #     return None
    #         print(data)
    #         if data and 'code' in data and data['code'] == '00' and 'DDAccounts' in data:
    #             for account in data.get('DDAccounts', []):
    #                 if self.account_number == account['accountNumber']:
    #                     if float(account['availableBalance']) < 0:
    #                         return float(account['availableBalance'])
    #                     else:
    #                         return float(account['availableBalance'])
    #             return -1
    #         elif 'code' in data and data['code'] == '108': 
    #             self.is_login = False
    #             self.save_data()
    #             if not retry:
    #                 return self.get_balance(retry=True)
    #             return -1
    #         else: 
    #             self.is_login = False
    #             self.save_data()
    #             if not retry:
    #                 return self.get_balance(retry=True)
    #             return -1
    #     except Exception as e:
    #         self.is_login = False
    #         self.save_data()
    #         print(f"Error in get_balance: {str(e)}")
    #         if not retry:
    #             return self.get_balance(retry=True)
    #         return -1
    def get_balance(self, retry = False):
        try:
            print(self.is_login, time.time() - self.time_login > 900)
            if not self.is_login or time.time() - self.time_login > 900:
                print('relogin')
                login = self.login()
                if 'success' not in login or not login['success']:
                    return login
            """
            Retrieves the available balance for a given account number from the provided data.

            Parameters:
            account_number (str): The account number to search for.

            Returns:
            str: The available balance for the specified account number, or an error message if not found.
            """
            data = self.getAccountDeltail()

            if data and 'code' in data and data['code'] == '00' and 'accountDetail' in data:
                account = data.get('accountDetail', [])
                if self.account_number == account['accountNo']:
                    balance = float(account['availBalance'].replace(',',''))
                    if balance < 0:
                        return balance
                    else:
                        return balance
                return -1
            elif 'code' in data and data['code'] == '108': 
                self.is_login = False
                self.save_data()
                if not retry:
                    return self.get_balance(retry=True)
                return -1
            else: 
                self.is_login = False
                self.save_data()
                if not retry:
                    return self.get_balance(retry=True)
                return -1
        except Exception as e:
            self.is_login = False
            self.save_data()
            print(f"Error in get_balance: {str(e)}")
            if not retry:
                return self.get_balance(retry=True)
            return -1
    def getlistAccount(self):
        param = {
            "DT": self.DT,
            "OV": self.OV,
            "PM": self.PM,
            "browserId": self.browserId,
            "E": self.getE() or "",
            "mid": 8,
            "cif": self.cif,
            "user": self.username,
            "mobileId": self.mobileId,
            "clientId": self.clientId,
            "sessionId": self.sessionId
        }
        result = self.curlPost(self.url['getlistAccount'], param)
        return result

    def getlistDDAccount(self):
        param = {
            "DT": self.DT,
            "OV": self.OV,
            "PM": self.PM,
            "browserId": self.browserId,
            "E": None,
            "lang": "vi",
            "appVersion": "",
            "mid": 35,
            "cif": self.cif,
            "serviceCode":  "0540,0541,0543,0551,2551",
            "user": self.username,
            "mobileId": self.mobileId,
            "clientId": self.clientId,
            "sessionId": self.sessionId
        }
        result = self.curlPost(self.url['getlistDDAccount'], param)
        return result

    def getAccountDeltail(self):
        param = {
            "DT": self.DT,
            "OV": self.OV,
            "PM": self.PM,
            "E": self.getE() or "",
            "browserId": self.browserId,
            "accountNo": self.account_number,
            "accountType": "D",
            "mid": 13,
            "cif": self.cif,
            "user": self.username,
            "mobileId": self.mobileId,
            "clientId": self.clientId,
            "sessionId": self.sessionId
        }
        result = self.curlPost(self.url['getAccountDeltail'], param)
        return result

    def getHistories(self, fromDate="16/06/2023", toDate="16/06/2023", account_number='', page=0,limit = 20):
        if not self.is_login or time.time() - self.time_login > 900:
                login = self.login()
                if 'success' not in login or not login['success']:
                    return login
        param = {
            "DT": self.DT,
            "OV": self.OV,
            "PM": self.PM,
            "E": self.getE() or "",
            "browserId": self.browserId,
            "accountNo": account_number or self.account_number,
            "accountType": "D",
            "fromDate": fromDate,
            "toDate": toDate,
            "lang": self.lang,
            "pageIndex": page,
            "lengthInPage": limit,
            "stmtDate": "",
            "stmtType": "",
            "mid": 14,
            "cif": self.cif,
            "user": self.username,
            "mobileId": self.mobileId,
            "clientId": self.clientId,
            "sessionId": self.sessionId
        }
        result = self.curlPost(self.url['getHistories'], param)
        if result['code'] == '00' and 'transactions' in result:
            return {'code':200,'success': True, 'message': 'Thành công',
                            'data':{
                                'transactions':result['transactions'],
                    }}
        else:
            self.is_login = False
            self.save_data()
            return  {
                    "success": False,
                    "code": 503,
                    "message": "Service Unavailable!"
                }

    def getBanks(self):
        param = {
            "DT": self.DT,
            "OV": self.OV,
            "PM": self.PM,
            "E": self.getE() or "",
            "browserId": self.browserId,
            "lang": self.lang,
            "fastTransfer": "1",
            "mid": 23,
            "cif": self.cif,
            "user": self.username,
            "mobileId": self.mobileId,
            "clientId": self.clientId,
            "sessionId": self.sessionId
        }
        result = self.curlPost(self.url['getBanks'], param)
        return result

    def transfer_external_1(self, bankCode, account_number, amount, message,bank_detail):
        param  = {
            "DT": self.DT,
            "OV": self.OV,
            "PM": self.PM,
            "E": None,
            "amount": str(amount),
            "appVersion": "",
            "browserId": self.browserId,
            "ccyType": "2",
            "cif": self.cif,
            "clientId": self.clientId,
            "creditAccountNo": account_number,
            "debitAccountNo": self.account_number,
            "feeType": "1",
            "lang": "vi",
            "mid": 4034,
            "mobileId": self.mobileId,
            "omniBankCode": bank_detail['omniBankCode'],
            "sessionId": self.sessionId,
            "type": "account",
            "user": self.username
        }
        result = self.curlPost(self.url['tranferOut_1'], param)
        return result
    
    def transfer_external_2(self, bankCode, account_number, amount, message,bank_detail):
        param  = {
            "DT": self.DT,
            "OV": self.OV,
            "PM": self.PM,
            "E": None,
            "amount": str(amount),
            "appVersion": "",
            "browserId": self.browserId,
            "ccyType": "2",
            "cif": self.cif,
            "clientId": self.clientId,
            "creditAccountNo": account_number,
            "debitAccountNo": self.account_number,
            "feeType": "1",
            "lang": "vi",
            "mid": 4035,
            "mobileId": self.mobileId,
            "creditOmniBankCode": bank_detail['omniBankCode'],
            "content": message,
            "sessionId": self.sessionId,
            "user": self.username
        }
        result = self.curlPost(self.url['tranferOut_2'], param)
        return result
        
    def get_bank_name(self, bank_code ,account_number):
        if bank_code == '970436':
            param = {
                "DT": self.DT,
                "OV": self.OV,
                "PM": self.PM,
                "E": "",
                "accountNo": account_number,
                "appVersion": "",
                "browserId": self.browserId,
                "cif": self.cif,
                "clientId": self.clientId,
                "lang": self.lang,
                "mobileId": self.mobileId,
                "sessionId": self.sessionId,
                "user": self.username,
            }
            result = self.curlPost(self.url['get_bank_name_in'], param)
        else:
            
            param = {
            "DT": self.DT,
            "E": None,
            "OV": self.OV,
            "PM": self.PM,
            "accountNo": account_number,
            "appVersion": "",
            "bankCode": str(bank_code),
            "browserId": self.browserId,
            "cif": self.cif,
            "clientId": self.clientId,
            "lang": self.lang,
            "mid": 917,
            "mobileId": self.mobileId,
            "sessionId": self.sessionId,
            "user": self.username
        }
            
            result = self.curlPost(self.url['get_bank_name_out'], param)
        if 'beneficiaryCusName' in result:
            result['cardHolderName'] = result['beneficiaryCusName']

        return result
    def transfer_internal(self,account_name, account_number, amount, message):
        param = {
            "DT": self.DT,
            "E": None,
            "OV": self.OV,
            "PM": self.PM,
            "amount": str(amount),
            "appVersion": "",
            "browserId": self.browserId,
            "ccyType": "2",
            "cif": self.cif,
            "clientId": self.clientId,
            "content": message,
            "creditAccountName": account_name,
            "creditAccountNo": account_number,
            "debitAccountNo": self.account_number,
            "feeType": "1",
            "lang": "vi",
            "mid": 4038,
            "mobileId": self.mobileId,
            "sessionId": self.sessionId,
            "transferCategory": None,  # undefined -> None
            "user": self.username
        }

        result = self.curlPost(self.url['tranferIn'], param)
        return result

    def send_verify_transfer(self,tranId,challengeCode, fptChallenge=None, fptSalt=None, fpt=None):
        param = {
        "DT": self.DT,
        "E": None,
        "OV": self.OV,
        "PM": self.PM,
        "appVersion": "",
        "browserId": self.browserId,
        "challengeCode": challengeCode,
        "cif": self.cif,
        "clientId": self.clientId,
        "facepayChallenge": fptChallenge,
        "facepaySalt": fptSalt,
        "facepaySdkToken": fpt,
        "lang": "vi",
        "mid": 3014,
        "mobileId": self.mobileId,
        "sessionId": self.sessionId,
        "tranId": tranId,
        "user": self.username
        }
        print(param)

        result = self.curlPost("https://digiapp.vietcombank.com.vn/authen-service/v1/api-3014", param)
        return result

    def check_verify_transfer(self,tranId):
        param = {
        "DT": self.DT,
        "E": None,
        "OV": self.OV,
        "PM": self.PM,
        "appVersion": "",
        "browserId": self.browserId,
        "cif": self.cif,
        "clientId": self.clientId,
        "lang": "vi",
        "mid": 3015,
        "mobileId": self.mobileId,
        "sessionId": self.sessionId,
        "tranId": tranId,
        "user": self.username
        }
        print(param)

        result = self.curlPost("https://digiapp.vietcombank.com.vn/authen-service/v1/api-3015", param)
        return result

    def send_request_transfer(self,account_name, account_number, amount, message):
        param = {
            "DT": self.DT,
            "E": None,
            "OV": self.OV,
            "PM": self.PM,
            "amount": str(amount),
            "appVersion": "",
            "browserId": self.browserId,
            "ccyType": "2",
            "cif": self.cif,
            "clientId": self.clientId,
            "content": message,
            "creditAccountName": account_name,
            "creditAccountNo": account_number,
            "debitAccountNo": self.account_number,
            "feeType": "1",
            "lang": "vi",
            "mid": 4038,
            "mobileId": self.mobileId,
            "sessionId": self.sessionId,
            "transferCategory": None,  # undefined -> None
            "user": self.username
        }
        print(param)

        result = self.curlPost(self.url['tranferIn'], param)
        return result

    def genOtpTranFer(self, tranId, type="OUT", otpType=5):
        if otpType == 1:
            solveCaptcha = self.solveCaptcha()
            if not solveCaptcha["status"]:
                return solveCaptcha
            param = {
                "DT": self.DT,
                "OV": self.OV,
                "PM": self.PM,
                "E": self.getE() or "",
                "lang": self.lang,
                "tranId": tranId,
                "type": otpType,  # 1 là SMS,5 là smart otp
                "captchaToken": solveCaptcha["key"],
                "captchaValue": solveCaptcha["captcha"],
                "browserId": self.browserId,
                "mid": 17,
                "cif": self.cif,
                "user": self.username,
                "mobileId": self.mobileId,
                "clientId": self.clientId,
                "sessionId": self.sessionId
            }
        else:
            param = {
                "DT": self.DT,
                "OV": self.OV,
                "PM": self.PM,
                "E": None,
                "appVersion": "",
                "lang": self.lang,
                "tranId": tranId,
                "type": otpType,  # 1 là SMS,5 là smart otp
                "captchaToken": "",
                "captchaValue": "",
                "mid": 17,
                "browserId": self.browserId,
                "cif": self.cif,
                "user": self.username,
                "mobileId": self.mobileId,
                "clientId": self.clientId,
                "sessionId": self.sessionId
            }
            print(param)

        if type == "IN":
            result = self.curlPost(self.url['genOtpIn'], param)
        else:
            result = self.curlPost(self.url['genOtpOut'], param)
        return result

    def confirmTranfer(self, tranId, challenge, otp, type="OUT", otpType=5):
        if otpType == 5:
            param = {
                "DT": self.DT,
                "OV": self.OV,
                "PM": self.PM,
                "E": self.getE() or "",
                "lang": self.lang,
                "tranId": tranId,
                "otp": otp,
                "challenge": challenge,
                "mid": 18,
                "cif": self.cif,
                "user": self.username,
                "browserId": self.browserId,
                "mobileId": self.mobileId,
                "clientId": self.clientId,
                "sessionId": self.sessionId
            }
        else:
            param = {
                "DT": self.DT,
                "OV": self.OV,
                "PM": self.PM,
                "E": self.getE() or "",
                "browserId": self.browserId,
                "lang": self.lang,
                "tranId": tranId,
                "otp": otp,
                "challenge": challenge,
                "mid": 18,
                "cif": self.cif,
                "user": self.username,
                "mobileId": self.mobileId,
                "clientId": self.clientId,
                "sessionId": self.sessionId
            }

        if type == "IN":
            result = self.curlPost(self.url['confirmTranferIn'], param)
        else:
            result = self.curlPost(self.url['confirmTranferOut'], param)
        return result
    def transfer(self,bank_code,account_name, ben_account_number, amount, message,bank_detail):
        if bank_code == '970436':
            result_transfer_init =  self.transfer_internal(account_name,ben_account_number, amount, message)
            if result_transfer_init and 'transaction' in result_transfer_init and 'code' in result_transfer_init and result_transfer_init['code'] == '00':
                tranId = result_transfer_init['transaction']['tranId']
                otp = self.genOtpTranFer(tranId, type="IN", otpType=5)
                otp['tranId'] = tranId
                otp['type'] = "IN"
                if 'code' in otp and otp['code'] == '00' and 'challenge' in otp:
                    return otp
                else:
                    return otp
        else:
            list_account = self.getlistDDAccount()
            # print('list_account',list_account)
            result_transfer_init_0 =  self.transfer_external_1(bank_code, ben_account_number, amount, message,bank_detail)
            
            if result_transfer_init_0 and 'code' in result_transfer_init_0 and result_transfer_init_0['code'] == '00':
                result_transfer_init =  self.transfer_external_2(bank_code, ben_account_number, amount, message,bank_detail)
                print('result_transfer_init',result_transfer_init)

                if result_transfer_init and 'code' in result_transfer_init and result_transfer_init['code'] == '00':   
                    tranId = result_transfer_init['transaction']['tranId']
                    otp = self.genOtpTranFer(tranId, type="OUT", otpType=5)
                    print('otp', otp)
                    otp['tranId'] = tranId
                    otp['type'] = "OUT"
                    if 'code' in otp and otp['code'] == '00' and 'challenge' in otp:
                        return otp
                    else:
                        return otp
            else:
                return result_transfer_init_0



        return result_transfer_init
    def convert_to_uppercase_no_accents(self,text):
        # Remove accents
        no_accents = unidecode.unidecode(text)
        # Convert to uppercase
        return no_accents.upper()
    def transferBank(self,bank_code, ben_account_number, amount, message,account_name):
        info_bank = mapping_bank_code(bank_code)
        bank_code = info_bank['bank_code']
        
        bank_send = {
                    'bankCode': bank_code,
                    'displayNameVi': info_bank['displayNameVi'],
                    'shortName': info_bank['shortName']
        }
        # self.login()
        global list_bank
        check_st = time.time()
        bank_code = bank_send['bankCode']


        bank_detail = None
        for bank in list_bank:
            if bank['bank_code'] == bank_code:
                bank_detail = bank
                break
        if not bank_detail:
            return {
            'code': 401,
            'success': False,
            'message': 'Tài khoản nhận không hợp lệ!',
        }

        print(ben_account_number, bank_code)
        ben_account_info_origin = self.get_bank_name(bank_code,ben_account_number)
        print('ben_account_info_origin',ben_account_info_origin)

        ben_account_info = ben_account_info_origin
        
        if not ben_account_info or 'code' not in ben_account_info or (ben_account_info['code'] != '00' and ben_account_info['code'] != '2011'):   
            return self.bank_checker_process(bank_send,ben_account_info,type="error")
        if 'code' in ben_account_info and ben_account_info['code'] == '2011':
            return {'code':418,'success': False, 'message': 'account_name mismatch!', 'data': ben_account_info_origin}
        if ben_account_info['cardHolderName'].lower().strip().replace(' ','') != self.convert_to_uppercase_no_accents(account_name).lower().strip().replace(' ',''):
            return self.bank_checker_process(bank_send,ben_account_info_origin,type="diff")

        # partnerName = ben_account_info['cardHolderName']
        # name_bank = bank_detail['bankName']
        # bbank_code = bank_detail['bank']

        transfer = self.transfer(bank_code,account_name, ben_account_number, amount, message,bank_detail)
        print('transfer',transfer)
        if ('data' not in transfer or 'code' not in transfer or transfer['code'] != '00') and 'des' in transfer:
            return {'code':500,'success': False, 'message': transfer['des'], 'data': transfer}
        
        if  ('data' not in transfer or 'code' not in transfer or transfer['code'] != '00'):
            return {'code':500,'success': False, 'data': transfer}  

        
        tranId = transfer['tranId']
        challenge = transfer['challenge']
        type_transfer = transfer['type']
        print('set_up_transfer',time.time() - check_st)
        check_st = time.time()
        if 'fpt' in transfer and 'fptChallenge' in transfer and 'fptSalt' in transfer:
            send_verify_transfer_result = self.send_verify_transfer(tranId,challenge, transfer['fptChallenge'], transfer['fptSalt'], transfer['fpt'])
            print('send_verify_transfer',send_verify_transfer_result,time.time() - check_st)
            if not send_verify_transfer_result or 'code' not in send_verify_transfer_result or send_verify_transfer_result['code'] != '00':
                return {'code':500, 'success': False, 'message': 'Unknow error!', 'data': send_verify_transfer_result} 
            print('Vui lòng xác thực giao dịch trên điện thoại(verify transfer in phone)!')
            confirm_transfer = self.confirmTranfer(tranId,challenge,"",type_transfer)
            st = time.time()
            while not confirm_transfer or 'code' not in confirm_transfer or confirm_transfer['code'] != '00':
                if st - time.time() > 60:
                    return {'code':500, 'success': False, 'message': 'Timeout verify'}
                time.sleep(3)
                confirm_transfer = self.confirmTranfer(tranId,challenge,"",type_transfer)
        else:
            send_verify_transfer_result = self.send_verify_transfer(tranId,challenge)
            print('send_verify_transfer',send_verify_transfer_result,time.time() - check_st)
            if not send_verify_transfer_result or 'code' not in send_verify_transfer_result or send_verify_transfer_result['code'] != '00':
                return {'code':500, 'success': False, 'message': 'Unknow error!', 'data': send_verify_transfer_result} 
            print('Vui lòng xác thực giao dịch trên điện thoại(verify transfer in phone)!')
            check_verify_transfer = self.check_verify_transfer(tranId)
            st = time.time()
            while not check_verify_transfer or 'code' not in check_verify_transfer or check_verify_transfer['code'] != '00':
                if st - time.time() > 60:
                    return {'code':500, 'success': False, 'message': 'Timeout verify'}
                time.sleep(2)
                check_verify_transfer = self.check_verify_transfer(tranId)



        confirm_transfer = self.confirmTranfer(tranId,challenge,"",type_transfer)
        if not confirm_transfer or 'code' not in confirm_transfer or confirm_transfer['code'] != '00':
            return {'code':405,'success': False, 'message': 'VCB Bank server error', 'data': confirm_transfer}
        confirm_transfer['success'] = True
        confirm_transfer['message'] = 'Thành công!'
        confirm_transfer['code'] = 200
        return confirm_transfer

    def get_bank_checker(self,shortName, is_random=False, amount = 1):
        file_path = 'bank_account_checker.json'

        # Read the JSON data from the file
        with open(file_path, 'r') as file:
            list_bank_account = json.load(file)
        if is_random:
            if amount == 1:
                return random.choice(list_bank_account)
            else:
                return random.sample(list_bank_account, amount)
        for bank_account in list_bank_account:
            if bank_account['bank_code'] == shortName:
                return bank_account
        return None
    def bank_checker_process(self,bank_send,ben_account_info_origin,type="diff"):
        shortName = bank_send['shortName']
        bank_checker = self.get_bank_checker(shortName)
        print('bank_checker',shortName,bank_checker)
        if bank_checker:
            print(bank_checker['account_number'], bank_send['bankCode'])
            ben_account_info = self.get_bank_name(bank_send['bankCode'],bank_checker['account_number'])
            
            if not ben_account_info or 'code' not in ben_account_info or (ben_account_info['code'] != '00' and ben_account_info['code'] != '2011'):
                return {'code':420,'success': False, 'message': 'Transfer Bank is in Maintenance!', 'data': ben_account_info}

            if  ben_account_info['code'] == '2011':
                if type == "diff":
                    return {'code':419,'success': False, 'message': 'Receiver Bank is in Maintenance!', 'data': ben_account_info_origin}
                elif type == "error":
                    return {'code':419,'success': False, 'message': 'Receiver Bank is in Maintenance!', 'data': ben_account_info_origin}

            if ben_account_info['cardHolderName'].lower().strip().replace(' ','') != self.convert_to_uppercase_no_accents(bank_checker['account_name']).lower().strip().replace(' ',''):
                if type == "diff":
                    return {
                        'success': False,
                        'code': 419,
                        'message': 'Receiver Bank is in Maintenance!',
                        'data': ben_account_info_origin
                    }
                elif type == "error":
                    return {
                        'success': False,
                        'code': 419,
                        'message': 'Receiver Bank is in Maintenance!',
                        'data': ben_account_info_origin
                    }
            if type == "diff":        
                return {'code':418,'success': False, 'message': 'account_name mismatch!', 'data': ben_account_info_origin}
            elif type == "error":
                return {'code':420,'success': False, 'message': 'Transfer Bank is in Maintenance!', 'data': ben_account_info}

        else:
            bank_checker_list = self.get_bank_checker(shortName,True,5)
            for index, bank_checker in enumerate(bank_checker_list):
                
                ben_account_info = self.get_bank_name(bank_send['bankCode'],bank_checker['account_number'])
                
                if not ben_account_info or 'code' not in ben_account_info or (ben_account_info['code'] != '00' and ben_account_info['code'] != '2011'):
                    return {'code':420,'success': False, 'message': 'Transfer Bank is in Maintenance!', 'data': ben_account_info}

                if  ben_account_info['code'] == 2011:
                    if type == "diff":
                        return {'code':419,'success': False, 'message': 'Receiver Bank is in Maintenance!', 'data': ben_account_info_origin}
                    elif type == "error":
                        return {'code':419,'success': False, 'message': 'Receiver Bank is in Maintenance!', 'data': ben_account_info_origin}

                if ben_account_info['cardHolderName'].lower().strip().replace(' ','') != self.convert_to_uppercase_no_accents(bank_checker['account_name']).lower().strip().replace(' ',''):
                    if type == "diff":
                        return {
                            'success': False,
                            'code': 419,
                            'message': 'Receiver Bank is in Maintenance!',
                            'data': ben_account_info_origin
                        }
                    elif type == "error":
                        return {
                            'success': False,
                            'code': 419,
                            'message': 'Receiver Bank is in Maintenance!',
                            'data': ben_account_info_origin
                        }
                if index == 4:
                    if type == "diff":        
                        return {'code':418,'success': False, 'message': 'account_name mismatch!', 'data': ben_account_info_origin['data']}
                    elif type == "error":
                        return {'code':420,'success': False, 'message': 'Transfer Bank is in Maintenance!', 'data': ben_account_info}
   