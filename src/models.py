from flask import Flask, redirect, render_template, request
from data import matter,type
import data
import jieba

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
        data_result = data.session.query(matter.id,matter.day,matter.start_time,matter.finish_time,matter.event,matter.level,)\
                    .filter(matter.acc == acc,matter.event == cut_keyword).all()
        data_result = lamba(data_result,data_result,headers)
        search_result.append(data_result)
    search_result = search_result[0]
    return search_result

def cut_types(input,acc,headers):#模糊搜索
    search_result = [] 
    cut_keywords = jieba.lcut_for_search(input) 
    for cut_keyword in cut_keywords:
        cut_keyword,*cut_keywords = cut_keywords
        data_result = data.session.query(type.id,type.type,type.level,type.acc)\
                    .filter(type.acc == acc,type.type == cut_keyword).all()
        data_result = lamba(data_result,data_result,headers)
        search_result.append(data_result)
    search_result = search_result[0]
    return search_result
