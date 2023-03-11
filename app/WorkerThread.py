"""
KorDivStockAnalyzerApp

Author
- 코드장인
- https://blog.naver.com/shawgibal
"""


import threading

class WorkerThread(threading.Thread):
    def __init__(self, stockAnalyzer):
        threading.Thread.__init__(self)
        self.stockAnalyzer = stockAnalyzer

    def run(self):
        self.stockAnalyzer.execute()