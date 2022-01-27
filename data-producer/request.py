from os import environ
from requests import post, exceptions
from logger import Logger

class Request(Logger):

    def __init__(self):
        self.token = False
        self.request_attempts = 10
        self.std_out = False
        self.register_attempt = False

    def post(self,url,payload,msg_success,msg_fail):
        self.info("Sending data to microservice...")
        headers = {'Authorization':self.get_token(),"Content-Type":"application/json"}
        for i in range(self.request_attempts):
            r = False
            try:
                r = post(url,headers=headers,json=payload)
            except exceptions.RequestException as e:
                self.error(e)
                return False
            if (r and r.status_code >= 200 and r.status_code <= 300):
                self.info(msg_success)
                return r.json()
            self.error(msg_fail)
            return False

    def register_admin(self,payload):
        # Register admin
        self.info("Attempting to Register admin.")
        url = "http://%s/api/users/registration" % environ.get('BASE_URL')
        r = False
        try:
            r = post(url,json=payload)
        except exceptions.RequestException as e:
            self.error(e)
            return False
        if (r and r.status_code >= 200 and r.status_code <= 300):
            self.username = payload['username']
            self.password = payload['password']
            self.info("Admin successfully registered.")
            self.info("username: %s password: %s",self.username,self.password)
            self.register_attempt = True
            return False
        self.error("Admin failed to be registered!")
    
    def credentials(self):
        return {
            "username":environ.get('USER_USERNAME'),
            "password":environ.get('USER_PASSWORD'),
        }

    def create_admin(self):
        admin = {
            "role":environ.get('USER_ROLE'),
            "username":environ.get('USER_USERNAME'),
            "password":environ.get('USER_PASSWORD'),
            "firstName":environ.get('USER_FIRSTNAME'),
            "lastName":environ.get('USER_LASTNAME'),
            "email":environ.get('USER_EMAIL'),
            "phone":environ.get('USER_PHONE'),
        }
        self.register_admin(admin)

    def fetch_token(self):
        # Returns jwt -> Bearer xyz
        self.info("Attempting to retieve token.")
        url = "http://%s/login" % environ.get('BASE_URL')
        r = False
        try:
            r = post(url,json=self.credentials())
        except exceptions.RequestException as e:
            self.error(e)
            return False
        if (r.status_code >= 200 and r.status_code <= 300):
            self.token = r.headers['Authorization']
            self.info("Token: %s", self.token.split(' ')[1])
        elif(r.status_code == 403 and self.register_attempt == False): 
            self.create_admin()
            return self.fetch_token()

    def get_token(self):
        if (self.token): return self.token
        self.fetch_token()
        if (self.token): return self.token
        self.error("Failed to retrieve token!")
        raise ValueError('Failed to retrieve token!')
