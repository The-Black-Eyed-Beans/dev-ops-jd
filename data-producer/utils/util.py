from os import environ
import re
from requests import post
from random import randint
from faker import Faker
from faker.providers import internet,date_time,misc
from .conn import get_conn
from .logger import Logger
from .request import Request

req = Request()
logger = Logger()
fake = Faker()
fake.add_provider(internet)
fake.add_provider(date_time)
fake.add_provider(misc)

conn_attempts = 3
ACCOUNT_TYPES = {0:'SAVINGS',1:'CHECKING',2:'CHECKING_AND_SAVINGS'}

def get_random_license():
    return "DL%d" % randint(10000, 99999)

def get_random_social_security():
    return "%d-%d-%d" % (randint(100,999),randint(10,99),randint(1000,9999))

def get_random_routing_num():
    return randint(100000000, 999999999)

def get_random_phone_num():
    return "(%d) %d-%d" % (randint(100, 999),randint(100, 999),randint(1000, 9999))

def get_random_address():
    addr = fake.address().split('\n')
    if (len(addr) > 2): get_random_address()
    addr = [addr[0]] + addr[1].split(', ')
    return addr[:2] + addr[-1].split(' ')

def create_applicants(qty):
    logger.info("Attempting to create %d dummy applicants...",qty)
    applicants = []
    for i in range(qty):
        logger.info("Applicant #%d" % i)
        applicants.append(add_applicant())
    return applicants

def create_applications(applicants):
    logger.info("Attempting to create %d dummy applications...",len(applicants))
    ids = list(map(lambda x: x['id'],applicants))
    apps = []
    i = 1
    for id in ids:
        logger.info("Application #%d" % i)
        apps.append(add_application(id))
        i+=1
    return apps

def create_banks(qty):
    logger.info("Attempting to create %d dummy banks...",qty)
    banks = []
    for i in range(qty):
        logger.info("Bank #%d",i)
        banks.append(add_bank())
    return banks

def create_branch(banks):
    logger.info("Attempting to create %d dummy branches...",len(banks))
    branches = []
    for i in range(len(banks)):
        logger.info("Branch #%d",i)
        branches.append(add_branch(banks[i]['id']))
    return branches

def add_null_merchant():
    logger.info("Querying database for null merchant...")
    conn = get_conn()
    curs = conn.cursor()
    curs.execute(('SELECT * FROM %s WHERE code="NONE"' % "merchant"))
    r = curs.fetchall()
    if (len(r) == 0): 
        logger.debug("No record found!")
        set_null_merchant()
        return
    logger.info("Record found. Continuing to next process...")

def set_null_merchant():
    logger.info("Attempting to insert NULL merchant...")
    conn = get_conn()
    curs = conn.cursor()
    sql = 'INSERT INTO merchant VALUES("NONE",null,null,null,"NONE",null,null,null)'
    try:
        curs.execute(sql)
        conn.commit()
        logger.info("Execution complete. Records commited: 1")
    except:
        logger.error("Execution failed. This may lead to errors/bugs when populating certain transactions!")

def create_merchants(qty):
    logger.info("Attempting to create %d dummy merchants...",qty)
    merchants = []
    for i in range(qty):
        logger.info("Merchant #%d",i+1)
        merchants.append(add_merchant())
    return merchants

def create_transactions(users,merchants):
    logger.info("Attempting to create %d dummy transactions...",len(users))
    transactions = []
    i = 1
    for user in users:
        rand_int = randint(0, len(merchants)-1)
        merchant = merchants[rand_int]
        logger.info("Transaction #%d",i)
        #transactions.append(add_transaction(user,merchant))
        url = "http://%s/api/transactions" % environ.get('BASE_URL')
        Faker.seed(0)
        payload = {
            "type":"DEPOSIT",
            "accountNumber":user['accountNumber'],
            "amount":get_random_routing_num(),
            "merchantCode":merchant['code'],
            "merchantName":merchant['name'],
            "description": fake.text(max_nb_chars=15),
            "method":"ATM",
            "hold":False
        }
        msg_success = "Microservice successfully added transaction to database!"
        msg_fail = "Microservice failed to add transaction to database! Reattempting..."
        transactions.append(req.post(url,payload,msg_success,msg_fail))
        i+=1
    return transactions

def create_users(apps):
    logger.info("Attempting to create %d dummy users...",len(apps))
    users_list = []
    i = 1
    for application in apps:
        logger.info("User #%d",i)
        user = add_user(application)
        if (user != None): users_list.append(user)
        i+=1
    return users_list

def add_applicant():
    # Add new applicant
    # Returns {applicant}
    logger.info("Creating dummy applicant.")    
    url = "http://%s/api/applicants" % environ.get('BASE_URL')
    addr = get_random_address()
    gender = "FEMALE"
    if (randint(0,99) % 2 == 0): gender = "MALE"
    payload = {
        "firstName": fake.name().split(' ')[0],
        "lastName": fake.name().split(' ')[1],
        "address":addr[0],
        "city":addr[1],
        "state":fake.state(),
        "zipcode":addr[-1],
        "mailingAddress":addr[0],
        "mailingCity":addr[1],
        "mailingState":addr[-2],
        "mailingZipcode":addr[-1],
        "phone":get_random_phone_num(),
        "driversLicense":get_random_license(),
        "socialSecurity": get_random_social_security(),
        "income":get_random_routing_num(),
        "gender":gender,
        "dateOfBirth": fake.date(),
        "email":fake.email()
    }
    logger.info("Dummy applicant successfully generated.")
    msg_success = "Microservice successfully added applicant to database!"
    msg_fail = "Microservice failed to add applicant to database! Reattempting..."
    res = req.post(url,payload,msg_success,msg_fail)
    if (res): return res
    return add_applicant()

def add_application(id):
    # Add new applicants
    # Returns {applications}
    rand_num = randint(1,100)
    account_type = ACCOUNT_TYPES[rand_num % 3]
    logger.info("Creating %s application." % account_type)
    url = "http://%s/api/applications" % environ.get('BASE_URL')
    payload = {
        "applicationType":account_type,
        "noApplicants":True,
        "applicantIds": [id]
    }
    msg_success = "Microservice successfully added application to database!"
    msg_fail = "Microservice failed to add application to database! Reattempting..."
    res = req.post(url,payload,msg_success,msg_fail)
    return res

def add_bank():
    # Add new bank
    # Returns {bank}
    logger.info("Creating dummy bank.")
    url = "http://%s/api/banks" % environ.get('BASE_URL')
    addr = get_random_address()
    payload = {
        "routingNumber":get_random_routing_num(),
        "address":addr[0],
        "city":addr[1],
        "state":addr[2],
        "zipcode":addr[3]
    }
    logger.info("Dummy bank successfully generated.")
    msg_success = "Microservice successfully added bank to database!"
    msg_fail = "Microservice failed to add bank to database! Reattempting..."
    res = req.post(url,payload,msg_success,msg_fail)
    if (res): return res
    return add_bank()

def add_branch(bankId):
    # Add new branch
    # Returns {branch}
    logger.info("Creating dummy branch.")
    url = "http://%s/api/branches" % environ.get('BASE_URL')
    addr = get_random_address()
    payload = {
        "bankID":bankId,
        "name":"%s Branch"%fake.name().split(' ')[1],
        "phone":get_random_phone_num(),
        "address":addr[0],
        "city":addr[1],
        "state":addr[2],
        "zipcode":addr[3]
    }
    logger.info("Dummy branch successfully generated.")
    msg_success = "Microservice successfully added branch to database!"
    msg_fail = "Microservice failed to add branch to database! Reattempting..."
    res = req.post(url,payload,msg_success,msg_fail)
    if (res): return res
    return add_branch(bankId)

def add_merchant():
    # Add new merchant
    # Returns {merchant}
    logger.info("Creating dummy merchant.")
    name = fake.name().split(' ')[0]
    rand_int = randint(1, 999)
    merchant_name = "%s%d LLC" % (name,rand_int)
    code = "%s%d" % (merchant_name[:4],rand_int)
    payload = {
        "code":code,
        "name":merchant_name,
    }
    logger.info("Dummy merchant successfully generated.")
    return payload

def add_user(applicant):
    # Add new user 
    # Returns {user}
    logger.info("Creating dummy user.")
    url = "http://%s/api/users/registration"  % environ.get('BASE_URL')
    username = "%s%s%d" % (applicant['firstName'],applicant['lastName'][-2:],randint(10,99999))
    payload = {
        "role":"member",
        "username": username,
        #"password": get_password(),
        "password": "Pass123!",
        "membershipId": applicant['membershipId'],
        "lastFourOfSSN": applicant['socialSecurity'][7:]
    }
    logger.info("Dummy user successfully generated.")
    logger.info("Sending data to microservice...")
    headers = {'Authorization':req.token,"Content-Type":"application/json"}
    for i in range(conn_attempts):
        r = post(url,headers=headers,json=payload)
        if (r.status_code >= 200 and r.status_code <= 300):
            logger.info("Microservice successfully added user to database!")
            data = r.json()
            # add accountNumber to User obj
            data['accountNumber'] = applicant['accountNumber']
            return data
        logger.error("Microservice failed to add user to database! Reattempting...")
    logger.error("Microservice failed. Attempts exhausted!")

def add_transaction(user,merchant):
    # Add new transaction
    # Returns {transaction}
    logger.info("Creating dummy transaction.")
    url = "http://%s/api/transactions" % environ.get('BASE_URL')
    Faker.seed(0)
    payload = {
        "type":"DEPOSIT",
        "accountNumber":user['accountNumber'],
        "amount":get_random_routing_num(),
        "merchantCode":merchant['code'],
        "merchantName":merchant['name'],
        "description": fake.text(max_nb_chars=15),
        "method":"ATM",
        "hold":False
    }
    logger.info("Dummy transaction successfully generated.")
    msg_success = "Microservice successfully added transaction to database!"
    msg_fail = "Microservice failed to add transaction to database! Reattempting..."
    res = req.post(url,payload,msg_success,msg_fail)
    if (res): return res
    return add_transaction

def clean_applications(apps):
    logger.info("Starting application spin cycle (removing denied accounts).")
    applications_list = []
    for application in apps:
        logger.info("Checking application status...")
        if (application and application['membersCreated']): 
            logger.info("Application approved. Adding to list...")
            application['applicants'][0]['membershipId'] = int(application['createdMembers'][0]['membershipId'])
            application['applicants'][0]['accountNumber'] = application['createdAccounts'][0]['accountNumber']
            applications_list.append(application['applicants'][0])
            logger.info("Application successfully added to list...")
        else: logger.debug("Application denied. Skipping...")
    return applications_list

def set_account_sequence():
    logger.info("Attempting to add new record to table...")
    tbl = "account_sequence"
    conn = get_conn()
    curs = conn.cursor()
    sql = "INSERT INTO %s.%s VALUES (%d)" % (environ.get('MYSQL_DATABASE'),tbl,101)

    try:
        curs.execute(sql)
        conn.commit()
        logger.info("Execution complete. Records commited: %s",curs.rowcount)
    except:
        logger.error("Execution failed. This will cause an error when populating accounts!")

def get_password():
    logger.info("Generating random password...")
    Faker.seed(0)
    password = fake.password()
    if (password_is_valid(password)): return password
    logger.info("Password failed to pass constrants! Reattempting...")
    return get_password()

def password_is_valid(password):
    exp = '''^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[-~`"/\\'}|@$!;:%*<>_[\]{^=#+()?&])[A-Za-z0-9@$-~!"%*^#+()?&]{8,}$'''
    r = re.search(exp,password)
    if (r == None): return False
    logger.info("Password passed contraints!")
    return True

def verify_account_sequence():
    logger.info("Retrieving last record in account_sequence...")
    conn = get_conn()
    curs = conn.cursor()
    curs.execute(("SELECT * FROM %s" % "account_sequence"))
    r = curs.fetchall()
    if (len(r) == 0): 
        logger.debug("No record found!")
        set_account_sequence()
        return
    logger.info("Record found. Continuing to next process...")
