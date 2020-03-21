import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib as mpl
import matplotlib.font_manager as fm
import dart_fss as dart
from bs4 import BeautifulSoup

import time
import re
import os
import zipfile


# 별도만 있는지 연결도 있는지 확인
def has_connected_by_code(df, company, kind_code):  
    tdf = df[(df.회사명==company) & (df.항목코드 == kind_code)]
    target_filter = (tdf.재무제표종류.str.contains('연결'))
    if target_filter.sum() == 0:
        return False
    else:
        return True

def has_connected_by_name(df, company, kind_name):    
    tdf = df[(df.회사명==company)]
    tdf = tdf[(tdf.항목명.str.contains(kind_name))]
    target_filter = tdf.재무제표종류.str.contains('연결')
    if target_filter.sum() == 0:
        return False
    else:
        return True

def get_target_kind_by_code(df, company, kind_code):
    if has_connected_by_code(df, company, kind_code):       
        str_tkind = "연결"
    else :
        str_tkind = "별도"

    tdf = df[df.회사명==company]
    tdf = tdf[tdf.재무제표종류.str.contains(str_tkind)]
    target_filter = tdf.항목코드 == kind_code
    target_filter |= tdf.항목코드 == kind_code.replace('ifrs', 'ifrs-full')
    tdf = tdf[target_filter]
    ret_df = tdf.groupby(['재무제표종류', '항목코드']).size().reset_index(name='count')

    print(company, str_tkind, len(tdf))
    return ret_df
        
def get_target_kind_by_name(df, company, kind_name):
    if has_connected_by_name(df, company, kind_name):       
        str_tkind = "연결"
    else :
        str_tkind = "별도"
    
    tdf = df[(df.회사명==company)]
    tdf = tdf[(tdf.항목명.str.contains(kind_name))]
    tdf = tdf[tdf.재무제표종류.str.contains(str_tkind)]
    ret_df = tdf.groupby(['재무제표종류', '항목명', '항목코드']).size().reset_index(name='count')

    print(company, str_tkind, len(tdf))
    return ret_df


def get_target_df(df, company, kind_kind, kind_code):
    target_filter = (df.회사명==company) & (df.항목코드 == kind_code) & (df.재무제표종류 == kind_kind)
    tdf = df[target_filter]

    tdf = tdf[['재무제표종류', '보고서종류', '항목명', '당기 1분기 3개월', '당기 1분기 누적', '당기 반기 3개월', '당기 3분기 3개월', '당기', '결산기준일']].sort_values('결산기준일')
    
    #display(tdf)
    
    return tdf

def get_quarter_fin(tdf):
    target_dic = {}
    year_val = 0
    for i, row in tdf.iterrows():
        val = np.nan
        if row.보고서종류 == '1분기보고서':            
            if pd.isnull(row['당기 1분기 3개월']):
                if pd.isnull(row['당기 1분기 누적']) == False:
                    val = int(row['당기 1분기 누적'].replace(',',''))
            else:
                val = int(row['당기 1분기 3개월'].replace(',',''))
            year_val += val
            target_dic[row['결산기준일']] = val
            
        elif row.보고서종류 == '반기보고서':
            if pd.isnull(row['당기 반기 3개월']) == True:
                continue
            else:
                val = int(row['당기 반기 3개월'].replace(',',''))
                year_val += val
                target_dic[row['결산기준일']] = val
                
        elif row.보고서종류 == '3분기보고서':
            if pd.isnull(row['당기 3분기 3개월']) == True:
                continue
            else:
                val = int(row['당기 3분기 3개월'].replace(',',''))
                year_val += val
                target_dic[row['결산기준일']] = val
                
        elif row.보고서종류 == '사업보고서':
            if pd.isnull(row['당기']) == True:
                continue
            else:
                val = int(row['당기'].replace(',',''))
                val -= year_val
                year_val = 0
                target_dic[row['결산기준일']] = val

    tSeries = pd.Series.from_array(target_dic)
    tSeries.index = pd.to_datetime(tSeries.index)  

    for i in range(len(tSeries)):
        if tSeries.index[i].month == 3:
            break
    tSeries = tSeries.iloc[i:]

    return tSeries

def get_quarter_fin_list(df, company, kind_code):
    df_kind = get_target_kind_by_code(df, company, kind_code)
    
#     display(df_kind)
    
    tdf = None
    for _, row in df_kind.iterrows():
        kind_kind = row[0]
        kind_name = row[1]

        if tdf is None:
            tdf = get_target_df(df, company, kind_kind, kind_name)
        else:
            tdf = tdf.append(get_target_df(df, company, kind_kind, kind_name))
    
    if tdf is None:
        return []
    
#     display(tdf)
    tdf = tdf.sort_values('결산기준일')
    tdf = tdf.drop_duplicates(['결산기준일'])
    
    ts_list = []    
    ts = get_quarter_fin(tdf)
    ts_list.append(ts)
    
    return ts_list

def show_quarter_fin(df, company, kind_code, show=True):
    # 모든 해당 항복의 데이터 리스트 받아오기
    ts_list = get_quarter_fin_list(df, company, kind_code)
    
    if len(ts_list) == 0:
        return
    
    target_series = None

    for ts in ts_list:
        if target_series is None:
            target_series = ts
        else :
            target_series = target_series.append(ts)    

    target_series = target_series.sort_index()
    target_series.name = kind_code
    
    if show==True:
        plt.xticks(rotation=45)
        plt.plot(target_series, 'bo-')
        plt.title(company + ',' + kind_code)
        plt.show()
    
    return target_series

def cal_year_growth(data):
    tre = data.rolling(4, min_periods=4).sum().dropna()
    return ((tre.iloc[-1] / tre.iloc[0])**(4/len(tre)) - 1)*100

def show_Vchart(data1, data2, rolling=True):
    if rolling == True:
        tdf = pd.DataFrame(data1.rolling(4, min_periods=4).sum())
        tdf = pd.concat([tdf, data2.rolling(4, min_periods=4).sum()],axis='columns')
    else:
        tdf = pd.DataFrame(data1)
        tdf = pd.concat([tdf, data2],axis='columns')
    tdf.columns=[data1.name, data2.name]

    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_ylabel(data1.name, color=color)
    lns1 = ax1.plot(tdf[data1.name], '-ro', label=data1.name)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.tick_params(axis='x', rotation=90)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel(data2.name, color=color)  # we already handled the x-label with ax1
    lns2 = ax2.plot(tdf[data2.name], '-bo', label=data2.name)
    ax2.tick_params(axis='y', labelcolor=color, rotation=90)
    ax2.tick_params(axis='x', rotation=90)

    lns = lns1+lns2
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()

def show_two(oi,pr):
    uk = 100000000
    fig, ax1 = plt.subplots()
    oi = (oi/uk).rolling(4, min_periods=4).sum()
    pr = (pr/uk).rolling(4, min_periods=4).sum()
    ax1.plot(oi, 'o-')
    ax1.plot(pr, 'o-')
    fig.tight_layout()
    ax1.legend()
    ax1.tick_params(axis='x', rotation=90)
    plt.show()


def get_fin(corp_code, bgn_de='20200101'):
    api_key='594f236d3b7d44d17e2d2b481e785af41fbf0c15'
    dart.set_api_key(api_key=api_key)

    reports = dart.filings.search(corp_code=corp_code, bgn_de=bgn_de)

    for report in reports:
        if (report.report_nm.find('매출액또는손익구조') != -1):
            tpage = report.pages[0]
            html= tpage.html
            bs = BeautifulSoup(html, 'html.parser')

            tlist = bs.find_all('span', {'class':'xforms_input'})
            매출액 = tlist[1].text
            영업이익 = tlist[5].text
            당기순이익 = tlist[13].text
            자산 = tlist[18].text
            부채 = tlist[20].text
            자본총계 = tlist[22].text
            코멘트 = tlist[26].text
            
            return {'매출액':매출액, '영업이익':영업이익, '당기순이익':당기순이익, '자산':자산, '부채':부채, '자본총계':자본총계, '코멘트':코멘트}