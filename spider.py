""" A spider can be used to snatch content from internet

Typical applications will use 'Crawler' class. The 'Crawler'
get url and start index as input, and auto forward until URLError
"""

import urllib.request
import http
import threading
import re

from bs4 import BeautifulSoup
import pdb

class Crawler(object):
    """ The real spider class

    kernel function is run loop
    """
    def __init__(self, base_url, start_index):
        self.base_url = base_url
        self.curr_index = start_index
        self.run()

    def run(self):
        while True:
            url = self.base_url.format(self.curr_index)
            try:
                text = urllib.request.urlopen(url)\
                                .read().decode('utf-8')
            except http.client.IncompleteRead as e:
                text = e.partial
            except urllib.error.URLError:
                print("----------------END------------------")
                return
            results = Washer().pick(text)
            Storage.instance().save(results)
            self.forward()

    def forward(self):
        print('page {} finish'.format(self.curr_index))
        self.curr_index += 1


class Washer(object):
    """ A class used to transform data
    """
    _pattern = 'bbs-content'                         #博客内容所在标签的class
    _answer_flag = '-{3}|_{3}|——{3}'
    def pick(self, text):
        soup = BeautifulSoup(text, 'html.parser')
        tags = soup.find_all(class_=self._pattern)
        results = [self.filter(t) for t in tags]
        return results

    def filter(self, tag):
        content = tag.text
        m = re.search(self._answer_flag, content)
        return content if not m else ''



class Storage(object):
    """ A class response for result storage
    """
    _instance_lock = threading.Lock()
    _path = '1.txt'

    @staticmethod
    def instance():
        if not hasattr(Storage, '_instance'):
            with Storage._instance_lock:
                if not hasattr(Storage, '_instance'):
                    Storage._instance = Storage()
        return Storage._instance


    def save(self, results):
        with open(self._path, 'at') as f:
            for rs in results:
                f.write(rs)


if '__main__' == __name__:
    base_url = "http://www.tianyatool.com/bbsdoc/post/no05/146711/{}.shtml"
    start_index = 1
    caw = Crawler(base_url, start_index)

