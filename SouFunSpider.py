#coding=UTF-8
"""
    soufun二手房抓取，主要抓取感兴趣的房源信息
"""
import StringIO
import gzip
import os
import re
import urllib
import urllib2
from urlparse import urlparse
from bs4 import BeautifulSoup
import time
import SouFunLogger

__author__ = 'wpbird'

default_url = 'http://esf.soufun.com'
default_dir = 'f:\\soufun'
default_sep = os.path.sep
default_time = time.strftime("%Y-%m-%d", time.localtime())
default_encode = 'gbk'
default_imgDir = 'f:\\soufun\\imgs'
LOG = SouFunLogger.initLog()

#获取图片
def getImage(url, name, imgs):
    result = urlparse(url)
    imgpath = default_imgDir + default_sep + unicode(name) + default_sep + result.path.split('/')[-1] + default_sep
    if not os.path.exists(imgpath):
        os.makedirs(imgpath)
    for img in imgs:
        print u'%s 写入' % img
        urllib.urlretrieve(img, unicode(imgpath) + ''.join(urlparse(img).path.split('/')[-2:]))

#抓取指定url内容
def getUrlInfo(url):
    html = ''
    try:
        request = urllib2.Request(url)
        request.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0")
        request.add_header("Accept-Language", "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3")
        request.add_header("Accept-Charset", "GB2312,utf-8;q=0.7,*;q=0.7")
        request.add_header("Accept-Encoding", "gzip,deflate")
        response = urllib2.urlopen(request)
        html = response.read()
        if response.info()['content-encoding'] == 'gzip' or response.info()['Content-Encoding'] == 'gzip':
            html = gzip.GzipFile(fileobj=StringIO.StringIO(html)).read()
    except urllib2.URLError as e:
        LOG.error('%s fetch error,error code is %s' % (url, e.code))
    if not isinstance(html, unicode):
        html = unicode(html, default_encode)
    return html

#获取下一页和详情的连接
def getNextAndDetailURL(page):
    links_dict = {}
    detailReg = re.compile('/chushou/[\d|_]*.htm')
    detailList = []
    soup = BeautifulSoup(page)
    links = soup.find_all('a')
    for link in links:
        if link.has_key('href')  and detailReg.match(link['href']):
            detailList.append(''.join([default_url, link['href']]))
    links_dict['details'] = set(detailList)

    #获取下一页的连接
    nextLink = soup.find(id="PageControl1_hlk_next")
    if nextLink and nextLink.has_key('href'):
        links_dict['next'] = ''.join([default_url, nextLink['href']])
    return links_dict

#获取详情
"""
    ·获取详情：
     1、下载页面
     2、下载图片
    ·目录组织形式
      顶级目录 日期 小区名 details
"""

def getDetail(xiaoqu, detail_url):
    LOG.debug(u'开始写入 【%s】 的 %s 连接' % (unicode(xiaoqu, 'utf-8'), detail_url))
    detailContent = getUrlInfo(detail_url)
    path = default_dir + default_sep + default_time + default_sep + unicode(xiaoqu, 'utf-8')
    if not os.path.exists(path):
        os.makedirs(path)
    output = open(path + default_sep + detail_url.split('/')[-1], 'wb', )
    output.write(detailContent.encode('utf-8'))
    output.close()
    LOG.debug(u'%s 写入结束' % detail_url)

if __name__ == '__main__':
    base_url = 'http://esf.soufun.com/house-a01/c2150-d2200-g22-j250-k270-p20-kw'
    seeds = {'安慧里': '%b0%b2%bb%db%c0%ef', '慧忠里': '%bb%db%d6%d2%c0%ef', '慧忠北里': '%bb%db%d6%d2%b1%b1%c0%ef',
             '安慧北里': '%b0%b2%bb%db%b1%b1%c0%ef'}
    for seed in seeds.keys():
        LOG.info(u'开始抓取【 %s 】附近的房源 ' % seed)
        page = getUrlInfo(base_url + seeds[seed] + '/')
        dict = getNextAndDetailURL(page)
        for detail in dict['details']:
            time.sleep(1)
            getDetail(seed, detail)
        while dict.has_key('next'):
            page = getUrlInfo(dict['next'])
            dict = getNextAndDetailURL(page)
            for detail in dict['details']:
                time.sleep(1)
                getDetail(seed, detail)