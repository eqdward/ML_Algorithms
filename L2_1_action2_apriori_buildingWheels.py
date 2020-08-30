# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 10:12:42 2020

@author: yy
"""

import itertools
from collections import defaultdict

def apriori(transactions, min_support, min_confidence):
    """apriori关联规则
    输入--
        transanctions: 交易记录
        min_support: 最小支持度
        min_confidence: 最小置信度
    输出--
        frequent_itemsets: 频繁项集
        rules: 关联规则    
    """
    
    """Part 1 计算频繁项集"""
    n = len(transactions)
    
    item_list = []
    for tran in transactions:
        item_list.extend(list(tran))
    item_list = set(item_list)   # 所有的商品类目

    supports = {}
    itemsets = []
    for k in range(1, len(item_list)+1):
        for j in itertools.combinations(item_list, k):
            itemsets.append(j)
    itemsets = itemsets[::-1]   # 所有可能的项集

    while itemsets:   # 循环计算每一个可能项集的支持度
        itemset = itemsets.pop()    
        counter = 0   # 计数器，计算项集在交易中的出现次数
        for tran in transactions:
            if len(set(itemset)-set(tran)) == 0:   # 用差集来判断项集是否出现在交易中
                counter += 1
        support = counter / n   # 项集的支持度
        
        if support < min_support:   # 判断该项集是否频繁，若不是频繁项集则从所有项集结果中删除该项集的超集
            for i in itemsets:
                if len(set(itemset)-set(i)) == 0:
                    itemsets.remove(i)
        else:
            key = tuple(sorted(list(itemset)))   # 用排序元组作为key，可以解决异位
            supports[key] = counter / n
    
    frequent_itemsets = defaultdict(dict)
    for k, v in supports.items():
        frequent_itemsets[len(k)][k] = int(v*n)
    
    """Part 2 发掘关联规则"""
    rules = []
    for A, B in itertools.permutations(supports.keys(), 2):   # 基于频繁项集构建所有可能的关联规则A->B
        if len(A)>=len(B) and len(set(A)&set(B)) == 0:   # 筛选规则: 1)A为多数集，B为少数集; 2)A和B无交集
            temp = tuple((sorted(list(set(A)|set(B)))))   # 计算A和B的交集，并排序，再转为元组
            if temp in supports.keys():   # 判断temp是否为频繁项集
                confidence = supports[temp]/supports[A]
                if confidence >= min_confidence:
                    rule = str(A)+"->"+str(B)
                    rules.append(rule)
           
    return frequent_itemsets, rules

if __name__ == "__main__":
    
    transactions = [('牛奶','面包','尿布'),
                    ('可乐','面包', '尿布', '啤酒'),
                    ('牛奶','尿布', '啤酒', '鸡蛋'),
                    ('面包', '牛奶', '尿布', '啤酒'),
                    ('面包', '牛奶', '尿布', '可乐')]
    frequent_itemsets, rules = apriori(transactions, min_support=0.5, min_confidence=1)
    print("频繁项集：", frequent_itemsets)
    print("关联规则：", rules)


