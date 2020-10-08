# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 11:40:34 2020

@author: whyang
"""

import jieba
import jieba.analyse
import jieba.posseg as pseg

jieba.set_dictionary('dict.txt.big')

content = sentence = '氣候變遷被視為是全球作物生長及生產的最重要關鍵議題。有關氣候變遷關注的因素為氣溫、濕度及大氣二氧化碳濃度的提升。氣候變遷會影響病蟲害生物學特性、分布、社群組成及生態動態等。本計畫擬赴日本農業研究機構研習有關氣候變遷對於水稻及果樹類病蟲害分布範圍位移、評估技術及預警作為等議題，以協助國內因應氣候變遷採取必要的作為。'

print("Input：", sentence)
words = pseg.cut(sentence)

#words = jieba.cut(sentence, cut_all=False)

print("Output 精確模式 Full Mode：")
for word in words:
    if word.flag == 'n':
        print(word.word, word.flag)
        

tags = jieba.analyse.extract_tags(content) #, 20)

print("Output：")
print(", ".join(tags))

print(jieba.analyse.extract_tags(content, withWeight=False, allowPOS=())) #'n' , 'vn' , 'v'))) #topK=20 
for x, w in jieba.analyse.extract_tags(content, withWeight=True, allowPOS=()): #'ns' , 'n' , 'vn' , 'v')):
    print('%s %s' % (x, w))
    
print(jieba.analyse.textrank(content,  withWeight=False, allowPOS=())) #'n' , 'vn' , 'v')))
for x, w in jieba.analyse.textrank(content, withWeight=True, allowPOS=()): #'ns' , 'n' , 'vn' , 'v')):
    print('%s %s' % (x, w))
