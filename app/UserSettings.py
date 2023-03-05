"""
KorDivStockAnalyzerApp

Author
- 코드장인
- https://blog.naver.com/shawgibal
"""


def getDefaultStockCode():
    try:
        with open("./data/default_stock_code.txt") as file:
            defaultStockCode = file.read()
            return defaultStockCode[:6]
    except Exception as e:
        return ""


if __name__ == '__main__':
  print(getDefaultStockCode())