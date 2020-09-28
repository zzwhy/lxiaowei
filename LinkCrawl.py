

import json
import requests
from DBConfig import RedisConfig
from settings import INI_LINK, HEADERS, INIT_KEY, RPP, CACH_KEEP
RedisConfig.cache_keep(CACH_KEEP)

class DownLink(object):

    def __init__(self):
        self.rc = RedisConfig.rc
        self.headers = HEADERS
        self.key_list = INIT_KEY
        self.link = INI_LINK
        self.rpp = RPP

    def get_link(self, page, keyword, key_type):

        params = {
            'type': 'photos',
            'term': keyword,  # 带搜索关键字
            'image_size[]': '31',
            'include_states': 'true',
            'formats': 'jpeg',  # 图片格式
            'page': page,  # 页码 出示页码是从1开始的。
            'rpp': self.rpp,  # 每页请求几个回来
        }
        resp = requests.get(url=self.link, params=params, headers=self.headers)
        content_json = json.loads(resp.text)
        content_num = len(content_json['photos'])
        if content_num != 0:
            for block in content_json['photos']:
                link = block['image_url'][-1]
                self.rc.rpush('links', str((link, key_type)))
            print('已经向redis中添加{0}类，第{1}页！'.format(keyword, page))
            return False
        else:
            return True

    def run(self):
        for keyword, key_type in self.key_list.items():
            page = 1
            while True:
                flag = self.get_link(page=page, keyword=keyword, key_type=key_type)
                page += 1
                if flag or page == 6:
                    break