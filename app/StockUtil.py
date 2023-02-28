
from datetime import datetime
from datetime import timedelta

import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
from pykrx import stock
import matplotlib.pyplot as plt
import time
plt.rcParams['font.family'] = 'Malgun Gothic'

def getLastBusinessDay():
    yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y%m%d')
    last_business_day = stock.get_nearest_business_day_in_a_week(yesterday)
    return last_business_day