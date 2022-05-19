#-*-coding:UTF-8 -*-
import pandas
# import pandas
# my_dict = {"index":[0, 1, 2]}
#
# df = pandas.DataFrame(my_dict)
# df.to_csv("output.csv")
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
print()
#print(cluster_id_dict.values())
for key,value in cluster_id_dict.items():
    if("欧洲文学") in value:
        print(key)
        print(list(value)[0])
