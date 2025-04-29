# import sqlite3
# import threading
#
#
# class DB:
#     def __init__(self):
#         self.local = threading.local()
#
#     def get_conn(self):
#         if not hasattr(self.local, 'conn'):
#             self.local.conn = sqlite3.connect('USERS_CHART.db', check_same_thread=False)
#             self.local.cursor = self.local.conn.cursor()
#         return self.local.conn, self.local.cursor
#
#     def initialize_database(self):
#         conn, cursor = self.get_conn()
#         cursor.execute('''
#             CREATE TABLE IF NOT EXISTS users (
#                 user_id INTEGER PRIMARY KEY,
#                 user_name TEXT NOT NULL UNIQUE,
#                 user_password TEXT NOT NULL,
#                 user_nickname TEXT NOT NULL
#             )
#         ''')
#         cursor.execute('SELECT COUNT(*) FROM users')
#         if cursor.fetchone()[0] == 0:
#             users = [
#                 (1, 'lily', '111111', 'sunny'),
#                 (2, 'mary', '222222', 'rainy'),
#                 (3, 'jack', '333333', 'winter')
#             ]
#             cursor.executemany('INSERT INTO users VALUES (?, ?, ?, ?)', users)
#             conn.commit()
#
#     def get_one(self, query, params=()):
#         conn, cursor = self.get_conn()
#         cursor.execute(query, params)
#         result = cursor.fetchone()
#         if not result:
#             return None
#         fields = [field[0] for field in cursor.description]
#         return dict(zip(fields, result))
#
#     def close(self):
#         if hasattr(self.local, 'conn'):
#             self.local.conn.close()
#             del self.local.conn
#             del self.local.cursor
#
#
# if __name__ == "__main__":
#     db = DB()
#     data=db.get_one('SELECT COUNT(*) FROM users WHERE user_name=?', ("jack",))
#     print(data)  # 首次运行输出数据，后续运行仍然存在
#     db.close()
#
#
#
# if __name__ == "__main__":
#     db = DB()
#     db.initialize_database()
#     # 测试用例
#     print("测试用户查询:")
#     print(db.get_user('jack'))  # 正常用户
#     print(db.get_user('not_exist'))  # 不存在的用户
#
#     db.close()

import sqlite3
import threading


class DB:
    def __init__(self):
        self.local = threading.local()


    def get_conn(self):
        if not hasattr(self.local, 'conn'):
            self.local.conn = sqlite3.connect('USERS_CHART.db', check_same_thread=False)
            self.local.cursor = self.local.conn.cursor()
        return self.local.conn, self.local.cursor

    def initialize_database(self):
        conn, cursor = self.get_conn()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS users
                       (
                           user_id
                           INTEGER
                           PRIMARY
                           KEY,
                           user_name
                           TEXT
                           NOT
                           NULL
                           UNIQUE,
                           user_password
                           TEXT
                           NOT
                           NULL,
                           user_nickname
                           TEXT
                           NOT
                           NULL
                       )
                       ''')
        # 更健壮的初始化检查
        cursor.execute('SELECT user_name FROM users WHERE user_name IN ("lily", "mary", "jack")')
        existing_users = [row[0] for row in cursor.fetchall()]

        users = [
            (1, 'lily', '111111', 'sunny'),
            (2, 'mary', '222222', 'rainy'),
            (3, 'jack', '333333', 'winter')
        ]
        insert_users = [u for u in users if u[1] not in existing_users]

        if insert_users:
            cursor.executemany("INSERT INTO users VALUES (?, ?, ?, ?)", insert_users)
            conn.commit()

    def get_one(self, query, params=()):
        conn, cursor = self.get_conn()
        cursor.execute(query, params)
        result = cursor.fetchone()
        if not result:
            return None
        fields = [field[0] for field in cursor.description]
        return dict(zip(fields, result))

    def add_user(self, username, password, nickname):
        conn, cursor = self.get_conn()

        cursor.execute('SELECT MAX(user_id) FROM users')
        max_id = cursor.fetchone()[0] or 0  # 当表为空时max_id会是None

        insert_data = (max_id + 1, username, password, nickname)

        cursor.execute(
            "INSERT INTO users (user_id, user_name, user_password, user_nickname) "
            "VALUES (?, ?, ?, ?)",
            insert_data
        )

        conn.commit()

    def close(self):
        if hasattr(self.local, 'conn'):
            self.local.conn.close()
            del self.local.conn
            del self.local.cursor


if __name__ == "__main__":
    # 正确的测试流程
    db = DB()
    db.initialize_database()  # 必须先初始化

    # 测试查询
    data = db.get_one('select * from (SELECT * FROM users WHERE user_name=?) "u*"', ("jack",))
    print("测试结果:", data)

    username="lucy"
    password="444444"
    nickname="summer"
    db.add_user(username,password,nickname)

    data = db.get_one('select * from (SELECT * FROM users WHERE user_name=?) "u*"', (username,))
    print("测试结果:", data)
    db.close()