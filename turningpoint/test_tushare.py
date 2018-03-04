# -*- coding: utf-8 -*-
import tushare as ts
import pandas as pd
import numpy as np

import os


BASE_FOLDER='E:\\tushare\\'
DOWNLOAD_BASE_FOLDER='E:\\tushare\\download\\'
CSV_REPORT_DATA_S2='E:\\tushare\\download\\report_data_2017_S2.csv'
CSV_REPORT_DATA_S1='E:\\tushare\\download\\report_data_2017_S1.csv'

def get_list_from_file():
    f=open('data/tushare_temp.data', 'r')

    #stocks_list=[]
    #for l in f.readlines():
    #    stocks_list.append(l)

    #stocks_list=f.read().split('\n')
    #stocks_list.pop()

    #stocks_list = list(map(lambda x: x.replace('\n',''), f.readlines()))
    return list(map(lambda x: x.replace('\n',''), f.readlines()))


def get_pe(l):
    pe = ts.get_stock_basics()
    #pe.set_index(ascending=True)
    #return pe.index
    #return pe['code']
    #return pe.dtypes
    #return pe.columns


    pe['code']=list(map(lambda x: int(str(x)), pe.index))
    #pe['code']=pe.apply(int(str(pe.index)))
    return pe[pe['code'].isin(l)]

def get_roe(l):
    S2 = pd.read_csv(CSV_REPORT_DATA_S2, encoding='gbk')
    roeS2=S2[S2['code'].isin(l)]
    S1 = pd.read_csv(CSV_REPORT_DATA_S1, encoding='gbk')
    roeS1=S1[S1['code'].isin(l)]

    frames = [roeS2, roeS1[~roeS1['code'].isin(roeS2['code'])]]
    roe = pd.concat(frames)
    #.drop_duplicates()
    #.duplicated()
    #IsDuplicated = roe.duplicated(['code'])
    roe=roe.drop_duplicates(['code'])

    return roe

def save_report_data():
    """
    tushare: save_report_data
    """
    report = ts.get_report_data(2017,2)
    report.to_csv(CSV_REPORT_DATA_S2)

    report = ts.get_report_data(2017,1)
    report.to_csv(CSV_REPORT_DATA_S1)


def get_k_data():
    """
    tushare: get_k_data
    """

    s0 = ts.get_k_data(code='600622', start='2010-07-01', end='2010-07-02')
    all_s = s0

    #print(all_s)

    for s_code in ['600622','600133','000036','002285','601155','000628','600503',\
    '600696','600064','600848','000567','600675','000043','600077','600240','000609','002314','000517',\
    '000861','600095','600225','000056','000514','600173','000040','000718','600067','600082','000573',\
    '600638','002147','600823','600510','600641','000014','002818','000667','000608','000809','600208',\
    '600223','600716','002133','000918','600708','600895','000029','000031','000506','000620','000838',\
    '000926','002244','600239','600246','600565','600657','600724','600732','600733','600890','000656',\
    '000002','000863','600736','600658','600533','600215','000005','000631','600383','000979','000671',\
    '600466','600807','600162','600376','000042','600007','600048','600743','002077','000505','600094',\
    '600052','600159','600325','001979','000046','600639','600648','600393','600113','002208','600748',\
    '600649','000668','002016','000534','000797','000691','000006','000011','000402','600185','600463',\
    '600266','601588','600665','000736','600606','000931','000732','000897','600568','600621','600773',\
    '600791','000616','000537','002305','600322','000965','600340','000981','600684','600683','600663',\
    '002146','600604','000615']:
        s1 = ts.get_k_data(code=s_code, start='2010-07-01', end='2010-07-02')
        frames = [s1, all_s]
        all_s = pd.concat(frames)

    print(all_s)
    filename = BASE_FOLDER + '20100701-02.csv'
    all_s.to_csv(filename)


def get_stock_basics():

    pe = ts.get_stock_basics()
    #print(type(pe))
    pe.set_index(ascending=True)
    print(pe)
    #pure_pe = pe[['code','pe']]

#def get_report_data():
    roeS2 = ts.get_report_data(2017,2)
    roeS1 = ts.get_report_data(2017,1)
    frames = [roeS2, roeS1]
    roe = pd.concat(frames)

    pure_roe = roe[['code','roe']]
    #print(roe)

    roe_pe=pd.merge(pe,pure_roe,how='outer')
    print(roe_pe)


def save_to_csv():
    filename = BASE_FOLDER + 'roe_pe.csv'
    roe_pe.to_csv(filename)


def simple():


    filename = 'E:\tushare\2017S2.csv'
    df = ts.get_report_data(2017,2)

    if os.path.exists(filename):
        df.to_csv(filename, mode='a', header=None)
    else:
        df.to_csv(filename)

    #exit(0)
    csv = pd.read_csv("E:\tushare\simple.csv")
    #print(data_x)

    #np_csv = np.array(csv)
    #code_list = np_csv.tolist()

    code_list = csv.code.tolist()
    print(code_list)
    print(type(code_list))

    str_code_list = list(map(lambda x: str(x), code_list))
    print(str_code_list)
    print(type(str_code_list))

    df = ts.get_report_data(2017,1)

    idx_for_df = df['code'].isin(code_list)

    df_final = df[idx_for_df]
    print(df_final)

    #print(type(df))
    #print(df[['code','name','roe']][(df.code>'299000') & (df.code<'301000') & (df.roe>10)])
    print(df_final[['code','name','roe']].sort_index(by=['roe'], ascending=0))

    df = ts.get_realtime_quotes('601988')
    print(df)
    print(df[['code','name','price','bid','ask','volume','amount','time']])





if __name__ == '__main__':

    #df = ts.get_k_data("399005", ktype="D", index=True, start="2017-10-16", end="2017-10-17")
    #df = ts.get_k_data("300088", ktype="D", start="2016-10-16", end="2017-10-17")
    df = ts.get_stock_basics()
    print(df)
    exit()

    stocks_list=get_list_from_file()
    df_pe=get_pe(stocks_list)

    df_roe=get_roe(stocks_list)
    df_roe = df_roe[['code','roe']]

    df_roe_pe=pd.merge(df_pe, df_roe, on='code', how='outer')

    df_pe.to_csv(BASE_FOLDER + '20170817_pe.csv')
    df_roe.to_csv(BASE_FOLDER + '20170817_roe.csv')
    df_roe_pe.to_csv(BASE_FOLDER + '20170817_roe_pe.csv')
    print('GN')





#end
