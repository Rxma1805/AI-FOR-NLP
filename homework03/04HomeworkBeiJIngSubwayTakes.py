import pandas as pd
import chardet
from collections import defaultdict
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)
#设置value的显示长度为100，默认为50
pd.set_option('max_colwidth',100)

def get_station_connection(line_2_station_dic):
    station_connect=defaultdict(list)
    for station_lines in line_2_station_dic:
        station_line_list = line_2_station_dic[station_lines]
        for index, station in enumerate(station_line_list):
            if index == 0:
                station_connect[station].append(station_line_list[index + 1])
            elif index == len(station_line_list) - 1:
                station_connect[station].append(station_line_list[index - 1])
            else:
                station_connect[station].append(station_line_list[index - 1])
                station_connect[station].append(station_line_list[index + 1])
    return station_connect

def get_min_takes(counts):
    return len(counts)

def get_max_takes(counts):
    return -len(counts)

def default_takes(count):
    return  count

def is_goal(dest):
    def _w(current):
        return current[-1] == dest
    return _w

def is_goal_and_passby_specific(dest,specific):
    def _w(current):
        if (current[-1] == dest) :
            if specific in current:
                return  True
            else:
                current.pop()
                return False

    return _w

def get_successor():
    pass

def strategy(func):
    def _w(path):
        return sorted(path, key=func)
    return _w

def BFS_search(start,goal_func,sort_func=lambda x:x):
    #result=[]
    pathes = [[start]]
    seen=set()
    while pathes:
        path = pathes.pop(0)
        fronter =path[-1]

        if fronter in seen:
            continue
        for station in station_connect[fronter]:
            if station in path:
                continue
            new_path =  path+[station]

            if goal_func(new_path):
                return new_path
                #result.append(new_path)
            pathes.append(new_path)
        #pathes.append(path)
        pathes = sort_func(pathes)
        seen.add(fronter)
    return #result

def DFS_search(start,goal_func,sort_func=lambda x:x):
    #result=[]
    pathes = [[start]]
    seen=set()
    while pathes:
        path = pathes.pop()
        fronter =path[-1]
        if fronter in seen:
            continue
        for station in station_connect[fronter]:
            if station in path:
                continue
            new_path =  path+[station]
            if goal_func(new_path):
                return new_path
                #result.append(new_path)
            pathes.append(new_path)
        #pathes.append(path)
        pathes = sort_func(pathes)
        seen.add(fronter)
    return #result



with open('./BeiJingStation.csv','rb') as f:
    ff= chardet.detect(f.read())
    encod = ff['encoding']

data_path = '''./BeiJingStation.csv'''
df = pd.read_csv(data_path,encoding =encod)

line_2_station_dic = defaultdict(list)
df.apply(lambda row: (line_2_station_dic[row['line']].append(row['station'])), axis=1)
station_connect=get_station_connection(line_2_station_dic)
print(BFS_search('西直门','北京站',sort_path,get_min_takes))
import networkx as nx
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.figsize'] = (16, 9)
plt.rcParams['savefig.dpi'] = 120 #图片像素
plt.rcParams['figure.dpi'] = 120
plt.figure()
graph = nx.Graph(station_connect)
graph.add_nodes_from(station_connect.keys())
nx.draw(graph,with_labels=True,size='10')
plt.show()
plt.savefig('1.jpg')


print(BFS_search('燕山',goal_func=is_goal('2号航站楼'),sort_func=strategy(get_min_takes)))
print(DFS_search('燕山',goal_func=is_goal('2号航站楼'),sort_func=strategy(get_min_takes)))
print(BFS_search('燕山',goal_func=is_goal_and_passby_specific('2号航站楼','北京西站'),sort_func=lambda x:x))

print(BFS_search('燕山',goal_func=is_goal('六里桥'),sort_func=lambda x:x))
print(DFS_search('燕山',goal_func=is_goal('六里桥'),sort_func=lambda x:x))
print(BFS_search('燕山',goal_func=is_goal_and_passby_specific('六里桥','西局'),sort_func=lambda x:x))
#[['燕山', '房山城关', '饶乐府', '马各庄', '大石河东', '星城', '阎村', '紫草坞', '阎村东', '苏庄', '良乡南关', '良乡大学城西', '良乡大学城', '良乡大学城北', '广阳城', '篱笆房', '长阳', '稻田', '大葆台', '郭公庄', '丰台科技园', '科怡路', '丰台南路', '丰台东大街', '七里庄', '六里桥'], ['燕山', '房山城关', '饶乐府', '马各庄', '大石河东', '星城', '阎村', '紫草坞', '阎村东', '苏庄', '良乡南关', '良乡大学城西', '良乡大学城', '良乡大学城北', '广阳城', '篱笆房', '长阳', '稻田', '大葆台', '郭公庄', '丰台科技园', '科怡路', '丰台南路', '丰台东大街', '七里庄', '西局', '六里桥']]
#[['燕山', '房山城关', '饶乐府', '马各庄', '大石河东', '星城', '阎村', '紫草坞', '阎村东', '苏庄', '良乡南关', '良乡大学城西', '良乡大学城', '良乡大学城北', '广阳城', '篱笆房', '长阳', '稻田', '大葆台', '郭公庄', '丰台科技园', '科怡路', '丰台南路', '丰台东大街', '七里庄', '六里桥'], ['燕山', '房山城关', '饶乐府', '马各庄', '大石河东', '星城', '阎村', '紫草坞', '阎村东', '苏庄', '良乡南关', '良乡大学城西', '良乡大学城', '良乡大学城北', '广阳城', '篱笆房', '长阳', '稻田', '大葆台', '郭公庄', '丰台科技园', '科怡路', '丰台南路', '丰台东大街', '七里庄', '西局', '六里桥']]
#[['燕山', '房山城关', '饶乐府', '马各庄', '大石河东', '星城', '阎村', '紫草坞', '阎村东', '苏庄', '良乡南关', '良乡大学城西', '良乡大学城', '良乡大学城北', '广阳城', '篱笆房', '长阳', '稻田', '大葆台', '郭公庄', '丰台科技园', '科怡路', '丰台南路', '丰台东大街', '七里庄', '西局', '六里桥']]

print(BFS_search('平安里',goal_func=is_goal('安定门'),sort_func=strategy(get_min_takes)))
print(BFS_search('平安里',goal_func=is_goal_and_passby_specific('安定门','南锣鼓巷'),sort_func=strategy(get_min_takes)))
#[['平安里', '新街口', '西直门', '积水潭', '鼓楼大街', '安定门']]
#[['平安里', '北海北', '南锣鼓巷', '东四', '张自忠路', '北新桥', '雍和宫', '安定门']]













# def search(start,dest,sort_func):
#     if start not in station_2_line_dic:
#         return
#     station_2_line_dic[start]

