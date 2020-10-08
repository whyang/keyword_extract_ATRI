# -*- coding: utf-8 -*-
"""
Created on Apr. 24, 2020
@author: whyang

農委會科技處成果網，三平台整合查詢系統，專區_氣候變遷，查詢使用之關鍵字字典
1.根據主要關鍵字(核心字彙)、延伸關鍵字(領域應用字彙)兩個部份已經過濾出的關鍵字table(.csv): 關鍵字欄位、(綱要名稱、中文摘要)斷詞斷句之關鍵字
2.主要關鍵字(核心字彙):關鍵字欄位，進行feature selection(or correlation)，生成'核心字彙'字典
3.延伸關鍵字(領域應用字彙):(綱要名稱、中文摘要)斷詞斷句之關鍵字，進行feature selection(or correlation)，生成'領域應用字彙'字典
Input: 
    1. train_data_kw_raw.csv (氣候變遷訓練資料_500+筆，關鍵字列表)
Output: 
    1.climate_change_kw_core.csv ('核心字彙'字典檔案)
    2.climate_change_kw_extend.csv ('領域應用字彙'字典檔案)
"""

###
# USAGE (example of command)
# python queryFeature_20200423.py -n 因應氣候變遷調適作物病蟲害管理模式之研究 (專案名稱) 
##

#importing libraries
import os
import argparse
import pandas as pd
#import numpy as np
#import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

'''
import statsmodels.api as sm

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import RFE
from sklearn.linear_model import RidgeCV, LassoCV, Ridge, Lasso
'''
#####################
# declare functions #
#####################
##
# remove leading and trailing characters of each value across all cells in dataframe
def trim_all_cells(df):
    # trim whitespace from ends of each value across all series in dataframe
    trim_strings = lambda x: x.strip() if isinstance(x, str) else x
    return df.applymap(trim_strings)


################
# main program #
################

if __name__ == '__main__':
    ##
    # config command for 
    ap = argparse.ArgumentParser()
    ap.add_argument('-n', '--name', required=True, help='project name')
    args = vars(ap.parse_args())
    
    # initialize variable
    datapath = '.\\data'  # directory of input data folder 
    if not os.path.isdir(datapath):
        os.mkdir(datapath)

    ##
    # step 1: 建購主要關鍵字(核心字彙)
    #
    
    # 讀入training dataset: 已經標註過與'氣候變遷'有關的資料庫內資料(以'專案名稱'為主，對應原始資料內'關鍵字'欄位內所收納的所收納內容
    # 原始資料 [專案名稱]、[關鍵字]... : 經過轉換成mapping table (context 1 表示該關鍵字有被使用/標註在對應的專案，反之為 0)
    with open(datapath+'train_data_kw_raw.csv', 'r', encoding='utf-8', newline='') as csvfile:
        df = pd.read_csv(csvfile,
                         header = 0,
                         verbose = True,
                         skip_blank_lines = True)
        
        X = df.drop('[專案名稱]', 1) # Feature Matrix
        df['label'] = 1
        y = df['label'] # Target Variable
        X_new = SelectKBest(chi2, k=2).fit_transform(X, y)
        row, col = X_new.shape
        print('*** SelectKBest [{a} , {b}] '.format(a=row, b=col))