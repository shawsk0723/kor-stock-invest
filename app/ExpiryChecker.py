from datetime import datetime
#from datetime import timedelta
import Config

def checkExpiry():
    expire_date = Config.APP_EXPIRE_DATE
    return datetime.today() > expire_date
