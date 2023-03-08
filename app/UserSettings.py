"""
KorDivStockAnalyzerApp

Author
- 코드장인
- https://blog.naver.com/shawgibal
"""

import pandas as pd


class StockLister:
    def __init__(self, filePath, stockCodeKey):
        self.filePath = filePath
        self.stockCodeKey = stockCodeKey

    def getFirstStockCode(self):
        try:
            df = pd.read_csv(self.filePath)
            stockCodeKey = self.stockCodeKey
            return str(df[stockCodeKey][0]).zfill(6)
        except Exception as e:
            print(str(e))
            return ""

    def getStockCodeList(self):
        try:
            df = pd.read_csv(self.filePath)
            stockCodeKey = self.stockCodeKey
            stockCodes = []
            for stockCode in df[stockCodeKey]:
                stockCodes.append(str(stockCode).zfill(6))
            return stockCodes
        except Exception as e:
            print(str(e))
            return ""


def getDefaultStockCode():
    try:
        df = pd.read_csv('./data/stocklist.csv')
        return str(df.StockCode[0]).zfill(6)
    except Exception as e:
        print(str(e))
        return ""

def getStockCodeList():
    try:
        df = pd.read_csv('./data/stocklist.csv')
        stockCodes = []
        for stockCode in df.StockCode:
            stockCodes.append(str(stockCode).zfill(6))
        return stockCodes
    except Exception as e:
        print(str(e))
        return ""


if __name__ == '__main__':
    stockLister = StockLister('./data/stocklist.csv', 'StockCode')
    defaultStockCode = stockLister.getFirstStockCode()
    print(f'defaultStockCode = {defaultStockCode}')
    stockCodeList = stockLister.getStockCodeList()
    print(f'stockCodeList = {stockCodeList}')

    """
    defaultStockCode = getDefaultStockCode()
    print(f'defaultStockCode = {defaultStockCode}')
    stockCodeList = getStockCodeList()
    print(f'stockCodeList = {stockCodeList}')
    """