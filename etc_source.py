import pandas as pd

def get_today_stock_price(kind):
    url = 'http://stock.hankyung.com/apps/rank.panel_sub?market='
    if kind == 'kospi':
        return get_today_stock_price_by_url(url+'1')
    elif kind=='kosdaq':
        return get_today_stock_price_by_url(url+'2')
        
def get_today_stock_price_by_url(url):
    tdf = pd.read_html(url, thousands=',')

    df = pd.DataFrame(columns=['종목명','종가','전일비'])

    for t in tdf:
        t.columns = df.columns
        df = df.append(t, ignore_index=True)

    df.전일비 = df.전일비.str.replace('▲','')
    df.전일비 = df.전일비.str.replace('▼','-')
    df.전일비 = df.전일비.str.replace('↑','')
    df.전일비 = df.전일비.str.replace(',','')

    df.종가 = pd.to_numeric(df.종가)
    df.전일비 = pd.to_numeric(df.전일비)
    
    return df.drop_duplicates().reset_index()