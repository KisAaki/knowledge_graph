#-*- enccoding:UTF-8 -*-

import pandas
from py2neo import Graph, Node, Relationship, Subgraph, Transaction

if __name__ == "__main__":

    g = Graph('http://localhost:11003', auth=("neo4j", "123456"))
    data = pandas.read_csv("./hobbies.csv", encoding="gbk")
    print(type(data))

    special_characters =[",", "，", ".", "\\", ";"]

    for index,row in data.iterrows():
        row.iloc[2] = row["hobbies"].replace(",", "，")
        row.iloc[2] = row["hobbies"].replace(" ", "，")
        row.iloc[2] = row["hobbies"].replace("、", "，")

        row.iloc[2] = [s for s in row["hobbies"].split("，") if len(s) > 0]

        data.iloc[index] = row     # 对原数据进行修改

    result_df = pandas.read_csv("testout.csv", encoding="utf-8")

    # 创建字典, 方便查找
    id_of_hobby = {row["Name"]: row['Cluster ID'] for index, row in result_df.iterrows()}

    persons = []
    hobby_nodes_of = dict()
    relationships = []

    for index, row in data.iterrows():  # iterate each student
        student_id = row['id']
        student_name = row['name']
        student = Node('Person', id=student_id, name=student_name)
        persons += [student]
        for hobby_name in row["hobbies"]:
            # query hobby_id by hobby_name
            hobby_id = id_of_hobby[hobby_name]
            if hobby_id in hobby_nodes_of.keys():  # already created hobby node for this hobby_id
                # pickup existing hobby node by hobby_id
                relationships += [Relationship(student, 'LIKES', hobby_nodes_of[hobby_id])]
            else:
                # Create node for new encountered hobby
                t = Node('Hobby', name=hobby_name, id=hobby_id)
                hobby_nodes_of[hobby_id] = t
                # Create relationship
                relationships += [Relationship(student, 'LIKES', t)]

    nodes = persons + list(hobby_nodes_of.values())

    subgraph = Subgraph(nodes, relationships)

    tx = g.begin()
    tx.create(subgraph)
    g.commit(tx)
