from flask import Flask, redirect, render_template, request
from data import SQLManager
import jieba

db = SQLManager()


def cal_add(a, b=0):#类型转换
    return a+b


def check_login(input_acc =None):#检查登录
    result_acc = 1
    if input_acc == None:
        login_error ="登陆超时"
        result_acc = 0
        return login_error
    else:
        return result_acc


def lamba(input1,input2,headers):#渲染
    input1 = list(input1)
    input2 = list(map(lambda e: dict(zip(headers, e)), input2))
    return input2


def cut_search(input,acc,headers):#模糊搜索
    search_result = [] 
    cut_keywords = jieba.lcut_for_search(input) 
    for cut_keyword in cut_keywords:
        cut_keyword,*cut_keywords = cut_keywords
        data_result = db.get_list2("select * from matter where event = "," and acc = ",cut_keyword,acc)
        data_result = lamba(data_result,data_result,headers)
        search_result.append(data_result)
    search_result = search_result[0]
    return search_result

def cut_types(input,acc,headers):#模糊搜索
    search_result = [] 
    cut_keywords = jieba.lcut_for_search(input) 
    for cut_keyword in cut_keywords:
        cut_keyword,*cut_keywords = cut_keywords
        data_result = db.get_list2("select * from type where type = "," and acc = ",cut_keyword,acc)
        data_result = lamba(data_result,data_result,headers)
        search_result.append(data_result)
    search_result = search_result[0]
    return search_result
    
class developer(object):
    def __init__(self) -> None:
        pass

    def d_print(self, mode, input):
        if mode == "On":
            print(input)
        else:
            pass