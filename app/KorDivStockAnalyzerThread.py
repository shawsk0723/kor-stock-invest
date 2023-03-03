"""
KorDivStockAnalyzerThread

Author
- 코드장인
- https://blog.naver.com/shawgibal
"""

import os
import sys

from tkinter import *            # tkinter 라이브러리에 모든 함수를 사용
import tkinter.ttk

import numpy as np
import pandas as pd
#from scipy.signal import savgol_filter
from pykrx import stock
import matplotlib.pyplot as plt
import time
#plt.rcParams['font.family'] = 'Malgun Gothic'

import traceback
import threading

from AppLogger import LOG
from KorDivStockPricer import KorDivStockPricer
import Config
import AppUtil

from DivHistoryAnalyzer import DivHistoryAnalyzer


"""
KorDivStockAnalyzerThread
"""
class KorDivStockAnalyzerThread(threading.Thread):
    def __init__(self, root):
        threading.Thread.__init__(self)
        self.root = root
        self.divHistoryAnalyzer = None
        self.stockPricer = None
        self.stockName = ""
        self.analysisResult = {}

    def run(self):
        LOG('KorDivStockAnalyzerThread Start...')

        # output 폴더가 없다면 새로 생성
        AppUtil.makeDirIfNotExist(Config.OUR_DIR)

        self.divHistoryAnalyzer = DivHistoryAnalyzer()
        self.stockPricer = KorDivStockPricer(self.root.stockCode)

        # GUI 업데이트
        self.root.startButton['state'] = DISABLED
        self.root.progressbar.start(10)
        self.root.statusText.delete(1.0, END) # 텍스트 위젯 리셋

        # 주가와 배당금 데이터 수집, 분석 
        try:
            stockCode = self.root.stockCode

            # check whether code is in the TIGER ETF 50 or not
            self.root.statusText.insert(END, f'{stockCode} -> 주식 코드를 확인합니다.\n')
            if Config.isRelease():
                self.divHistoryAnalyzer.checkStockCodeInTigerETF(stockCode)

            # get stock name
            self.stockName = self.stockPricer.getStockName()
            self.root.statusText.insert(END, f'주식 이름은 <<{self.stockName}>>입니다.\n')

            self.root.statusText.insert(END, f'배당 성장 정보를 확인합니다.\n')
            self.divGrowthInfo = self.divHistoryAnalyzer.getDivGrowthInfo(stockCode)

            """ TEST GUI S """
            #self.root.threadCb(True)
            #return
            """ TEST GUI E """

            # collect stock data
            self.root.statusText.insert(END, f'주가/배당금 데이터를 수집합니다.\n')
            self.stockPricer.collectStockData()

            # analyze stock data
            self.root.statusText.insert(END, f'주가/배당금 데이터를 분석합니다.\n')
            self.pricingResult = self.stockPricer.doStockPricing()

            self.analysisResult = {**self.pricingResult, **self.divGrowthInfo}
            self.root.statusText.insert(END, f'데이터 분석을 완료하였습니다.\n')

            self.root.threadCb(True)
        except Exception as e:
            self.root.statusText.insert(END, str(e))
            self.root.threadCb(False)
        finally:
            # GUI 업데이트
            self.root.startButton['state'] = NORMAL
            self.root.progressbar.stop()
            LOG('KorDivStockAnalyzerThread Stop...')

    def getStockName(self):
        return self.stockName

    def getAnalysisResult(self):
        return self.analysisResult

    def saveResult(self):
        self.stockPricer.savePriceDivChart()
        # To-Do save analysis result to excel file
