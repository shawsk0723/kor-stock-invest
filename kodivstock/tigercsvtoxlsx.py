import pandas as pd

"""
TIGER 배당성장 ETF CSV 파일을 xlsx 파일로 저장
"""

def convertTigerEtfCsvToXlsx(csvFilePath):
    try:
        df = pd.read_csv(csvFilePath, encoding='EUC-KR')

        """ No 컬럼 삭제 """
        df = df.drop('No', axis=1)

        """ 종목코드가 0인 행 삭제 """
        df = df[df.종목코드 != 0]

        """ 정수형 종목코드를 6자리 스트링으로 변환 """
        tickers = df.종목코드.to_list()
        tickers_new = []
        for ticker in tickers:
            """ 앞에 빈 자리는 0으로 채워서 6자리로 만든다. """
            tickers_new.append(str(ticker).zfill(6))
        df.종목코드 = tickers_new

        """ xlsx 파일로 저장 """
        xlsx_file_path = csvFilePath.replace('.csv', '.xlsx')
        df.to_excel(xlsx_file_path, index=False)
        return xlsx_file_path
    except Exception as e:
        raise e
