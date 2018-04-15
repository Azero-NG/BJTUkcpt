#!/env/bin python3
# !coding:utf-8
import requests
import re
import time
from pyquery import PyQuery as pq

def GetLesson(s):
    r=s.get(r'http://cc.bjtu.edu.cn:81/meol/lesson/blen.student.lesson.list.jsp')#课程列表
    h=re.findall(r'<a href="init_course.jsp\?lid=(.*?)" target="_blank">(\S*)',r.text)
    if(len(h)>=1):
        for x in range(len(h)):
            h[x]=list(h[x])
            h[x][0]=r'http://cc.bjtu.edu.cn:81/meol/common/script/listview.jsp?acttype=enter&folderid=0&lid='+h[x][0]
        return h
def GetCourseName(courseId,s):
    r=s.get('http://cc.bjtu.edu.cn:81/meol/jpk/course/layout/newpage/index.jsp?courseId='+str(courseId))
    result=re.findall(pat,r.text)
    if(len(result)>=1):
        return re.sub(r'\s','',result[0])
def GetCourseProfile(courseId=''):
    pattern=r'<p class="offCon" style="display:none;">([\s\S]*?)</p>'
    try:
        a=s.get('http://cc.bjtu.edu.cn:81/meol/jpk/course/layout/newpage/default_demonstrate.jsp?courseId='+courseId)
        h=re.findall(pattern,a.text)
        if(len(h)!=0):
            h=re.sub(r'(\s|&.*?quo)','',h[0])#正则或匹配用括号
            return h
    except:
        pass

class kcptfile:
    web_name=''
    link=''
    file_name=''
    father_dir=''
    s=requests.Session
    def download(s):
        res=s.get(kcptfile.link)
        with open(father_dir+res.headers['Content-Disposition'][22:-1],'w') as f:
            f.write(res.content)


class kcptdir:
    a={'name':'','link':'','children':[],'father':'','files':[]}
    name='6'
    def fillchildren(s):
        ##文件名
        d=s.get(kcptfile.a['link'])
        table=re.findall(r'<TABLE cellSpacing=0 cellPadding=0 class="valuelist">[\s\S]*?</TABLE>',d.text)[0]
        lis=re.findall('<TD class="common indentten" colspan="4"><img alt="" src=".*?">&nbsp;<a href="(.*?)" title="">(.*?)</a></TD>',table)
        for x in lis:
            kcptfile(name=x[1],link=x[0],father=kcptfile.a['link'],s=s)
        sou=re.findall(r'<a href="(.*?)" target="_blank"\s*?title="">(.*?)</a>',table)
        for x in sou:
            kcptfile.a['files'].append(x)
    def __init__(self,name='',link='',children='',father='',s=''):
        kcptfile.a['name']=name
        kcptfile.a['link']=link
        kcptfile.a['children']=children
        kcptfile.a['father']=father
        kcptfile.fillchildren(s)
def login(username='',password=''):
    s=requests.session()
    s.get('http://jwc.bjtu.edu.cn:82/LoginAjax.aspx?username='+ username + '&password=' + password +'&type=1')
    s.get('http://jwc.bjtu.edu.cn:82/NoMasterJumpPage.aspx?URL=jwcKcpt&FPC=page:jwcKcpt')
    return s
def loginByMis(username='',password=''):
    s = requests.session()
    a = s.get("https://mis.bjtu.edu.cn/", verify=False)
    doc = pq(a.text)
    data = {doc("input[value]")[0].attrib['name']: doc("input[value]")[0].attrib['value'],
            doc("input[value]")[1].attrib['name']: doc("input[value]")[1].attrib['value'], 'loginname': username,
            'password': password}
    s.headers['Referer'] = a.url
    print(a.url)
    print("\n\n\n\n\n\n\n")
    b = s.post(a.url, data=data)
    c = s.get("https://mis.bjtu.edu.cn/module/module/280/")
    doc2 = pq(c.text)
    data = {doc2("input")[0].attrib['name']: doc2("input")[0].attrib['value']
        , doc2("input")[1].attrib['name']: doc2("input")[1].attrib['value']
        , doc2("input")[2].attrib['name']: doc2("input")[2].attrib['value']}
    d = s.post("http://cc.bjtu.edu.cn:81/meol/homepage/common/sso_login_portal.jsp", data=data)
    return s
# s=login()
# root=[]
# print(GetLesson(s))
#for x in GetLesson(s):
#    root.append(kcptfile(name=x[1],link=('http://cc.bjtu.edu.cn:81/meol/lesson/'+x[0]),s=s)





#http://cc.bjtu.edu.cn:81/meol/lesson/blen.student.lesson.list.jsp#课程列表
#'http://cc.bjtu.edu.cn:81/meol/jpk/course/layout/newpage/default_demonstrate.jsp?courseId='+str(courseId))#课程描述
#'http://cc.bjtu.edu.cn:81/meol/common/script/listview.jsp?acttype=enter&folderid=0&lid='+courseId#根目录




'''
#bbc=s.get('http://cc.bjtu.edu.cn:81/meol/common/script/preview/download_preview.jsp?fileid=354908&resid=64301&lid=11717')
#print(bbc.links)
#with open('test.doc','wb') as code:
    #code.write(bbc.content)
#url='http://cc.bjtu.edu.cn:81/meol/common/script/'
#r=s.get(url+i[0])
#r.headers['Content-Disposition'].encode('latin1').decode()
#
#GetLesson(s)
#
#
#
#
#
#courseId='18346'
#courseUrl='http://cc.bjtu.edu.cn:81/meol/jpk/course/layout/newpage/index.jsp?courseId='+courseId
#courseRootUrl=r'http://cc.bjtu.edu.cn:81/meol/common/script/listview.jsp?acttype=enter&folderid=0&lid=' + courseId#根目录
#kcptfile(GetCourseName(courseUrl,s),courseRootUrl)
'''
