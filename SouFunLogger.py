# -*- coding:utf-8 -*-

def initLog():
    from datetime import datetime
    import logging
    import sys

    logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename='./%s.log' % (datetime.now().strftime("%Y-%m-%d")),
        filemode='a')
    logger = logging.getLogger('logging')
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.NOTSET)

    return logger

