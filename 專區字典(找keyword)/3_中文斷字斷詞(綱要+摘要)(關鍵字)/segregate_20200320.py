# -*- coding: utf-8 -*-

"""
Created on Tue Mar 19, 2020
@author: whyang

過濾農委會三平台上有關於氣候變遷的計畫名稱列表(一共510筆計畫名稱)，拆解每個計畫的中文摘要、綱要，其對應的關鍵字(群組) 
"""
###
# USAGE (example of command)
# python inspect.py -n 專案名稱 (e.g., 因應氣候變遷調適作物病蟲害管理模式之研究) 
##
import os
import argparse
import pandas as pd
import numpy as np

import jieba
import jieba.analyse
import jieba.posseg as pseg
        
#####################
# declare functions #
#####################
##
# remove leading and trailing characters of each value across all cells in dataframe
def trim_all_cells(df):
    # trim whitespace from ends of each value across all series in dataframe
    trim_strings = lambda x: x.strip() if isinstance(x, str) else x
    return df.applymap(trim_strings)
##
# 查詢 element 在 List object 中的位置指標 
def getIndexPositions(listOfElements, element):
    ''' Returns the indexes of all occurrences of give element in
    the list- listOfElements '''
    indexPosList = []
    indexPos = 0
    while True:
        try:
            # Search for item in list from indexPos to the end of list
            indexPos = listOfElements.index(element, indexPos)
            # Add the index position in list
            indexPosList.append(indexPos)
            indexPos += 1
        except ValueError as e:
            break
    return indexPosList

###
# main program
#
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
    
    # main process
    with open(datapath+'\\training_data_ext_1.csv', 'r', encoding='utf-8', newline='') as csvfile: # kw_data.csv
        # read into 訓練資料表格 510*1217 (510筆計畫(氣候變遷有關)，一共對應出1,217個關鍵字)
        df = pd.read_csv(
                csvfile,
                header = None,
                #prefix = 'x_',
                verbose = True,
                skip_blank_lines = True)
        
        # remove leading and tailing white space of string (content of cell in dataframe)
        trim_all_cells(df)
    
        # 抓出所有的'專案名稱'、'關鍵字'(欄位名稱)
        # data structure is used as list structure (converted from dataframe)
        proj_names = df.loc[1:, 0].tolist() # column 0: presents all projects' names
        col_names = df.loc[0, :].tolist() # row 0: presents all columns' names w.r.t the csv table (dataframe)
    
        ##
        # 1. 處理一筆計畫資料 
        name = args['name'] #'因應氣候變遷調適作物病蟲害管理模式之研究'
        if name in proj_names:
            print('專案名稱 = ', name ,' exist')
            # 找到 name 對應在 dataframe table的位置(第幾列)
            i = getIndexPositions(proj_names, name)
            # 取出 name 對應的列的所有column的值 (， 
            # convert to list structure
            col_data = df.loc[i[0]+1, :].tolist()
            # 找出 name 對應的列的所有column的值為'1'的位置(找到所有相對應的關鍵字)
            indexPosList = getIndexPositions(col_data, '1')
            print(indexPosList)
            # 取出每個關鍵字的欄位名稱
            for j in indexPosList:
                print(col_names[j])
        else:
            print('專案名稱 = ', name ,' doesn\'t exist')
    
        ##
        # 2. 根據目前csv table的所有專案名稱(一共510筆)，處理全部個筆對應的關鍵字，並output成 kw_table.csv 檔案 
        # declare dataframe structure used by kw_table.csv
        df_table = pd.DataFrame(columns=('專案名稱', '關鍵字 號碼', '關鍵字', '綱要名稱', '綱要名稱(關鍵字)', '中文摘要', '中文摘要(關鍵字)'))    
        _index = 0 # counter of 專案名稱 (from 0 to 510)    
        #
        jieba.set_dictionary('dict.txt.big') # 使用斷詞詞庫切換到 dic.txt.big 這個檔案
        jieba.load_userdict('kw_def.txt') # 使用自定義詞典
        jieba.analyse.set_stop_words('stop_words.txt') # file_name為自定義語料庫的路徑關鍵詞提取所使用停止詞（Stop Words）文字語料庫可以切換成自定義語料庫的路徑
        #
        for name in proj_names:
            # fill in column '專案名稱' of dataframe
            df_table.loc[_index, '專案名稱'] = name # name is a string object
            print('專案名稱 = ', name, ' exist')
        
            # fill in column '關鍵字 號碼' of dataframe
            i = getIndexPositions(proj_names, name) # 專案名稱對應到那一列 (kw_data.csv)
            col_data = df.loc[i[0]+1, :].tolist() # 抓出 對應的整列資料 (關鍵字); i[0]+1 because counter begins from 1 w.r.t. project_name
            indexPosList = getIndexPositions(col_data, '1') # 找出 有被標註的關鍵字(有使用為'1')
            #fullStr = ''
            #fullStr = ' '.join(indexPosList)
            df_table.loc[_index, '關鍵字 號碼'] = indexPosList
            print(indexPosList)
        
            # fill in column '關鍵字' of dataframe
            kw_list = []
            for k in indexPosList:
                kw_list.append(col_names[k]) # 取出對應的關鍵字(欄位名稱)
                print(col_names[k])
            # 將list structure轉成 string, 並用','分隔每個使用的關鍵字
            fullStr = ''
            fullStr = ', '.join(kw_list)
            df_table.loc[_index,'關鍵字'] = fullStr #kw_list
                
            ##
            # 3. conduct parsing 中文摘要 and extracting top-10 keywords       
            #for name in proj_names:
            
            #i = getIndexPositions(proj_names, name)
            j = getIndexPositions(col_names, '[綱要名稱]')
            content = df.loc[i[0]+1, j[0]]
            print('綱要名稱= ', content)
            kw_list = []
            if pd.notna(content):
                 for x, w in jieba.analyse.extract_tags(content, withWeight=True, allowPOS=(), topK=5): 
                     kw_list.append(x)
            print('綱要名稱: ',kw_list)
            # fill in column '綱要名稱' of dataframe
            fullStr = ''
            fullStr = ', '.join(kw_list)
            df_table.loc[_index,'綱要名稱'] = content
            df_table.loc[_index,'綱要名稱(關鍵字)'] = fullStr          
            
            j = getIndexPositions(col_names, '[中文摘要]')
            content = df.loc[i[0]+1, j[0]]
            df_table.loc[_index,'中文摘要'] = content
            kw_list = []
            if pd.notna(content):
                for x, w in jieba.analyse.extract_tags(content, withWeight=True, allowPOS=('vn', 'n')):
                    if w >= 0.4:
                        kw_list.append(x)
                        #print('%s %s' % (x, w))
            print('中文摘要: ',kw_list)
            # fill in column '中文摘要' of dataframe
            df_table.loc[_index,'中文摘要'] = content
            fullStr = ''
            fullStr = ', '.join(kw_list)
            df_table.loc[_index,'中文摘要(關鍵字)'] = fullStr   
            
            print('-------')                
            # increase counter
            _index += 1
    
        # output results to kw_table.csv 檔案 
        df_table.to_csv(datapath+'\\kw_table.csv', index=False, encoding='cp950') # mode='a' for append mode if needs             
###############
# End of File #
###############            
        
 