# desc: 用于校园网登录的GUI程序
#author: chengzi
#date: 2023-9-29
#version: 1.0,非逆向版本,参数没加密直接传就行.
import sys
import json
import requests
import threading
import urllib.parse  # 导入urllib.parse模块
import configparser  # 导入configparser库
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox
class NetworkRequestApp(QMainWindow):
    # 定义用于更新 GUI 的自定义信号
    update_gui_signal = QtCore.pyqtSignal(str)
    request_success_signal = QtCore.pyqtSignal(str) # 定义请求成功的信号
    def __init__(self):
        super().__init__()
        # 创建一个configparser对象来处理配置信息
        self.config = configparser.ConfigParser()
        self.config.read('./config/config.ini')  # 读取配置文件

        self.setWindowTitle("校园网登录一键版")
        self.setGeometry(100, 100, 400, 300)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # 标题显示作者信息
        title_label = QLabel("Creat by chengzi", central_widget)
        layout.addWidget(title_label)

        # 用户名和密码输入
        username_label = QLabel("账号:", central_widget)
        self.username_input = QLineEdit(central_widget)
        password_label = QLabel("密码:", central_widget)
        self.password_input = QLineEdit(central_widget)
        self.password_input.setEchoMode(QLineEdit.Password)

        # 运营商选择
        carrier_label = QLabel("运营商:", central_widget)
        self.carrier_combo = QComboBox(central_widget)
        self.carrier_combo.addItems(["移动", "联通", "电信"])

        # QueryString输入
        query_string_label = QLabel("Query String:", central_widget)
        self.query_string_input = QLineEdit(central_widget)

        # 请求按钮
        self.request_button = QPushButton("发送请求", central_widget)
        self.request_button.clicked.connect(self.send_request)

        # 将界面元素添加到布局中
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(carrier_label)
        layout.addWidget(self.carrier_combo)
        layout.addWidget(query_string_label)
        layout.addWidget(self.query_string_input)
        layout.addWidget(self.request_button)
        
        # 在初始化时从配置文件中加载已保存的值
        self.load_saved_values()
        # 将自定义信号连接到更新 GUI 的插槽（方法）
        self.update_gui_signal.connect(self.update_gui)
    def update_gui(self, message):
        # 发出自定义信号时从主线程调用此方法
        QMessageBox.information(self, "请求结果", message)
        self.request_button.setEnabled(True)  # Enable the button

    def load_saved_values(self):
        # 从配置文件中加载已保存的值
        if 'UserInput' in self.config:
            user_input_section = self.config['UserInput']
            self.username_input.setText(user_input_section.get('username', ''))
            self.password_input.setText(user_input_section.get('password', ''))
            self.carrier_combo.setCurrentText(user_input_section.get('carrier', ''))
            self.query_string_input.setText(user_input_section.get('query_string', ''))
    def save_user_input(self):
        # 创建或更新配置文件
        if 'UserInput' not in self.config:
            self.config.add_section('UserInput')

        user_input_section = self.config['UserInput']
        user_input_section['username'] = self.username_input.text()
        user_input_section['password'] = self.password_input.text()
        user_input_section['carrier'] = self.carrier_combo.currentText()
        user_input_section['query_string'] = self.query_string_input.text()

        # 保存配置到文件
        with open('./config/config.ini', 'w') as config_file:
            print('保存配置完成')
            self.config.write(config_file)
    def send_request(self):
        self.request_button.setEnabled(False)  # 禁用按钮，避免重复点击

        # 创建请求线程并启动
        self.request_thread = threading.Thread(target=self.perform_request)
        self.request_thread.start()

    def perform_request(self):
        self.request_button.setEnabled(False)  # 禁用按钮，避免重复点击
        username = self.username_input.text()
        password = self.password_input.text()
        carrier = self.carrier_combo.currentText()
        query_string = self.query_string_input.text()
        # 对运营商进行URL编码
        encoded_carrier = urllib.parse.quote(carrier)
        encoded_carrier_url = encoded_carrier+'%E7%94%A8%E6%88%B7'
        retry_count = 3  # 重试次数
        success = False
        post_url ='http://222.179.99.144:8080/eportal/InterFace.do?method=login'

        for _ in range(retry_count):
            try:
                # 构建请求
                payload = {
                    'userId': username,
                    'password': password,
                    'service': encoded_carrier,
                    'operatorPwd':'',
                    'operatorUserId':'',
                    'validcode':'',
                    'passwordEncrypt':'false',
                    'queryString': query_string
                }
                headers={
                    'Host': '222.179.99.144:8080',
                    'Connection': 'keep-alive',
                    'Content-Length': '911',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.43',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Accept': '*/*',
                    'Origin': 'http://222.179.99.144:8080',
                    'Referer': f'http://222.179.99.144:8080/eportal/index.jsp?{query_string}',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                    # 'Cookie': 'EPORTAL_COOKIE_DOMAIN=false; EPORTAL_COOKIE_OPERATORPWD=; EPORTAL_COOKIE_SAVEPASSWORD=true; EPORTAL_AUTO_LAND=; EPORTAL_COOKIE_USERNAME=202021014010; EPORTAL_COOKIE_PASSWORD=4ca298406272bcc4650fa67a85ee5cc0f346f1c35e2945a065732a2e77895ff560a26651924c3065300cfbe48d5792d368777156e21b20a218a1ef75c90bc74708d0fec84e0376342b0393814e363965d160b429d851eb476caab2dcdedb4c2b879ec1245399f4a4547b5efddb6eb51827aa10138de71a0151c9687f0b2d9dd7; EPORTAL_COOKIE_SERVER=%E7%A7%BB%E5%8A%A8; EPORTAL_COOKIE_SERVER_NAME=%E7%A7%BB%E5%8A%A8%E7%94%A8%E6%88%B7; EPORTAL_USER_GROUP=2023%E7%BA%A7%E6%96%B0%E7%94%9F; JSESSIONID=0DE8EFCF153A9D74E91DB2A51F07D24A',
                    'Cookie': f'EPORTAL_COOKIE_DOMAIN=false; EPORTAL_COOKIE_OPERATORPWD=; EPORTAL_COOKIE_SAVEPASSWORD=true; EPORTAL_AUTO_LAND=; EPORTAL_COOKIE_SERVER={encoded_carrier}; EPORTAL_COOKIE_SERVER_NAME={encoded_carrier_url}; EPORTAL_COOKIE_USERNAME={username}; EPORTAL_COOKIE_PASSWORD={password}; EPORTAL_USER_GROUP=2023%E7%BA%A7%E6%96%B0%E7%94%9F',
                    }
                response = requests.post(url=post_url, headers =headers, params=payload) 

                # 检查响应状态码
                if response.status_code == 200:
                    success = True
                    response.encoding = 'utf-8' 
                    res = json.loads(response.text)
                    print(res)
                    res_msg = json.dumps(res, indent=4, ensure_ascii=False)
                    # print('2',res_msg)

                    # QMessageBox.information(self, "返回结果", res_msg)
                    # self.request_success_signal.emit(res)

                    # QMessageBox.information(self, "请求成功", "请求已发送并成功完成")
                    break  # 请求成功，跳出重试循环
                else:
                    # 处理其他状态码，例如404、500等
                    QMessageBox.warning(self, "请求错误", f"HTTP错误：{response.status_code}")
            except Exception as e:
                # 处理异常，例如请求超时、网络异常等
                QMessageBox.warning(self, "请求错误", f"发生异常：{str(e)}")

        if success:
            # 请求成功，显示成功消息
            # Request was successful, emit the custom signal to update the GUI
            self.update_gui_signal.emit("登录成功")
            # QMessageBox.information(self, "请求成功", "请求已发送并成功完成")
            # self.request_success_signal.emit(res_msg)
        self.request_button.setEnabled(True)  # 启用按钮
        # 保存用户输入的值到配置文件
        self.save_user_input()
        self.request_success_signal.connect(self.on_request_success)

    def on_request_success(self, msg):
        QMessageBox.information(self, "结果", msg)
    def show_request_success(self, message):
        # 在主线程中显示成功消息
        self.run_in_main_thread(lambda: QMessageBox.information(self, "请求成功", message))

    def show_request_error(self, message):
        # 在主线程中显示错误消息
        self.run_in_main_thread(lambda: QMessageBox.warning(self, "请求错误", message))

    def run_in_main_thread(self, func):
        # 在主线程中执行函数
        self.run_in_main_thread_callback(func)
    def on_request_success(self, msg):
        QMessageBox.information(self, "结果", msg)

    def run_in_main_thread_callback(self, func):
        # 用于在主线程中回调执行函数
        QtCore.QMetaObject.invokeMethod(self, func)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open("./style/style.qss", "r",encoding="utf-8") as f:
        app.setStyleSheet(f.read())
    window = NetworkRequestApp()
    window.show()
    sys.exit(app.exec_())
