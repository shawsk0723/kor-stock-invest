"""
KorDivStockAnalyzerApp

Author
- 코드장인
- https://blog.naver.com/shawgibal
"""

import pandas as pd

def getDefaultStockCode():
    try:
        df = pd.read_csv('./data/stocklist.csv')
        return str(df.code[0]).zfill(6)
    except Exception as e:
        return ""


if __name__ == '__main__':
  print(getDefaultStockCode())