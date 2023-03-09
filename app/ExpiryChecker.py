"""
KorDivStockAnalyzerApp

Author
- 코드장인
- https://blog.naver.com/shawgibal
"""

from datetime import datetime
from datetime import timedelta
import Config

def checkExpiry():
    expire_date = Config.APP_EXPIRE_DATE
    return datetime.today() > expire_date

def getExiryDate():
    exiryDate = (Config.APP_EXPIRE_DATE - timedelta(days=1)).strftime("%Y-%m-%d")
    return exiryDate

"""
TEST
"""
if __name__ == '__main__':
    expiryDate = getExiryDate()
    print(f'Expiry Date = {expiryDate}')

    checkExpiryResult = checkExpiry()
    print(f'Expiry Check Result = {checkExpiryResult}')