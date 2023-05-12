from data import matter,type
import data

def cal_add(a, b=0):#类型转换
    return a+b


def lamba(input1,input2,headers):#渲染
    input1 = list(input1)
    input2 = list(map(lambda e: dict(zip(headers, e)), input2))
    return input2


def cut_search(inputInfo,acc,headers):#模糊搜索
    inputInfo = "%" + inputInfo + "%"
    data_result = data.session.query(matter.id,matter.date,matter.start_time,matter.finish_time,matter.matterInfo,matter.level,)\
                    .filter(matter.matterInfo.like(inputInfo),matter.account == acc,).all()
    data_result = lamba(data_result,data_result,headers)
    return data_result

def cut_types(input,acc,headers):#模糊搜索
    inputInfo = "%" + input + "%"
    data_result = data.session.query(type.id,type.type,type.level,type.account,)\
                    .filter(type.type.like(inputInfo),matter.account == acc,).all()
    data_result = lamba(data_result,data_result,headers)
    return data_result
