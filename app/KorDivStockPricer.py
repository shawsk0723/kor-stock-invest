"""
KorDivStockAnalyzerApp

Author
- 코드장인
- https://blog.naver.com/shawgibal
"""

import logging
from pykrx import stock
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
import time
plt.rcParams['font.family'] = 'Malgun Gothic'

import kodivstock.stockutil as stockutil

def LOG(msg):
    logging.debug(msg)

SLEEP_TIME = 2

class KorDivStockPricer():
    def __init__(self, stockCode):
        self.stockCode = stockCode
        self.stockName = ""

    def getStockName(self):
        LOG(f'getStockName, stock code = {self.stockCode}')

        try:
            if self.stockName == "":
                self.stockName = stock.get_market_ticker_name(self.stockCode)
            LOG(f'주식 이름: {self.stockName}')
            return self.stockName
        except Exception as e:
            LOG(str(e))
            raise(Exception(f'주식 코드가 맞는지 다시 확인해 주세요!'))

    """
    주가, 배당금 데이터 수집
    """
    def collectStockData(self, startDate, endDate):
        LOG(f'collectStockData, stock name = {self.stockName}')

        stockCode = self.stockCode

        # collect price
        self.df_p = stock.get_market_ohlcv(startDate, endDate, stockCode)

        # sleep to aviod server denial
        time.sleep(SLEEP_TIME)

        # collect dividend
        self.df_f = stock.get_market_fundamental(startDate, endDate, stockCode, freq='d')

        # sleep to aviod server denial
        time.sleep(SLEEP_TIME)

        self.df_cur_f = stock.get_market_fundamental(endDate, endDate, stockCode)

        # sleep to aviod server denial
        time.sleep(SLEEP_TIME)

    """
    주가, 배당금 데이터로 매수 가격, 매도 가격, 매수 점수 계산
    """
    def doStockPricing(self):
        LOG(f'doStockPricing, stock name = {self.stockName}')
        
        df_f = self.df_f
        df_p = self.df_p
        df_cur_f = self.df_cur_f

        # calculate buy/sell price & score
        self.close_prices = savgol_filter(df_p.종가, 51, 3)
        self.div_yields = savgol_filter(df_f.DIV, 51, 3)

        div_yields_without_zero = df_f.DIV[df_f.DIV > 0]
        div_yields_without_zero_filtered = savgol_filter(div_yields_without_zero, 51, 3)
        div_min = round(min(div_yields_without_zero_filtered), 2)
        div_max = round(max(div_yields_without_zero_filtered), 2)

        self.pricingResult = {}
        self.cur_dps = df_cur_f.DPS[0]
        LOG(f'배당금 = {self.cur_dps}')
        self.pricingResult['배당금'] = [self.cur_dps]

        self.cur_div = df_cur_f.DIV[0]
        LOG(f'배당률 = {self.cur_div}')
        self.pricingResult['배당률'] = [self.cur_div]

        self.buy_price = df_cur_f.DPS[0]/div_max * 100
        LOG(f'목표 매수 가격 = {round(self.buy_price)}')
        self.pricingResult['목표 매수 가격'] = [round(self.buy_price)]

        self.sell_price = df_cur_f.DPS[0]/div_min * 100
        LOG(f'목표 매도 가격 = {round(self.sell_price)}')
        self.pricingResult['목표 매도 가격'] = [round(self.sell_price)]

        self.buy_score = stockutil.calculate_buy_score(self.cur_div, div_min, div_max)
        LOG(f'매수 점수 = {round(self.buy_score)}')
        self.pricingResult['매수 점수'] = [round(self.buy_score)]

        return self.pricingResult

    def getResult(self):
        return self.pricingResult

    def savePriceDivChart(self, imageFilePath):

        # draw graph & save image
        plt.rcParams["figure.figsize"] = (8,6)
        fig, ax1 = plt.subplots()

        color = 'tab:red'
        ax1.set_xlabel('year')
        ax1.set_ylabel('price', color=color)
        ax1.set_xticks([])
        ax1.plot(self.close_prices, color=color)

        ax2 = ax1.twinx()

        color = 'tab:blue'
        ax2.set_ylabel('dividend yield', color=color)
        ax2.plot(self.div_yields, color=color)

        ax2.axhline(y=min(self.div_yields), color='y', linestyle='--', label='min div yield')
        ax2.axhline(y=max(self.div_yields), color='r', linestyle='--', label='max div yield')
        ax2.axhline(y=self.div_yields[-1], color='g', linestyle='--', label='current div yield')

        plt.legend(loc='upper left', framealpha=1.0)
        plt.title(f'[{self.getStockName()}] 주가 vs. 배당률')
        plt.savefig(imageFilePath)
        plt.close('all')
        #plt.show()

