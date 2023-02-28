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
plt.rcParams['font.family'] = 'Malgun Gothic'

import traceback
import threading

from AppLogger import LOG
import KorDivStockAnalyzer

"""
KorDivStockAnalyzerThread
"""
class KorDivStockAnalyzerThread(threading.Thread):
    def __init__(self, root):
        threading.Thread.__init__(self)
        self.root = root

    def run(self):
        self.isRunning = True

        LOG('KorDivStockAnalyzerThread Start...')
        # GUI 업데이트
        self.root.startButton['state'] = DISABLED
        self.root.progressbar.start(10)

        # 주가/배당금 분석 
        KorDivStockAnalyzer.analyzeStock(self.root.stockCode)

        # GUI 업데이트
        self.root.startButton['state'] = NORMAL
        self.root.progressbar.stop()


        LOG('KorDivStockAnalyzerThread Stop...')


    def requestExitThread(self):
        self.isRunning = False