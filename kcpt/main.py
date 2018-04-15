#!/env/bin python3
# !coding:utf-8
import kcpt_lib
import trees
import time
from threading import Thread
from multiprocessing.dummy import Pool as ThreadPool
import threading
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

s = kcpt_lib.login(input("请输入你的用户名:"),input("请输入你的密码:"))
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
path = input('\n\n请输入保存路径\n(!!!!末尾有/号!!!!例如"./课程/")\n:')
path = "./课程/"
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
    trees.download_list(i)
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
