
from socket import *
from config import *
import sys
from db import *


class Client:
    def __init__(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.running = False
        self.nickname = None
        self.username = None
        self.lock = threading.Lock()
        self.db=DB()

    def connect_server(self):
        try:
            self.sock.connect((SERVER_IP, SERVER_PORT))
        except Exception as e:
            print(f"连接服务器失败: {e}")
            sys.exit(1)

    def start_receiver(self):
        while self.running:
            try:
                data = self.sock.recv(1024).decode('utf-8')
                if not data:
                    self.stop()
                    return
                self.handle_message(data)
            except (ConnectionResetError, ConnectionAbortedError):
                self.stop()
                print("\n与服务器的连接已断开")
                return
            except Exception as e:
                print(f"\n接收数据错误: {e}")
                self.stop()

    def handle_message(self, data):
        parts = data.split('|')
        print(f"\n({parts[0]}): {parts[1]}")

    def send_message(self, message):
        with self.lock:
            try:
                self.sock.send(f"0002|{self.nickname}|{message}".encode('utf-8'))
            except Exception as e:
                print(f"发送消息失败: {e}")
                self.stop()

    def stop(self):
        self.running = False
        try:
            self.sock.close()
        except Exception as e:
            print(e)

    def register(self):
        username = input("新用户名：").strip()
        nickname = input("你的昵称").strip()
        sql = "SELECT *FROM users WHERE user_name=?"
        result = self.db.get_one(sql, (username,))
        password = input("密码：").strip()
        password1 = input("确认密码：").strip()
        if  not result:
            if password != password1:
                print("两次密码不一致，注册失败！")
                self.login_menu()
            else:
                self.db.add_user(username, password,nickname)
                print("注册成功！")
                print("--------注册成功--------")
                print("1.返回登录")
                print("2.退出系统")
                print("--------*******---------")
                choice = input("输入你的操作：")
                while True:
                    if choice == "1":
                        self.login_menu()
                        break
                    elif choice == "2":
                        exit()
                    else:
                        print("请输入有效选项")
        else:
            if username == result["user_name"]:
                print("该用户名已经存在，请重新注册！")
                self.register()

    def chat_session(self):
        self.running = True
        receiver = threading.Thread(target=self.start_receiver)
        receiver.daemon = True
        receiver.start()

        print("\n--- 聊天室界面 (输入'exit'退出) ---")
        while self.running:
            try:
                msg = input(">>> ")
                if msg.lower() == 'exit':
                    self.stop()
                    break
                else:
                    self.send_message(msg)
            except KeyboardInterrupt:
                self.stop()
                break

    def login(self):
        print("\n---------- 用户登录 -------------")
        while True:
            username = input("用户名: ").strip()
            password = input("密码: ").strip()

            self.sock.send(f"0001|{username}|{password}".encode('utf-8'))
            response = self.sock.recv(1024).decode('utf-8')

            if '|' in response and response.split('|')[1] == "登录成功":
                self.username = username
                self.nickname = response.split('|')[2]
                print(f"{self.username}登录成功！你的昵称为：{self.nickname}")
                return True
            else:
                print(f"\n登录失败: {response}")
                print("-------------登录失败---------------")
                print("a.重新登录")
                print("b.没有账号，返回注册")
                print("c.退出系统")
                print("------------***********------------")
                while True:
                    choice=input(">>> ").strip()
                    if choice == 'a':
                        self.login()
                        break
                    elif choice == 'b':
                        self.register()
                        break
                    elif choice == 'c':
                        exit()
                    else:
                        print("请输入正确的选项！")

    def main_menu(self):
        while True:
            print("\n---------- 主菜单 ----------")
            print("1. 进入聊天室")
            print("2. 退出系统")
            print("------------ ****** -----------")
            choice = input("请选择: ").strip()

            if choice == '1':
                self.chat_session()
                if not self.running:
                    break
            elif choice == '2':
                self.stop()
                print("正在退出.....")
                break
            else:
                print("无效的选项，请重新输入")

    def login_menu(self):
        print("------------聊天系统------------")
        print("1、登录")
        print("2、注册")
        print("3、退出")
        print("------------*******------------")
        n = input("输入你的选择：")
        if n == "1":
            if self.login():
                self.main_menu()
        elif n == "2":
            self.register()
        elif n == "3":
            exit()
        else:
            print("输入错误！！")
            self.login_menu()

    def run(self):
        try:
            self.connect_server()
            self.login_menu()
        finally:
            self.stop()


if __name__ == "__main__":
    client = Client()
    client.run()