import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import traceback
from datetime import datetime, timedelta
from typing import *
import copy
import sqlite3
import calendar

members: Dict[str, List] = {}

def creat_table_by_sqlite():
    try:
        conn = sqlite3.connect('members.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date DATE NOT NULL,
                welfare_completed INTEGER NOT NULL,
                contribution INTEGER NOT NULL,
                full_completed_welfare INTERGER NOT NULL,
                completed_5_days_welfare INTERGER NOT NULL
            )
        ''')
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def get_all_members_info():
    try:
        conn = sqlite3.connect('members.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT name, date, welfare_completed, contribution, full_completed_welfare, completed_5_days_welfare FROM members
                       ''')
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def insert_member_to_table(tuple_data):
    try:
        conn = sqlite3.connect('members.db')
        cursor = conn.cursor()
        sql = '''INSERT INTO members (name, date, welfare_completed, contribution, full_completed_welfare, completed_5_days_welfare) VALUES(?, ?, ?, ?, ?, ?)'''
        cursor.execute(sql, tuple_data)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def calculate_current_month_total(start_day=1):
    # 获取当前年份和月份
    now = datetime.now()
    year = now.year
    month = now.month
    
    # 计算当前年份和月份的天数
    days_in_month = calendar.monthrange(year, month)[1]
    
    full_total = 0
    total_5_days = 0
    for day in range(start_day, days_in_month + 1):
        # 判断每一天是星期几，并根据条件给予不同的值
        weekday = calendar.weekday(year, month, day)
        if weekday in [0, 1, 3, 5]:  # Monday, Tuesday, Thursday, Saturday
            full_total += 3
            total_5_days += 3
        elif weekday in [2, 4]:  # Wednesday, Friday
            full_total += 1
        elif weekday == 6:  # Sunday
            full_total += 2
            total_5_days += 2

    return full_total, total_5_days

def get_total_welfare_of_7():
    pass

def get_total_welfare_of_6():
    pass

def get_total_welfare_of_5():
    pass

def get_welfare_Top_15():
    pass

def get_full_welfare_of_new_member():
    pass

def fetch_all_rows_as_json(query_result):
    # 构建 JSON 对象
    json_data = []
    for row in query_result:
        day = datetime.strptime
        full_total, total_5_days = calculate_current_month_total()
        row_dict = {
            'name': row[0],
            'date': row[1],
            'welfare_completed': row[2],
            'contribution': row[3],
            'less_completed_welfare': full_total - row[2],
            'full_completed_welfare': row[4],
            'completed_5_days_welfare': row[5],
            "total_welfare_of_5_days": total_5_days,
            "total_welfare": full_total
        }
        json_data.append(row_dict)

    return json_data

class MembersHandler(tornado.web.RequestHandler):
    def get(self):
        members = get_all_members_info()
        print(members)
        members = fetch_all_rows_as_json(members) # 转成json
        msg = {
            "code": 0,
            "msg": "success",
            "count": len(members),
            "data": members,
        }
        self.write(json.dumps(msg))

    def post(self):
        msg = json.loads(self.request.body)
        member_info = msg.get('info')
        full_total, total_5_days = calculate_current_month_total()
        name = member_info.get('name')
        join_date = member_info.get('join_date')
        contribution = int(member_info.get('contribution', 0))
        welfarenum = int(member_info.get('welfarenum', 0))
        insert_member_to_table((name, join_date, welfarenum, contribution, welfarenum == full_total, welfarenum >= total_5_days))
        self.write('')
        

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
    creat_table_by_sqlite()
    app = make_app()
    app.listen(8889)
    print('Server started')
    print('http://localhost:8889')
    tornado.ioloop.IOLoop.current().start()