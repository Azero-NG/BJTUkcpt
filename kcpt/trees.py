import requests
import re
import os

s_headers=''
s=''
class tree:
    def __init__(self, l, name, d_f):
        self.children = []
        self.link = l
        self.dir_file = d_f  # 0:dir 1:file
        self.parent = None
        self.name = name
        self.download_list = [] # link ,name,path,dir
    def add_child(self,child):
        self.children.append(child)

    def show(self, index=""):
        print(self.name)
        for ind, x in enumerate(self.children):
            print(index, end="")
            if ind == len(self.children) - 1:
                print("└── ", end="")
                x.show(index+"    ")
            else:
                print("├── ", end="")
                x.show(index+"│   ")
            # print(x.link+"├── "+self.name+" "+"dir" if (x.dir_file == 2) else "file")

    def add_to_download_list(self, path, download_list):
        d_l = []
        d_l.append(self.link)
        d_l.append(self.name)
        d_l.append(path)
        d_l.append(self.dir_file)
        download_list.append(d_l)
        if self.dir_file == 0:
            for x in self.children:
                x.add_to_download_list(path+self.name+'/',download_list)


    def find_child(self):  # s:有访问权限的账号
        d = s.get(self.link)
        # 文件夹
        result = re.findall(r'(listview.jsp\?acttype=enter&folderid=.*?&lid=.*?)" title="">(.*)</a>', d.text)
        for j in result:
            child = tree("http://cc.bjtu.edu.cn:81/meol/common/script/"+j[0], j[1], 0)
            child.find_child()
            self.add_child(child)

        # 文件
        result = re.findall(r'preview/download_preview.jsp\?(fileid=.*?&resid=.*?&lid=[0-9]*)" target="_blank"\s*?title="">(.*)</a>', d.text)
        for j in result:
            child = tree("http://cc.bjtu.edu.cn:81/meol/common/script/download.jsp?"+j[0], j[1], 1)
            self.add_child(child)

def download_list(i):
    if i[3] == 0:
        path = i[2]+i[1]
        if not(os.path.exists(path)):

            os.makedirs(i[2]+i[1])
    else:
        if not(os.path.exists(i[2])):
            os.makedirs(i[2])

        with s.get(i[0], stream=True, headers=s_headers) as r:
            i[1] = re.findall('"(.*)"', r.headers['Content-Disposition'].encode('latin1').decode('gbk'))[0]
            if os.path.isfile(i[2] + i[1]):
                return
            chunk_size = 10240 # 单次请求最大值
            content_size = int(r.headers['content-length'])
            if content_size > 102400000*3:
                print(i[1]+'下载完成')
            else:
                with open(i[2]+i[1], "wb") as file:
                    k=0
                    for data in r.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        k+=chunk_size
                        #print('%lf%%'%(k/content_size*100),end='\r',flush=True)
        print(i[1]+'下载完成')