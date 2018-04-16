# BJTUKcpt
## Brief function description
BJTUKcpt lets you quickly download all your course from kcpt
## Simple introduction to program
BJTUKcpt is a script program written by python.So it depends on some python modules
### dependencies
1. python 3.6.4
2. requests 2.18
3. py-query 1.4

### How to use
```bash
usage: main.py [-h] -u  -p  -o  [-m]

optional arguments:
  -h, --help        show this help message and exit
  -u , --username   北京交通大学mis账户
  -p , --password   北京交通大学mis账户密码
  -o , --output     下载目录
  -m , --maxsize    最大下载文件大小(超过则放弃下载) 格式:{K,M,G,T,P} 例如:xGxKxB
```
## Introduction to my sourse code

``` bash
.
├── kcpt_lib.py         #the lib of kcpt about login,get lessons and so on 
├── main.py             
├── README.md           #the indroduction of this program
└── trees.py            #the lib about the data struct in which the lessons is stored
```
## url to this project
https://github.com/Azero-NG/BJTUkcpt