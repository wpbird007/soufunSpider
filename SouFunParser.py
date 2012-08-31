#coding=utf-8
"""
    soufun详情页解析
"""

from bs4 import BeautifulSoup
import bs4
from SouFunDetail import SouFunDetail
import SouFunLogger

__author__ = 'wpbird'

#搜房解析
def parse(page, url):
    LOG = SouFunLogger.initLog()
    detail = SouFunDetail()
    #解析的网页
    detail.sourceUrl = url
    #解析网页的内容
    detail.content = page
    #内容解析
    content = BeautifulSoup(page, from_encoding="utf-8")
    #标题
    detail.title = ''.join(content.find('h1', attrs={"class": "icon_tag20120517"}).stripped_strings)
    #房源标号
    detail.no = content.select(".gray6 span")[1].string[5:].strip()
    #发布时间
    publish_time = content.find('p', class_="gray6").contents[4]
    publish_time = publish_time[5:len(publish_time) - 1]
    detail.publish_time = publish_time
    dllist = content.select('.base_info dl')
    items = []
    for dl in dllist:
        items.extend([''.join(tag.stripped_strings) for tag in dl.contents if isinstance(tag, bs4.element.Tag)])
    detail.total = ''
    detail.roomStyle = ''
    detail.area = ''
    detail.useArea = ''
    detail.year = ''
    detail.face = ''
    detail.floor = ''
    detail.structure = ''
    detail.decoration = ''
    detail.type = ''
    detail.build_type = ''
    detail.right = ''
    detail.meetTime = ''
    detail.build_name = ''
    detail.support = ''
    for item in items:
        item_spi = [it.strip() for it in item.split(u'：')]
        if len(item_spi) == 2:
            if item_spi[0].find(u'总价') >= 0 < item_spi[1].find('('):
                detail.total = item_spi[1]
            elif item_spi[0].find(u'户型') >= 0:
                detail.roomStyle = item_spi[1]
            elif item_spi[0].find(u'使用面积') >= 0:
                detail.useArea = item_spi[1]
            elif item_spi[0].find(u'建筑面积') >= 0:
                detail.area = item_spi[1]
            elif item_spi[0].find(u'年代') >= 0:
                detail.year = item_spi[1]
            elif item_spi[0].find(u'朝向') >= 0:
                detail.face = item_spi[1]
            elif item_spi[0].find(u'楼层') >= 0:
                detail.floor = item_spi[1]
            elif item_spi[0].find(u'结构') >= 0:
                detail.structure = item_spi[1]
            elif item_spi[0].find(u'装修') >= 0:
                detail.decoration = item_spi[1]
            elif item_spi[0].find(u'住宅类别') >= 0:
                detail.type = item_spi[1]
            elif item_spi[0].find(u'建筑类别') >= 0:
                detail.build_type = item_spi[1]
            elif item_spi[0].find(u'产权性质') >= 0:
                detail.right = item_spi[1]
            elif item_spi[0].find(u'看房时间') >= 0:
                detail.meetTime = item_spi[1]
            elif item_spi[0].find(u'楼盘名称') >= 0:
                detail.build_name = item_spi[1]
            elif item_spi[0].find(u'配套设施') >= 0:
                detail.support = item_spi[1]
                #电话
    detail.phone = content.find("span", attrs={"id": "mobilecode"}).string
    LOG.debug(
        'total:%s roomstyle: %s area:%s useArea:%s' % (detail.total, detail.roomStyle, detail.area, detail.useArea))
    LOG.debug(
        'year:%s face:%s floor:%s structure:%s decoration:%s type:%s build_type:%s right:%s meetTime:%s build_name:%s support:%s' % (
            detail.year, detail.face, detail.floor, detail.structure, detail.decoration, detail.type, detail.build_type,
            detail.right, detail.meetTime, detail.build_name, detail.support))
    #房源描述
    detail.describe = ''.join(content.select('.describe.mt10 div')[0].stripped_strings)
    #户型图
    if not len(content.select('#esfbjxq_117 img')):
        detail.sizeImg = ''
    else:
        detail.sizeImg = ''.join([content.select('#esfbjxq_117 img')[0]['src']])
    LOG.debug('sizeImg:%s' % detail.sizeImg)
    #室内图
    roomImgList = []
    for img in content.select('#esfbjxq_116 img'):
        if img.has_key('src'):
            roomImgList.append(img['src'])
    detail.indoorImgs = ','.join(roomImgList)
    LOG.debug('indoorImgs:%s' % detail.indoorImgs)
    #外景图 js动态写上的，需要可以执行网页的解析器
    #地图交通 （地址 交通状况）#0是地址，1交通
    addAndTra = [''.join(tt.stripped_strings) for tt in content.select('#esfbjxq_121 p')]
    detail.address = addAndTra[0][3:]
    detail.traffic = ''.join(addAndTra[1][5:].split())
    LOG.debug('address:%s traffic:%s' % (detail.address, detail.traffic))
    #小区简介（物业类型 绿化率 物业费 物业公司 楼盘名称 开发商）
    detail.wuyeType = ''
    detail.lvhua = ''
    detail.wuyeFee = ''
    detail.wuyeComp = ''
    detail.developer = ''
    briefIntro = [''.join(tt.stripped_strings) for tt in content.select('dl.mt10 dd')]
    for tmp in briefIntro:
        items = tmp.strip().split(u'：')
        if len(items) == 2:
            if items[0].find(u'物业类型') >= 0:
                detail.wuyeType = items[1]
            elif items[0].find(u'绿 化 率') >= 0:
                    detail.lvhua = items[1]
            elif items[0].find(u'物 业 费') >= 0:
                    detail.wuyeFee = items[1]
            elif items[0].find(u'物业公司') >= 0:
                    detail.wuyeComp = items[1]
            elif items[0].find(u'开 发 商') >= 0:
                    detail.developer = items[1]
    LOG.debug('wuyeType:%s lvhua:%s wuyefee:%s wuyeCom:%s developer:%s' % (detail.wuyeType, detail.lvhua, detail.wuyeFee, detail.wuyeComp, detail.developer))
    return detail

if __name__ == '__main__':
        url = 'http://esf.soufun.com/chushou/3_67581874.htm'
        path = 'F:/soufun/2012-08-30/test/3_67581874.htm'
        #    pageInfo = souFunSpider.getDetail('test',url)
        file1 = open(path, 'rb')
        parse(unicode(''.join(file1.readlines()), encoding='utf-8'), url)
        #    path = 'F:/soufun/error/3_68428130.htm'
        #    page = open(path,'rb')
        #    d = parse(unicode(''.join(page.readlines()),encoding='utf-8'),'test')
        #    print d.__dict__
        #    for root, dirs, files in os.walk('F:/soufun/2012-08-23'):
        #        for file in files:
        #            path = os.path.join(root.decode('gbk'), file)
        #            print path
        #            try:
        #                file1 = open(path, 'rb')
        #                d = parse(unicode(''.join(file1.readlines()), encoding='utf-8'),'http://esf.soufun.com/chushou/' + file)
        #                file1.close()
        #            except Exception,e:
        #                print path
        #                print e