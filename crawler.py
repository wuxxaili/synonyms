#  crawler.py
#  
#
#  Created by Xuanxuan Wu on 7/02/18.
#  
import urllib
import urllib2
import BeautifulSoup
import re

class crawler(obejct):
    def __init__(self):
    
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
