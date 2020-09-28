

import os
import time
import requests
import hashlib
from random import randint
from DBConfig import RedisConfig
from settings import HEADERS, PATH, KEY_DIR, SQL, SQL_PATH

class DownImage(object):

    def __init__(self):
        self.rc = RedisConfig.rc
        self.headers = HEADERS
        self.hash_object = HashLink()

    def get_link(self):
        return self.rc.lpop('links')

    def sadd_finger(self, finger):
        return self.rc.sadd('finger', finger)

    def judge(self, finger):
        return self.rc.sismember('finger', finger)

    def download(self, image_path, link, key_type):
        file_name = link.split('=')[-1] + '.jpg'
        file_path = os.path.join(image_path, file_name)
        tries_num = 3
        sleep_time = 1
        finger = self.hash_object.creat_finger(link)
        if self.judge(finger) != 1:
            for i in range(tries_num):
                try:
                    image = requests.get(url=link, headers=self.headers, timeout=120).content
                    with open(file_path, 'wb') as f:
                        f.write(image)
                        f.flush()
                    self.sadd_finger(finger)
                    with open(SQL_PATH, 'a', encoding='utf-8') as fq:
                        fq.write(SQL.format(link, KEY_DIR[key_type], file_name, key_type))
                    time.sleep(randint(2, 5)/10)
                    return
                except Exception as exc:
                    if i < 2:
                        print(f'{exc} ------  在{sleep_time}秒后，重新发起第{i}次请求')
                        time.sleep(sleep_time)
                    if i == 2:
                        self.rc.rpush('links', str((link, key_type)))
                        print(f'已将{link}重新加入队列')
                    sleep_time += 1


    def run(self):
        lpop_times = 0
        while True:
            parameter = self.get_link()
            if parameter:
                link, key_type = eval(parameter)
                path = PATH + '/{0}'.format(KEY_DIR[key_type])
                if not os.path.exists(path):
                    os.makedirs(path)
                self.download(image_path=path,
                              link=link, key_type=key_type)
            else:
                time.sleep(3)
                if lpop_times < 10:
                    break

class HashLink():

    def __init__(self):
        self.ham5 = hashlib.md5()

    def creat_finger(self, url):
        self.ham5.update(url.encode(encoding='utf-8'))
        return self.ham5.hexdigest()