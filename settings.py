
"""
    @Author  : Eric Liu
    @Date    : 2020.9.28
    @function: 爬虫请求参数，初始url，User_Agent，redis，数据库相关参数的配置
"""

import os
from fake_useragent import UserAgent

ua = UserAgent()  # User_Agent配置
dirs = os.path.dirname(__file__)

INI_LINK = 'https://api.500px.com/v1/photos/search?'  # 初始URL，当接口发生变化在此修改
INIT_KEY = {'萌宠': 1, '甜点': 2, '咖啡': 2, '下午茶': 2, '蛋糕': 2, '冰激淋': 2, '夜店': 3,
            '酒吧': 3, '蹦D': 3, '旅游': 4, '特色地标': 4, '运动': 5, '滑雪': 5, '篮球': 5,
            '足球': 5, '滑板': 5, '极限运动': 5, '美食': 6, '游戏': 7, '王者': 7, 'lol': 7,
            '吃鸡': 7, 'switch': 7, 'ps4': 7, '狼人杀': 7, '德州': 7, 'steam': 7, 'Coser': 8,
            '二次元': 8, '汉服': 8, '动漫手办公仔': 8}  # 待爬取关键字
HEADERS = {
        'authority': 'api.500px.com', 'method': 'GET', 'scheme': 'https', 'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br', 'accept-language': 'zh-CN,zh;q=0.9', 'User-Agent': ua.random,
        'cache-control': 'no-cache', 'origin': 'https://500px.com', 'referer': 'https://500px.com/'
}
KEY_DIR = {1: 'pet', 2: 'desserts', 3: 'nightclub', 4: 'tour', 5: 'sport', 6: 'food', 7: 'game', 8: 'coser'}

CACH_KEEP = False  # 是否持续化数据中的key
RPP = 200  # 爬取图片URl时，每页传输数量。最大200。
REDIS_INI = {'host': '127.0.0.1', 'port': 6379, 'decode_responses': True, 'db': 0}

PATH = '/Users/real/PycharmProjects/xp500'

SQL = 'insert into disposition_photo (origin_url, url, `type`) values ("{0}","https://cdn-static.real-dating.cn/server/disposition-photo/{1}/{2}",{3});\n'
SQL_PATH = os.path.join(PATH, 'statement.txt')