from datetime import datetime
from utils.logger import Logger
from utils import util

def main():
    file_name = "./logs/py_inj_%s.log" % datetime.today().strftime('%Y-%m-%d-%H%M%S')
    logger = Logger(file_name)
    logger.create_file_and_start()
    logger.info("Starting python script...")

    util.verify_account_sequence()
    util.add_null_merchant()

    qty = 5
    banks = util.create_banks(qty)
    util.create_branch(banks)
    applicants = util.create_applicants(qty)
    applications = util.clean_applications(util.create_applications(applicants))
    users = util.create_users(applications)
    merchants = util.create_merchants(int(qty/5))
    util.create_transactions(users,merchants)

    logger.info("Script completed successfully and is shuting down!")


if __name__=="__main__":
    main()