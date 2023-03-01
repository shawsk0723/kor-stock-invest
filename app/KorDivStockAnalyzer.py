import os
from pykrx import stock
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
import time
plt.rcParams['font.family'] = 'Malgun Gothic'

from AppLogger import LOG
import Config
import StockUtil

def analyzeStock(stockCode):
    LOG(f'analyzeStock, stock code = {stockCode}')

    try:
        stockName = stock.get_market_ticker_name(stockCode)
        #stockName = StockUtil.getStockName(stockCode)
        LOG(f'주식 이름: {stockName}')
    except Exception as e:
        LOG(str(e))
        raise(Exception(f'주식 코드가 맞는지 다시 확인해 주세요!'))

    # check whether code is in the TIGER ETF 50 or not


    # set period
    start_date = Config.START_DATE
    LOG(f'시작일: {start_date}')
    end_date = StockUtil.getLastBusinessDay()
    LOG(f'종료일: {end_date}')

    # collect price
    df_p = stock.get_market_ohlcv(start_date, end_date, stockCode)
    close_prices = savgol_filter(df_p.종가, 51, 3)

    # sleep to aviod server denial
    time.sleep(2)

    # collect dividend
    df_f = stock.get_market_fundamental(start_date, end_date, stockCode, freq='d')
    div_yields = savgol_filter(df_f.DIV, 51, 3)

    df_cur_f = stock.get_market_fundamental(end_date, end_date, stockCode)
    cur_div = df_cur_f.DIV[0]
    LOG(f'현재 배당률 = {round(cur_div, 2)}%')

    # calculate buy/sell price & score
    div_yields_without_zero = df_f.DIV[df_f.DIV > 0]
    div_yields_without_zero_filtered = savgol_filter(div_yields_without_zero, 51, 3)
    div_min = round(min(div_yields_without_zero_filtered), 2)
    div_max = round(max(div_yields_without_zero_filtered), 2)

    buy_price = df_cur_f.DPS[0]/div_max * 100
    LOG(f'목표 매수 가격 = {round(buy_price)}')

    sell_price = df_cur_f.DPS[0]/div_min * 100
    LOG(f'목표 매도 가격 = {round(sell_price)}')

    buy_score = StockUtil.calculate_buy_score(cur_div, div_min, div_max)
    LOG(f'매수 점수 = {round(buy_score)}')

    # draw graph & save image
    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('year')
    ax1.set_ylabel('price', color=color)
    ax1.set_xticks([])
    ax1.plot(close_prices, color=color)

    ax2 = ax1.twinx()

    color = 'tab:blue'
    ax2.set_ylabel('dividend yield', color=color)
    ax2.plot(div_yields, color=color)
    plt.title(f'[{stockName}] 주가 vs. 배당률')

    saveFilePath = os.path.join(Config.OUR_DIR, 'output.png')
    plt.savefig(saveFilePath)
    #plt.show()
