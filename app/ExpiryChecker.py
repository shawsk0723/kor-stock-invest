"""
KorDivStockAnalyzerApp

Author
- 코드장인
- https://blog.naver.com/shawgibal
"""
import os
from hashlib import blake2b
import tempfile
from datetime import datetime
from datetime import timedelta
import Config

def checkExpiry():
    expire_date = Config.APP_EXPIRE_DATE
    return datetime.today() > expire_date

def getExiryDate():
    exiryDate = (Config.APP_EXPIRE_DATE - timedelta(days=1)).strftime("%Y-%m-%d")
    return exiryDate

class ExpiryChecker:
    def __init__(self, expiration_day = Config.EXPIRATION_DAY):
        m = blake2b(digest_size=17)
        m.update(Config.WIN_TITLE.encode('utf-8'))
        expiryfilename = m.hexdigest() + '.bin'
        #print(f'expiryfilename length = {len(expiryfilename)}')
        self.expiry_file_path = os.path.join(tempfile.gettempdir(), expiryfilename) 
        self.expiration_day = expiration_day
        self.remained_day = 0

    def isExpired(self):
        current_date = datetime.now()
        print(f'expiry_file_path = {self.expiry_file_path}')
        if os.path.isfile(self.expiry_file_path):
            with open(self.expiry_file_path, 'r') as f:
                install_date =f.read()
                install_date = datetime.strptime(install_date, "%Y%m%d")
                print(f'install_date = {install_date}')
                print(f'current_date = {current_date}')
                elapsed_day = current_date - install_date
                self.remained_day = self.expiration_day - elapsed_day.days
                return elapsed_day > timedelta(self.expiration_day)
        else:
            with open(self.expiry_file_path, 'w') as f:
                f.write(f'{current_date.strftime("%Y%m%d")}')
                self.remained_day = self.expiration_day
                return False

    def getRemainedDay(self):
        return self.remained_day

"""
TEST
"""
if __name__ == '__main__':
    expiryDate = getExiryDate()
    print(f'Expiry Date = {expiryDate}')

    checkExpiryResult = checkExpiry()
    print(f'Expiry Check Result = {checkExpiryResult}')

    expiryChecker = ExpiryChecker()
    expired = expiryChecker.isExpired()
    print(f'expired = {expired}')
    print(f'remained day = {expiryChecker.getRemainedDay()}')