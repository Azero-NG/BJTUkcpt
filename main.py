#!/usr/bin/env python
#!coding:utf-8
import kcpt_lib
import trees
import time
from threading import Thread
from multiprocessing.dummy import Pool as ThreadPool
import threading
import argparse
#命令行
parser = argparse.ArgumentParser()
##metavar 每个-u,--username后面metavar,最后help
parser.add_argument('-u','--username',dest='username',required=True,help="北京交通大学mis账户",metavar="")
parser.add_argument('-p','--password',dest='password',required=True,help="北京交通大学mis账户密码",metavar="")
parser.add_argument('-o','--output',dest='outputdir',required=True,help="下载目录",metavar="")
parser.add_argument('-m','--maxsize',dest='maxsize',required=False,help="最大下载文件大小(超过则放弃下载)\n格式:{K,M,G,T,P}\n例如:xGxKxB",metavar="")
args = parser.parse_args()


######时间记录
start = time.time()
#进程池
threads = []
# 课程数据存放
lessons = []
#获取课程数据函数
def get_all(i):
    root = trees.tree(i[0], i[1], 0)
    root.find_child()
    lessons.append(root)
    print(root.name)
#登录

s = kcpt_lib.login(args.username,args.password)
trees.s = s
#获取课程数据
for i in kcpt_lib.GetLesson(s):
    t = Thread(target=get_all,args=[i])
    t.start()
    threads.append(t)
print("获取课程数据完毕")
#获取课程数据完毕
for t in threads:
    t.join()
#生成下载连接
download_list = []
path = args.outputdir
if path[-1]!='/':
    path+='/'
for root in lessons:
    root.add_to_download_list(path, download_list)
print(download_list)
#下载函数
trees.s_headers = {'Cookie':'JSESSIONID='+s.cookies.values()[0]+';'}
num = 0
sum = len(download_list)
pool = ThreadPool(20)
lock = threading.Lock()

def download(i):
    trees.download_list(i,trees.humanToByte(args.maxsize))
    lock.acquire()
    global num
    num += 1
    print('%d/%d' % (num, sum))
    lock.release()
pool.map(download,download_list)

pool.close()

pool.join()
end = time.time()
print(end-start)
