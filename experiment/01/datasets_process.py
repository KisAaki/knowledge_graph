# -*- coding=utf-8 -*-
import csv
import py2neo
import pandas
from py2neo import Graph,Node,Relationship,NodeMatcher

g=Graph('http://localhost:7474',user='neo4j',password='123456')
datas = pandas.read_csv(".\hobbies.csv", encoding="gbk")
#去掉全为 NAN 的行
datas = datas.dropna(axis=0, how = "all")
#去掉全为 NAN 的列
datas = datas.dropna(axis = 1, how = "all")
#g.delete_all()

for index,row in datas.iterrows():
    name = row["姓名"]
    print(type(name))
    hobby = row["兴趣爱好"]
    id = row["学号"]

    print("姓名是：",name)
    print("兴趣爱好是：", hobby)
    print("学号是:", id)
    name_node = Node("haha",name = name)
    g.create(name_node)

    id_node = Node("haha",name = id)
    g.create(id_node)
    re = Relationship(name_node, "学号", id_node)
    g.create(re)

    hobby_node = Node("haha",name = hobby)
    g.create(hobby_node)
    re = Relationship(name_node, "爱好", hobby_node)
    g.create(re)
