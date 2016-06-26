# -*- coding: utf-8 -*-  
#---------------------------------------  
#   程序：乐文小说爬虫  
#   版本：1.0  
#   作者：token  
#   日期：2016-06-26  
#   语言：Python 2.7  
#   操作：输入网址后自动只看楼主并保存到本地文件  
#   功能：将楼主发布的内容打包txt存储到本地。  
#---------------------------------------  
   
import string  
import urllib2  
import re  
  
#----------- 处理页面上的各种标签 -----------  
class HTML_Tool:  
    # 用非 贪婪模式 匹配 \t 或者 \n 或者 空格 或者 超链接 或者 图片  
    BgnCharToNoneRex = re.compile("(\t|\n| |<a.*?>|<img.*?>)")  
      
    # 用非 贪婪模式 匹配 任意<>标签  
    EndCharToNoneRex = re.compile("<.*?>")  
  
    # 用非 贪婪模式 匹配 任意<p>标签  
    BgnPartRex = re.compile("<p.*?>")  
    CharToNewLineRex = re.compile("(<br/>|</p>|<tr>|<div>|</div>)")  
    CharToNextTabRex = re.compile("<td>")  
  
    # 将一些html的符号实体转变为原始符号  
    replaceTab = [("<","<"),(">",">"),("&","&"),("&","\""),(" "," ")]  
      
    def Replace_Char(self,x):  
        x = self.BgnCharToNoneRex.sub("",x)  
        x = self.BgnPartRex.sub("\n    ",x)  
        x = self.CharToNewLineRex.sub("\n",x)  
        x = self.CharToNextTabRex.sub("\t",x)  
        x = self.EndCharToNoneRex.sub("",x)  
  
        for t in self.replaceTab:    
            x = x.replace(t[0],t[1])    
        return x    
      
class Lewen_Spider:  
    # 申明相关的属性  
    def __init__(self,url):    
        self.myUrl = url
        self.chapters = []
        self.datas = []  
        self.myTool = HTML_Tool()  
        print u'已经启动乐文爬虫，咔嚓咔嚓'  
    
    # 初始化加载页面并将其转码储存  
    def lewen_xs(self):  
        # 读取页面的原始信息并将其从gbk转码  
        myPage = urllib2.urlopen(self.myUrl).read().decode("GBK")
        # 获取小说的标题  
        title = self.find_title(myPage)  
        print u'小说标题：' + title
        # 获取小说章节数和对应的url  
        self.chapter_counter(myPage)    
        # 获取最终的数据  
        self.save_data(title,self.chapters)  

    # 获取小说的标题  
    def find_title(self,myPage):  
        # 匹配 找出标题  
        myMatch = re.search(r'<h1>(.*?)</h1>', myPage, re.S)  
        title = u'暂无标题'  
        if myMatch:  
            title  = myMatch.group(1)
        else:
            print u'爬虫报告：无法加载小说标题！'  
        # 文件名不能包含以下字符： \ / ： * ? " < > |  
        title = title.replace('\\','').replace('/','').replace(':','').replace('*','').replace('?','').replace('"','').replace('>','').replace('<','').replace('|','')  
        return title

    #获取小说章节数和对应的url
    def chapter_counter(self,myPage):  
        myMatch2 = re.findall(r'(?i)class=dccss.*?>\s*\r*\n*<a.*? href=[\"\'](.*?)[\"\'].*?>(.*?)</a>', myPage, re.S)

        if myMatch2:
            #myMatch2:(u'14582635.html', u'\u7b2c1\u7ae0 \u4e09\u4e2a\u68a6\u5883')
            for k, v in myMatch2:
                #print k, v
                #print v, self.myUrl[:self.myUrl.find("index.html")]+k
                if k.startswith('h'):
                    continue
                self.chapters.append((v,self.myUrl[:self.myUrl.find("index.html")]+k))
  
            print u'爬虫报告：成功获取小说章节'
        else:  
            print u'爬虫报告：未发现小说内容' 
        #return endPage  

    # 获取最终的数据
    def save_data(self,title,chapters):  
        # 加载页面数据到数组中  
        self.get_data(chapters)  
        # 打开本地文件  
        f = open(title+'.txt','w+')
        f.writelines(self.datas)  
        f.close()  
        print u'爬虫报告：文件已下载到本地并打包成txt文件'  
        print u'请按任意键继续...'  
        raw_input();  

    # 获取页面源码并将其存储到数组中  
    def get_data(self,chapters):
        i = 1
        for key, value in chapters:
            print u'爬虫报告：爬虫正在加载第%d章...'%i
            myPage = urllib2.urlopen(value).read().decode("GBK") 
            # 将myPage中的html代码处理并存储到datas里面  
            self.deal_data(key, myPage)
            i = i + 1

    # 将内容从页面代码中抠出来  
    def deal_data(self,key,myPage):
        p = r'(?i)id=content.*?>\s*\r*\n*<p>(.*?)</p>'
        myItem = re.findall(p,myPage,re.S)
        #print "-------------------------------",myItems
        if myItem:
            chap_title = self.myTool.Replace_Char(key.replace("\n","").encode('GBK'))
            data = self.myTool.Replace_Char(myItem[0].replace("\n","").replace("&nbsp;","").encode('GBK'))
            self.datas.append(chap_title+'\n'+data+'\n')

#-------- 程序入口处 ------------------  
print u"""#--------------------------------------- 
#   程序：乐文小说爬虫 
#   版本：1.0 
#   作者：token 
#   日期：2016-06-26 
#   语言：Python 2.7 
#   操作：输入网址后自动只看楼主并保存到本地文件 
#   功能：将楼主发布的内容打包txt存储到本地。 
#--------------------------------------- 
"""  

while True:  
    print u'输入网址格式如：www.lwxs520.com/books/60/60618/index.html(输入0结束)'  
    url = str(raw_input(u''))

    if url == '0':
        break
    else:
        lwurl = 'http://' + url
        # lwurl = "http://www.lwxs520.com/books/64/64682/index.html"
        #调用  
        mySpider = Lewen_Spider(lwurl)  
        mySpider.lewen_xs()

print u'欢迎下次使用！'
