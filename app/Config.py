import os
from datetime import datetime
import Version

"""
앱 유효 기간
"""
APP_EXPIRE_DATE = datetime(2023,5,1)
#APP_EXPIRE_DATE = datetime(2023,2,1)

"""
App Config
"""
WIN_TITLE = f'안티똥손 {Version.getVersion()}'
START_BUTTON_LABEL = '분석 실행'
DATA_DIR = os.path.join(os.getcwd(), 'data')
OUR_DIR = os.path.join(os.getcwd(), 'output')

"""
Stock Config
"""
START_DATE = '20150501'
