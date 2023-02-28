import pandas as pd
import kodivstock.divcaculator as divcal

"""
배당 엑셀 파일을 이용하여 배당 성장 기간, 성장률을 분석한다.
"""

class DivExcelAnalyzer:

    """
    배당 이력 엑셀 파일 입력하면 데이터프레임으로 읽어 오기
    """
    def __init__(self, excelFilePath):
        df = pd.read_excel(excelFilePath)
        # 인덱스에 연도를 저장
        df.index = df.iloc[:,0]
        df.index.name = None
        # 연도 칼럼을 제거
        df.drop(df.columns[0], axis=1, inplace=True)
        # 멤버 변수에 결과 저장
        self.df_dps = df

    """
    엑셀 파일의 종목 코드를 리스트로 반환
    """
    def getTickers(self):
        tickers = self.df_dps.columns.values.tolist()
        return tickers

    """
    티커 리스트를 입력하면 배당 성장 기간을 리스트로 반환
    """
    def getDivGrowthYears(self, tickers):
        divGrowthYearList = []
        for ticker in tickers:
            divs = self.df_dps[ticker].to_list()
            divGrowthYear, _ = divcal.caculateActualDivGrowthYears(divs)
            divGrowthYearList.append(divGrowthYear)
        return divGrowthYearList


    """
    티커 리스트, 기간을 입력하면 배당 성장률을 리스트로 반환
    """
    def getDivGrowthRates(self, tickers, period):
        divGrowthRateList = []
        for ticker in tickers:
            divs = self.df_dps[ticker].to_list()
            capital = divs[-1*(period+1)]
            final_balance = divs[-1]
            cagr = divcal.calculateCAGR(capital, final_balance, period)
            divGrowthRateList.append(round(cagr, 2))
        return divGrowthRateList        
