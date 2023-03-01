
from datetime import datetime
from datetime import timedelta

import os
import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
from pykrx import stock
import matplotlib.pyplot as plt
import time
#plt.rcParams['font.family'] = 'Malgun Gothic'

from AppLogger import LOG



def getLastBusinessDay():
    yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y%m%d')
    last_business_day = stock.get_nearest_business_day_in_a_week(yesterday)
    return last_business_day

def getStockNameByCode(code):
    try:
        name = stock.get_market_ticker_name(code)
        LOG(f'stock name = {name}')
        return name
    except Exception as e:
        LOG(str(e))
        raise(e)

def get_percentage(input, min, max):
    return round((input - min) / (max - min) * 100)

def calculate_buy_score(current_div_yield, div_min, div_max):
    buy_score = get_percentage(current_div_yield, div_min, div_max)
    return buy_score