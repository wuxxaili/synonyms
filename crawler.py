#  crawler.py
#  
#
#  Created by Xuanxuan Wu on 7/02/18.
#  
import urllib
import urllib2
import BeautifulSoup
import re
## the following package mock a browser and submit the query to website, when we cannot find the url
from selenium import webdriver
from time import sleep
## Another method to mock a browser
import mechanize
import cookielib

## In fact, I didn't use the method "mock a browser" since I can easily get the url, the speed is much faster than mock a browser.

class crawler():
    def __init__(self):
        ## Those work for function crawler_xinpai_browser
        self.br = mechanize.Browser()
        # Cookie Jar
        self.cj = cookielib.LWPCookieJar()
        self.br.set_cookiejar(self.cj)
        # Browser options
        self.br.set_handle_equiv(True)
        self.br.set_handle_gzip(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_robots(False)
        # Follows refresh 0 but not hangs on refresh > 0
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        self.br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


    
    ## This function crawls all the synonyms from http://jyc.kxue.com
    ## Return a dictionay with length 8215
    def crawler_kuaixue(self):
        Synony_kuaixue = {}
        for i in range(1,138):
            url =  ['http://jyc.kxue.com/list/index_',str(i),'.html']
            url = "".join(url)
            html = self.open_url(url)
            soup = BeautifulSoup.BeautifulSoup(html)
            syn = soup.findAll("span", {"class": "hz"})
            for s in syn:
                word = self.remainChinese(s.a.text).encode('utf-8')
                if word not in Synony_kuaixue:
                    js = self.remainChinese(s.findAll("span",{"class":"js"})[0].text).encode('utf-8').split("、")
                    Synony_kuaixue[word] = js
        return Synony_kuaixue
    
    ## This function crawls all the synonyms from http://jinyici.xpcha.com
    ## Return a dictionay with length 8215
    def crawler_xinpai(self):
        Synony_xinpai = {}
        for i in range(1,173):
            if i in [11,12,31,41,51,61,71,81,91,101,111,121,131,141,151,161,171]:
                continue
            url =  ['http://jinyici.xpcha.com/list_0_',str(i),'.html']
            url = "".join(url)
            html = self.open_url(url)
            soup = BeautifulSoup.BeautifulSoup(html)
            syn = soup.findAll("dl", {"class":"shaixuan_5"})[0].findAll('a')
            for s in syn:
                word = self.remainChinese(s.text).encode('utf-8')
                if word not in xinpai:
                    Synony_xinpai[word] = []
                    newurl = 'http://jinyici.xpcha.com/' + s['href'].encode('ascii')
                    newhtml = self.open_url(newurl)
                    newsoup = BeautifulSoup.BeautifulSoup(newhtml)
                    newsyn = newsoup.findAll("dl", {"class":"shaixuan_1"})[0].findAll('span')
                    for syn in newsyn:
                        Synony_xinpai[word].append(remainChinese(syn.text).encode('utf-8'))
         return Synony_xinpai
    
    ## This function crawls the synonyms from http://dict.baidu.com
    ## Enter one word and return a list contains the synonyms of the word
    def crawler_baidu(self,word):
        url = ['http://dict.baidu.com/s?wd=',word,'&ptype=word']
        url = "".join(url)
        html = self.open_url(url)
        if html == 0:
            return []
        soup = BeautifulSoup.BeautifulSoup(html)
        s = soup.find(id='synonym')
        res = []
        if s is not None:
            for k in s.findAll('a'):
                res.append(str(k.string.encode('utf-8')))
        return res
    
    def crawler_baidu_browser(self,word):
        driver = webdriver.PhantomJS()
        driver.get("http://dict.baidu.com/")
        driver.find_element_by_id('kw').send_keys(word.decode('utf-8'))
        sleep(1)
        driver.find_element_by_id('su').click()
        html = self.open_url(driver.current_url)
        if html == 0:
            return []
        soup = BeautifulSoup.BeautifulSoup(html)
        s = soup.find(id='synonym')
        res = []
        if s is not None:
            for k in s.findAll('a'):
                res.append(str(k.string.encode('utf-8')))
        return res
    
    def crawler_xinpai_browser(self,word):
        r = self.br.open('http://jinyici.xpcha.com/')
        html = r.read()
        # Select the first (index zero) form
        br.select_form(nr=0)
        # Let's search
        br.form['q']=word
        br.submit()
        lines = br.response().read()
        result = re.findall(r"<span>(.+?)：</span>",lines)
        return result

    ##open the url
    def open_url(self,url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0')
        try:
            response = urllib2.urlopen(req)
            html = response.read()
            return html
        except urllib2.HTTPError:
            print 'There was an error with the request'
            return 0

    ## Sometime the synonyms we crawled from websites might not be the manderin
    ## use re only remain the manderin
    def remainChinese(self,s):
        rule = re.compile(ur"[^ \u4e00-\u9fa5 ^\u3001]")
        return rule.sub('',s)
