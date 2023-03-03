"""
KorDivStockAnalyzerApp

Author
- 코드장인
- https://blog.naver.com/shawgibal
"""

import os
import sys
from AppLogger import LOG

kodivstock_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
+ '/kodivstock/')
sys.path.append(kodivstock_dir)
import divexcelanalyzer as dea


class DivHistoryAnalyzer:
    def __init__(self):
        self.divExcelAnalyzer = dea.DivExcelAnalyzer('./data/tiger_divgrowth50_dps_data_2012_2021.xlsx')

    def checkStockCodeInTigerETF(self, stockCode):
        tickers = self.divExcelAnalyzer.getTickers()
        if not stockCode in tickers:
            raise(Exception(f'<{stockCode}> TIGER 배당성장 ETF 보유 종목이 아닙니다.'))

    def getDivGrowthInfo(self, stockCode):
        divGrowthInfo = {}
        divGrowthYears = self.divExcelAnalyzer.getDivGrowthYears([stockCode])
        LOG(f'div growth years {divGrowthYears}')
        divGrowthInfo['배당 성장 연수'] = divGrowthYears

        divGrowthRate3 = self.divExcelAnalyzer.getDivGrowthRates([stockCode], 3)
        LOG(f'3 year div growth rates  {divGrowthRate3}')
        divGrowthInfo['배당 성장률(3)'] = divGrowthRate3

        divGrowthRate7 = self.divExcelAnalyzer.getDivGrowthRates([stockCode], 7)
        LOG(f'7 year div growth rates  {divGrowthRate7}')
        divGrowthInfo['배당 성장률(7)'] = divGrowthRate7

        return divGrowthInfo
