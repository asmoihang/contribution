import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import traceback
from datetime import datetime, timedelta
from typing import *
import copy

members: Dict[str, List] = {}

def read_members_from_file(file_name):
    global members 
    with open(file_name, 'r', encoding='utf-8') as file:
        members = json.load(file)

class MembersHandler(tornado.web.RequestHandler):
    def get(self):
        pass

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/members", MembersHandler),
    ],
    template_path="templates")

if __name__ == '__main__':
    # 读取信息
    read_members_from_file('members.json')

    app = make_app()
    app.listen(8889)
    print('Server started')
    print('http://localhost:8889')
    tornado.ioloop.IOLoop.current().start()