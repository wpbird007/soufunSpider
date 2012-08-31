#coding=utf-8
import os
from sqlalchemy import *
from sqlalchemy.orm import *
import SouFunDetail
import SouFunLogger
import SouFunParser
"""
    将抓取的数据解析后入库
"""
__author__ = 'wpbird'
LOG = SouFunLogger.initLog()
sqlite_engine = create_engine('sqlite:///soufun.db', echo=True)
mysql_engine = create_engine('mysql://wangp:wangp@192.168.0.138/wangp?charset=utf8')

metadata = MetaData()
soufun = Table('soufunDetail', metadata,
    Column('id', Integer, primary_key=True),
    Column('sourceUrl', String(50)),
    Column('title', String(100)),
    Column('no', String(15)),
    Column('publish_time', String(20)),
    Column('total', String(100)),
    Column('roomStyle', String(100)),
    Column('area', String(20)),
    Column('useArea', String(20)),
    Column('phone', String(15)),
    Column('year', String(10)),
    Column('face', String(10)),
    Column('floor', String(100)),
    Column('structure', String(100)),
    Column('decoration', String(100)),
    Column('type', String(100)),
    Column('build_type', String(100)),
    Column('right', String(100)),
    Column('meetTime', String(100)),
    Column('build_name', String(100)),
    Column('support', String(100)),
    Column('describe', String(2000)),
    Column('sizeImg', String(500)),
    Column('indoorImgs', String(2000)),
    Column('address', String(200)),
    Column('traffic', String(200)),
    Column('wuyeType', String(100)),
    Column('lvhua', String(100)),
    Column('wuyeFee', String(100)),
    Column('wuyeComp', String(200)),
    Column('developer', String(200)),
    mysql_engine='InnoDB',
    mysql_charset='utf8')

mapper(SouFunDetail.SouFunDetail, soufun)
metadata.create_all(mysql_engine)
Session = sessionmaker(bind=mysql_engine)
session = Session()

def addToDB(detail):
    session.add(detail)
    session.flush()

def showAll():
    for d in session.query(SouFunDetail.SouFunDetail):
        print d

if __name__ == '__main__':
    for root, dirs, files in os.walk('F:/soufun/2012-08-23'):
        for file in files:
            path = os.path.join(root.decode('gbk'), file)
            LOG.debug(u'正在解析 %s' % path)
            try:
                file1 = open(path, 'rb')
                d = SouFunParser.parse(unicode(''.join(file1.readlines()), encoding='utf-8'),
                    'http://esf.soufun.com/chushou/' + file)
                addToDB(d)
            except Exception as e:
                LOG.error(e.value)
                session.commit()
        session.commit()