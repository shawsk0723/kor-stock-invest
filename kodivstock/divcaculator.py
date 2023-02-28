import time
from pykrx import stock

"""
매년 5월 31에 제일 가까운 영업일의 배당금 가져 오기
"""
def getAnnualDps(start_year, end_year, ticker):
    dps_list = []
    for year in range(int(start_year)+1, int(end_year)+2):
        try:
            #print(year)
            last_business_day_of_may = stock.get_nearest_business_day_in_a_week(str(year)+'0531')
            #print(last_business_day_of_may)
            start_date = last_business_day_of_may
            end_date = last_business_day_of_may
            df_annual_f = stock.get_market_fundamental(start_date, end_date, ticker)
            #display(df_annual_f)
            dps_list.append(df_annual_f.DPS.values[0])
            time.sleep(1)
        except Exception as e:
            print(f' {ticker} cannot read dps in {year}')
            dps_list.append(0)
    return dps_list


"""
CAGR 계산
"""
def calculateCAGR(capital, final_balance, period):
    cagr = (final_balance/capital) ** (1/period) - 1
    return cagr


"""
배당금 리스트를 입력하면 연속 배당 성장 연수, 리스트를 반환
"""    
def caculateActualDivGrowthYears(divs):
    div_history = divs.copy()
    div_history.reverse()
    div_growth_list = []
    for div_cur, div_before in zip(div_history, div_history[1:]):
        #print(f'div_cur = {div_cur}, div_before = {div_before}')
        if div_before == 0:
            #print('div_before is 0')
            break;

        if div_cur >= div_before:
            div_growth_list.append(div_cur)
        else:
            #print('div_before is more than div cur')
            div_growth_list.append(div_cur)            
            break

    div_growth_list.reverse()
    return len(div_growth_list) - 1, div_growth_list



