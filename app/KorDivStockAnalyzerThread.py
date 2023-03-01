"""
KorDivStockAnalyzerThread

Author
- 코드장인
- https://blog.naver.com/shawgibal
"""

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
from KorDivStockAnalyzer import KorDivStockAnalyzer
import Config
import AppUtil

"""
KorDivStockAnalyzerThread
"""
class KorDivStockAnalyzerThread(threading.Thread):
    def __init__(self, root):
        threading.Thread.__init__(self)
        self.root = root
        self.stockAnalyzer = KorDivStockAnalyzer(self.root.stockCode)

    def run(self):
        LOG('KorDivStockAnalyzerThread Start...')

        # output 폴더가 없다면 새로 생성
        AppUtil.makeDirIfNotExist(Config.OUR_DIR)

        # GUI 업데이트
        self.root.startButton['state'] = DISABLED
        self.root.progressbar.start(10)

        # 주가와 배당금 데이터 수집, 분석 
        try:
            stockName = self.stockAnalyzer.getStockName()

            self.root.statusLabel.configure(text = f'{stockName} 데이터를 수집합니다.')
            self.stockAnalyzer.collectStockData()

            self.root.statusLabel.configure(text = f'{stockName} 데이터를 분석합니다.')
            self.stockAnalyzer.analyzeStockData()

            self.root.statusLabel.configure(text = f'{stockName} 데이터 분석을 완료하였습니다.')

            self.root.threadCb(True)
        except Exception as e:
            self.root.statusLabel.configure(text = str(e))
            self.root.threadCb(False)
        finally:
            # GUI 업데이트
            self.root.startButton['state'] = NORMAL
            self.root.progressbar.stop()
            LOG('KorDivStockAnalyzerThread Stop...')


