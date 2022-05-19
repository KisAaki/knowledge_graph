#-*- enccoding:UTF-8 -*-

import csv
import pandas
import jieba
from py2neo import Graph,Node,Relationship,NodeMatcher
if __name__ == "__main__":


    #with open('hobbies.csv') as f:
        #data = [record for record in csv.DictReader(f)]
    #g = Graph('http://localhost:7474', user='test1', password='123456')
    g = Graph('http://localhost:11003', auth = ("neo4j", "123456"))
    datas = pandas.read_csv(".\hobbies.csv", encoding="gbk")
    print(type(datas))
    #print(datas)
    special_characters =[",", "，", ".", "\\", ";"]
    arr = []
    for index,row in datas.iterrows():
        #print(row["hobbies"])
        row.iloc[2] = row["hobbies"].replace(",", "，")
        row.iloc[2] = row["hobbies"].replace(" ", "，")
        row.iloc[2] = row["hobbies"].replace("、", "，")

        row.iloc[2] = row["hobbies"].split("，")
        arr += [x for x in row.iloc[2] if x != ""]
        #print(row["hobbies"])
        datas.iloc[index] = row     #对原数据进行修改
        # print("index:",index)
        # row.iloc[2] = jieba.lcut(row["hobbies"])
        # print(row["hobbies"])
        # print()
    #arr.remove("\\n")
    #print(arr)
    #print(arr[113])
    my_dict = { "Id":[i for i in range(len(arr))]
                ,"Name": arr}
    #df = pandas.DataFrame(my_dict)
    #df.to_csv("test.csv",encoding='utf_8_sig', index = False)
    result_df = pandas.read_csv("testout.csv", encoding="utf-8")
    cluster_id_dict = {}
    #创建字典，方便查找
    for index, row in result_df.iterrows():
        key = row["Cluster ID"]
        value = row["Name"]

        if key in cluster_id_dict.keys():
            cluster_id_dict[key].add(value)
        else:
            cluster_id_dict[key] = set()
            cluster_id_dict[key].add(value)
    print(cluster_id_dict)


    used_id = []
    for index, row in datas.iterrows():
        name = row["name"]
        id = row["id"]
        name_node = Node("Person", name=name)
        g.create(name_node)
        #暂时不存储 id_node（学号）
        # id_node = Node("A", name=id)
        # g.create(id_node)
        # re = Relationship(name_node, "学号", id_node)
        # g.create(re)
        for hobby in row["hobbies"]:
            temp_cluster_id = -1
            for key, value in cluster_id_dict.items():
                if hobby in value:
                    temp_cluster_id = key
                    if temp_cluster_id in used_id:    #之前已经用过
                        hobby = list(value)[0]                                        #统一使用第一个元素
                    else:                                                       #没用过
                       used_id.append(key)
                    break                             #找到即只有一个，跳出

            hobby_node = Node("Hobby", name=hobby)
            g.create(hobby_node)
            re = Relationship(name_node, "LIKES", hobby_node)
            g.create(re)