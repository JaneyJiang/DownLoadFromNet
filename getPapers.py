#coding python3.6
#JaneyJiang
#http://www.jmlr.org/papers/
#downLoad paper from websit
#download according to the volume
#TODO:how to download according to the topic.

import requests
from bs4 import BeautifulSoup
import os
import re
from urllib.request import urlretrieve
from urllib.parse import urljoin


def getbsObj(url):
    try:
            headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome'}
            r = requests.get(url, headers = headers)
            r.raise_for_status()
    except:
 	    print('get {0} page failed'.format(url))
    else:
 	    bsObj = BeautifulSoup(r.content, 'html.parser')
 	    return bsObj
 	
class GetPaper:
    def __init__(self,url):
        self.baseurl = url
        self.naviurls = list()
        self.foldnames = list()
        self.starturl = self.baseurl
        self.pdfurls = list()
        self.fold = '/'.join(os.getcwd().split('\\'))

    def getNaviUrls(self):
        bsObj = getbsObj(self.starturl)
        #atrees = bsObj.find('div',{'id':'content'}).findAll('a')
        #atrees = bsObj.find('div',{'id':'content'}).findAll('a', href= re.compile('^(v)\d+'))
        atrees = bsObj.find('div',{'id':'content'}).findAll('a', href= re.compile('^(topic|special).*html'))
        #如果需要制定某些特殊格式herf则用如下，否则就用如上，因为所要下载的导航链接都在上面
        #这个示例是保存只是volumn的paper
        #self.naviurls = bsObj.find('div',{'id':'content'}).findAll('a', href= re.compile('^(v)\d+'))
        for i,a in enumerate(atrees):
            suburl = a.get('href')
            self.naviurls.append(self.baseurl + '/'+a.get('href'))
            #self.foldnames.append(a.get_text())
            #print(self.naviurls)

    def processNaviUrls(self):
        for index,url in enumerate(self.naviurls):
            print(url)
           # if index b
            bsObj = getbsObj(url)
            #if index <=14:
            #    pdfurl,filename = self.processVolumeafter3(bsObj)
            #else:
            self.processVolume(bsObj)
            #self.processVolumeafter3(bsObj)
            
                    
    def processVolumeafter3(self,bsObj):#原来用来处理volumn4，,5.等大于volumn3的数据，这里已经不需要了，可以改写成为适用于special topic的paper下载
        content = bsObj.find('div',{'id':'content'}).findAll('dl')
        pdfurl = ''
        filename =''
        for i,dl in enumerate(content):
            #title_name = p.dt.get_text()
            dl = dl.dt.dd#之所以下降范围是因为如果不这么做会有干扰url出现
            suburl = dl.find('a',{'target':'_blank'}).get('href')
            #print(suburl)
            pdfurl = urljoin(self.baseurl,suburl)
            #pathlist = suburl.split('/')[-4:-1]+title_name+'.pdf'
            filename = self.fold +'/'+ '/'.join(suburl.split('/')[-4:])
            saveFile(filename, pdfurl) 


    def processVolume(self,bsObj):#处理volume的下载
        content = bsObj.findAll('a',{'href':re.compile(r'.*volume\d+.*pdf$')})
        pdfurl = ''
        filename =''
        for a in content:
            suburl = a.get('href')
            pdfurl = urljoin(self.baseurl,suburl)
            #pathlist = suburl.split('/')[-4:-1]+title_name+'.pdf'
            filename = self.fold +'/'+ '/'.join(suburl.split('/')[-4:])
            print(filename, pdfurl)
            saveFile(filename, pdfurl)        

    def getDownloadPath(self):
        pass
    def co_paper(self):
        self.getNaviUrls()
        self.processNaviUrls()

#save pdf as filename from source url
def saveFile(filename, source):
    directory = os.path.dirname(filename)
    #print(directory)
    if not os.path.exists(directory):
        os.makedirs(directory)
        #print(directory)
        print(filename, source)
        urlretrieve(source, filename)

        
if __name__ == '__main__':
    url = 'http://www.jmlr.org/papers'
    getPaper = GetPaper(url)
    getPaper.co_paper()
    
