import threading
from socket import *
from config import *
from db import DB


class server:
    def __init__(self):
        self.soc = socket(AF_INET, SOCK_STREAM)
        self.soc.bind((SERVER_IP, SERVER_PORT))
        self.soc.listen(128)

        self.client = {}
        self.client_socs = []
        self.db = DB()
        self.db.initialize_database()

    def start_server(self):
        while True:
            print("正在获取客户端连接......")
            soc1, addr = self.soc.accept()
            print(f"新的客户端上线：{addr}")
            t = threading.Thread(target=self.request_hand, args=(soc1,))
            t.start()

    def request_hand(self, soc1):
        while True:
            try:
                recv_data = soc1.recv(512).decode('utf-8')
                if not recv_data:
                    self.outline_client(soc1)
                    break
                else:
                    parse_data = self.parse_recv_data(recv_data)
                    if parse_data['request_id'] == REQUEST_LOGIN:
                        self.handle_login(soc1, parse_data)
                    if parse_data['request_id'] == REQUEST_CHART:
                        self.handle_chart(soc1, parse_data)
            except Exception as e:
                print(e)
                break


    def parse_recv_data(self, recv_data):
        print("解析客户端数据：" + recv_data)
        request_list = recv_data.split("|")
        request_data = {'request_id': request_list[0]}

        if request_data['request_id'] == REQUEST_LOGIN:
            request_data['username'] = request_list[1]
            request_data['password'] = request_list[2]
        elif request_data['request_id'] == REQUEST_CHART:
            request_data['nickname'] = request_list[1]
            request_data['message'] = request_list[2]
        return request_data

    def outline_client(self, client_soc):
        for username, info in self.client.items():
            if info['socket'] == client_soc:
                mas = f"{self.client[username]['username']}已下线..."
                self.broad_cast(mas)
                client_soc.close()
                del self.client[username]
                break

    def check_login(self, username, password):
        sql = "SELECT *FROM users WHERE user_name=?"
        result = self.db.get_one(sql, (username,))
        if not result:
            return "0", "", ""
        if password == result["user_password"]:
            return "1", result["user_name"], result["user_nickname"]
        else:
            return "2", "", ""

    def handle_login(self, client_soc, request_data):
        print("收到登录请求，准备登录....")

        username = request_data["username"]
        password = request_data["password"]

        ret, username, nickname = self.check_login(username, password)

        if ret == "0":
            mas = "该用户不存在！"
            client_soc.send(mas.encode('utf-8'))
        elif ret == "1":
            self.client[username] = {
                'socket': client_soc,
                'username': username,
                'nickname': nickname,
            }
            for info in self.client.values():
                self.client_socs.append(info['socket'])
            mas = request_data['username'] + "|" + "登录成功" + "|" + nickname
            client_soc.send(mas.encode('utf-8'))
        elif ret == "2":
            mas = "用户名或密码输入错误！"
            client_soc.send(mas.encode('utf-8'))

    def handle_chart(self, soc1, request_data):
        print("收到聊天请求...")
        print(request_data)
        nickname = request_data['nickname']
        message = request_data['message']

        mas = nickname + "|" + message


        soc1.send(mas.encode('utf-8'))
        if len(self.client_socs) > 1:
            self.broad_cast(mas)
        print("消息已转发！")

    def broad_cast(self, mas):
        for i in range(len(self.client_socs)):
            soc = self.client_socs[i]
            soc.send(mas.encode('utf-8'))


if __name__ == "__main__":
    s = server()
    s.start_server()
