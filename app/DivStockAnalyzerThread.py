"""
KorDivStockAnalyzerThread

Author
- 코드장인
- https://blog.naver.com/shawgibal
"""

import os
from tkinter import *            # tkinter 라이브러리에 모든 함수를 사용
import threading

import Config
import logging
from KorDivStockPricer import KorDivStockPricer
from KorDivHistoryAnalyzer import KorDivHistoryAnalyzer
import kodivstock.stockutil as stockutil

def LOG(msg):
    logging.debug(msg)


"""
KorDivStockAnalyzerThread
"""
class DivStockAnalyzerThread(threading.Thread):
    def __init__(self, root, stockCodeList):
        threading.Thread.__init__(self)
        self.root = root
        self.stockCodeList = stockCodeList
        self.divHistoryAnalyzer = None
        self.stockPricer = None
        self.stockNameList = []
        self.analysisResult = {}

    def run(self):
        LOG('KorDivStockAnalyzerThread Start...')

        self.divHistoryAnalyzer = KorDivHistoryAnalyzer()

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

            # create KorDivStockPricer
            self.stockPricer =KorDivStockPricer(stockCode)

            # get stock name
            stockName = self.stockPricer.getStockName()
            self.stockNameList.append(stockName)
            self.root.statusText.insert(END, f'주식 이름은 <<{stockName}>>입니다.\n')

            self.root.statusText.insert(END, f'배당 성장 정보를 확인합니다.\n')
            self.divGrowthInfo = self.divHistoryAnalyzer.getDivGrowthInfo(stockCode)

            """ TEST GUI S """
            #self.root.threadCb(True)
            #return
            """ TEST GUI E """

            self.stockPricer = KorDivStockPricer(self.root.stockCode)

            # collect stock data
            self.root.statusText.insert(END, f'주가/배당금 데이터를 수집합니다.\n')

            startDate = Config.START_DATE
            LOG(f'시작일: {startDate}')
            endDate = stockutil.getLastBusinessDay()
            LOG(f'종료일: {endDate}')

            self.stockPricer.collectStockData(startDate, endDate)

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
        return self.stockNameList

    def getAnalysisResult(self):
        return self.analysisResult

    def saveResult(self):
        # save price div chart by image file
        imageFilePath = os.path.join(Config.OUT_DIR, f'{self.stockNameList[-1]}.png')
        self.stockPricer.savePriceDivChart(imageFilePath)

        # To-Do: save analysis result to excel file
