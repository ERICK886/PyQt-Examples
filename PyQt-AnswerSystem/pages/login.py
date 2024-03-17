import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from .utils import *
from .home import Home

Database = Database()


class Login_UI(QWidget):
    def __init__(self):
        super().__init__()
        # 登录页布局
        self.layoutLogin = QVBoxLayout()
        self.layoutLogin.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layoutLogin)

        self.labelTitle = QLabel("登录考试答题系统")  # 登录页标题
        self.labelTitle.setStyleSheet(title_style)
        self.labelTitle.setAlignment(Qt.AlignCenter)
        self.layoutLogin.addWidget(self.labelTitle)

        # 登录框布局
        self.labelUsername = QLabel("用户名：")  # 登录框用户名标签
        self.labelUsername.setFont(QFont("宋体", 12))
        self.layoutLogin.addWidget(self.labelUsername)

        self.editUsername = QLineEdit()  # 登录框用户名输入框
        self.editUsername.setPlaceholderText("请输入用户名")
        self.layoutLogin.addWidget(self.editUsername)
        self.editUsername.setStyleSheet(form_control)
        self.editUsername.setFixedWidth(320)
        self.editUsername.setFixedHeight(50)

        self.labelPassword = QLabel("密码：")  # 登录框密码标签
        self.labelPassword.setFont(QFont("宋体", 12))
        self.layoutLogin.addWidget(self.labelPassword)

        self.editPassword = QLineEdit()  # 登录框密码输入框
        self.editPassword.setPlaceholderText("请输入密码")
        self.editPassword.setEchoMode(QLineEdit.Password)
        self.layoutLogin.addWidget(self.editPassword)
        self.editPassword.setStyleSheet(form_control)
        self.editPassword.setFixedWidth(320)
        self.editPassword.setFixedHeight(50)

        # 按钮布局
        self.layoutBtn = QHBoxLayout()
        self.layoutLogin.addLayout(self.layoutBtn)

        # 按钮设置
        self.btnLogin = QPushButton("登录")  # 登录按钮
        self.layoutBtn.addWidget(self.btnLogin)
        self.btnLogin.setStyleSheet(btn_primary)

        self.btnRegister = QPushButton("注册")  # 注册按钮
        self.layoutBtn.addWidget(self.btnRegister)
        self.btnRegister.setStyleSheet(btn_danger)

        self.btnExit = QPushButton("退出")  # 退出按钮
        self.layoutBtn.addWidget(self.btnExit)
        self.btnExit.setStyleSheet(btn_secondary)

        self.btnExit.setFixedSize(100, 35)
        self.btnRegister.setFixedSize(100, 35)
        self.btnLogin.setFixedSize(100, 35)


class Login(Login_UI):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.btnLogin.clicked.connect(self.login)  # 登录按钮点击事件连接到login函数
        self.btnRegister.clicked.connect(self.register)  # 注册按钮点击事件连接到register函数
        self.btnExit.clicked.connect(self.exit)  # 退出按钮点击事件连接到exit函数
        self.editUsername.returnPressed.connect(self.login)  # 输入框回车事件连接到login函数
        self.editPassword.returnPressed.connect(self.login)  # 输入框回车事件连接到login函数

    def login(self):
        users = Database.select_users()  # 从数据库中获取所有用户信息
        username = self.editUsername.text()  # 获取用户名输入框中的文本
        password = self.editPassword.text()  # 获取密码输入框中的文本
        if users:
            for user in users:
                if username and password:  # 如果用户名和密码均输入
                    if username == user['username'] and password == user['password']:  # 如果用户名和密码与数据库中的信息匹配
                        userfile = UserFile()  # 创建用户文件对象
                        nowUser = {  # 当前用户信息
                            'userid': user['userid'],
                            'username': username,
                            'password': password,
                        }
                        userfile.write(nowUser)  # 将当前用户信息写入用户文件
                        self.home = Home(self.stacked_widget)  # 创建主页对象
                        self.stacked_widget.addWidget(self.home)  # 将主页添加到堆栈布局中
                        self.stacked_widget.setCurrentIndex(2)  # 设置堆栈布局的当前索引为2
                        QMessageBox.information(self, "登录成功", "登录成功！")  # 弹出登录成功的提示框
                        break
            else:
                QMessageBox.warning(self, "登录失败", "用户名或密码错误！")  # 弹出登录失败的提示框
        else:
            QMessageBox.warning(self, "登录失败", "请先注册！")  # 弹出登录失败的提示框

    def register(self):
        self.stacked_widget.setCurrentIndex(1)  # 设置堆栈布局的当前索引为1，即显示注册页面

    def exit(self):
        sys.exit()  # 退出程序
