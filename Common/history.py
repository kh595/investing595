import pandas as pd
import matplotlib.pyplot as plt

def get_한투_거래기록(file_path):
    거래기록 = pd.read_csv(file_path, engine='python', thousands=',')
    거래기록 = 거래기록.dropna(subset=['종목명'])
    
    거래기록['거래종류'] = 거래기록.iloc[:,2]
    거래기록.거래종류[거래기록.거래종류.str.contains('매수')] = '매수'
    거래기록.거래종류[거래기록.거래종류.str.contains('매도')] = '매도'

    거래기록['주문일']  = pd.to_datetime(거래기록.거래일)
    거래기록['체결가격'] = pd.to_numeric(거래기록.거래단가)
    거래기록['체결수량'] = pd.to_numeric(거래기록.거래수량) 

    거래기록 = replace_company_name(거래기록)    
    
    return 거래기록

def get_미래_거래기록(file_path):
    거래기록 = pd.read_csv(file_path, engine='python', thousands=',')
    거래기록 = 거래기록.dropna(subset=['종목명'])

    거래기록 = 거래기록.replace({'보통주': ''}, regex=True)

    거래기록.거래종류[거래기록.거래종류.str.contains('매수')] = '매수'
    거래기록.거래종류[거래기록.거래종류.str.contains('매도')] = '매도'

    거래기록['주문일']  = pd.to_datetime(거래기록.거래일자)
    거래기록['체결가격'] = pd.to_numeric(거래기록.단가)
    거래기록['체결수량'] = pd.to_numeric(거래기록.수량) 

    거래기록 = replace_company_name(거래기록)    
    
    return 거래기록

def get_이베스트_거래기록(file_path):
    거래기록 = pd.read_csv(file_path, engine='python', thousands=',')
    거래기록 = 거래기록.dropna(subset=['종목명'])    
    거래기록.columns = 거래기록.columns.str.strip()

    거래기록 = 거래기록[거래기록.상태 == '체결']
    거래기록['거래종류'] = 거래기록.매매구분

    거래기록['주문일']  = pd.to_datetime(거래기록.주문일)
    거래기록['체결가격'] = pd.to_numeric(거래기록.체결가격)
    거래기록['체결수량'] = pd.to_numeric(거래기록.체결수량) 

    거래기록 = replace_company_name(거래기록)    

    return 거래기록


def replace_company_name(거래기록):
    거래기록 = 거래기록.replace('삼화콘덴서', '삼화콘덴서공업')
    거래기록 = 거래기록.replace('휴니드', '휴니드테크놀러지스')
    거래기록 = 거래기록.replace('KT&G', '케이티앤지')
    거래기록 = 거래기록.replace('CJENM', 'CJ ENM')
    거래기록 = 거래기록.replace('현대차', '현대자동차')
    거래기록 = 거래기록.replace('기아차', '기아자동차')
    거래기록 = 거래기록.replace('에스케이 머티리얼즈', 'SK머티리얼즈')
    거래기록 = 거래기록.replace('신한금융지주회사', '신한지주')
    거래기록 = 거래기록.replace('케이엠에이치', 'KMH')
    거래기록 = 거래기록.replace('스튜디오드래곤 주식회사', '스튜디오드래곤')
    거래기록 = 거래기록.replace('에스케이씨 솔믹스', 'SKC 솔믹스')
    거래기록 = 거래기록.replace('에이스테크놀로지', '에이스테크')
    거래기록 = 거래기록.replace('서부티엔디', '서부T&D')
    거래기록 = 거래기록.replace('큐브엔터테인먼트', '큐브엔터')
    거래기록 = 거래기록.replace('푸른상호저축은행', '푸른저축은행')
    거래기록 = 거래기록.replace('케이에스에스 해운 ', 'KSS해운')
    거래기록 = 거래기록.replace('아프리카티비', '아프리카TV')
    거래기록 = 거래기록.replace('에스넷시스템', '에스넷')
    거래기록 = 거래기록.replace('노루페인트 ', '노루페인트')

    return 거래기록


def show_거래기록_with_price(거래기록, naver_stock, price_page_num = 50, 매수='매수', 매도='매도'):
    for 종목명 in 거래기록.종목명.unique():            
        print(종목명)
        tdf = 거래기록[거래기록.종목명 == 종목명]   
        url = naver_stock.get_url_by_name(종목명)
        pdf = naver_stock.get_ts_data(url, price_page_num)

        _, ax = plt.subplots()
        ax.tick_params(axis='x', rotation=45)
        ax.plot(pdf.종가, 'k', label='주가')
        ax.plot(tdf[tdf.거래종류==매수].주문일, tdf[tdf.거래종류==매수].체결가격, 'ro', label='매수')
        ax.plot(tdf[tdf.거래종류==매도].주문일, tdf[tdf.거래종류==매도].체결가격, 'bo', label='매도')
        ax.legend()

    #     ax2 = ax.twinx()
    #     ax2.plot(kospi.loc[pdf.index.max():pdf.index.min()].체결가, 'g', label='kospi', alpha=0.3)
    #     ax2.plot(3*kosdaq.loc[pdf.index.max():pdf.index.min()].체결가, 'y', label='kosdaq', alpha=0.3)
    #     ax2.legend(loc='lower left')
        plt.show()    