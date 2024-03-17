import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from .utils import *

Database = Database()  # 创建数据库对象

class Register_UI(QWidget):
    def __init__(self):
        super().__init__()

        # 注册布局
        self.layoutRegister = QVBoxLayout()
        self.layoutRegister.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layoutRegister)

        # 注册标题
        self.labelTitle = QLabel("注册")
        self.labelTitle.setStyleSheet(title_style)
        self.labelTitle.setAlignment(Qt.AlignCenter)
        self.layoutRegister.addWidget(self.labelTitle)

        # 注册框内容
        self.labelUsername = QLabel("用户名：")
        self.layoutRegister.addWidget(self.labelUsername)
        self.lineEditUsername = QLineEdit()
        self.layoutRegister.addWidget(self.lineEditUsername)
        self.lineEditUsername.setPlaceholderText("请输入用户名")
        self.lineEditUsername.setFixedWidth(320)
        self.lineEditUsername.setFixedHeight(35)

        self.labelPassword = QLabel("密码：")
        self.layoutRegister.addWidget(self.labelPassword)
        self.lineEditPassword = QLineEdit()
        self.lineEditPassword.setEchoMode(QLineEdit.Password)
        self.layoutRegister.addWidget(self.lineEditPassword)
        self.lineEditPassword.setPlaceholderText("请输入密码")
        self.lineEditPassword.setFixedWidth(320)
        self.lineEditPassword.setFixedHeight(35)

        self.labelConfirmPassword = QLabel("确认密码：")
        self.layoutRegister.addWidget(self.labelConfirmPassword)
        self.lineEditConfirmPassword = QLineEdit()
        self.lineEditConfirmPassword.setEchoMode(QLineEdit.Password)
        self.layoutRegister.addWidget(self.lineEditConfirmPassword)
        self.lineEditConfirmPassword.setPlaceholderText("请再次输入密码")
        self.lineEditConfirmPassword.setFixedWidth(320)
        self.lineEditConfirmPassword.setFixedHeight(35)

        self.labelName = QLabel("姓名：")
        self.layoutRegister.addWidget(self.labelName)
        self.lineEditName = QLineEdit()
        self.layoutRegister.addWidget(self.lineEditName)
        self.lineEditName.setPlaceholderText("请输入姓名")
        self.lineEditName.setFixedWidth(320)
        self.lineEditName.setFixedHeight(35)

        self.labelEmail = QLabel("邮箱：")
        self.layoutRegister.addWidget(self.labelEmail)
        self.lineEditEmail = QLineEdit()
        self.layoutRegister.addWidget(self.lineEditEmail)
        self.lineEditEmail.setPlaceholderText("请输入邮箱")
        self.lineEditEmail.setFixedWidth(320)
        self.lineEditEmail.setFixedHeight(35)

        self.labelPhone = QLabel("电话：")
        self.layoutRegister.addWidget(self.labelPhone)
        self.lineEditPhone = QLineEdit()
        self.layoutRegister.addWidget(self.lineEditPhone)
        self.lineEditPhone.setPlaceholderText("请输入电话")
        self.lineEditPhone.setFixedWidth(320)
        self.lineEditPhone.setFixedHeight(35)

        self.labelSex = QLabel("性别：")
        self.layoutRegister.addWidget(self.labelSex)
        self.comboBoxSex = QComboBox()
        self.comboBoxSex.addItem("男")
        self.comboBoxSex.addItem("女")
        self.layoutRegister.addWidget(self.comboBoxSex)
        self.comboBoxSex.setFixedWidth(320)
        self.comboBoxSex.setFixedHeight(35)

        self.labelClass = QLabel("班级：")
        self.layoutRegister.addWidget(self.labelClass)
        self.lineEditClass = QLineEdit()
        self.layoutRegister.addWidget(self.lineEditClass)
        self.lineEditClass.setPlaceholderText("请输入班级")
        self.lineEditClass.setFixedWidth(320)
        self.lineEditClass.setFixedHeight(35)

        self.layoutBtn = QHBoxLayout()
        self.layoutRegister.addLayout(self.layoutBtn)

        self.btnRegister = QPushButton("注册")
        self.layoutBtn.addWidget(self.btnRegister)
        self.btnRegister.setStyleSheet(btn_primary)
        self.btnRegister.setFixedWidth(100)
        self.btnRegister.setFixedHeight(35)

        self.bntBack = QPushButton("返回")
        self.layoutBtn.addWidget(self.bntBack)
        self.bntBack.setStyleSheet(btn_secondary)
        self.bntBack.setFixedWidth(100)
        self.bntBack.setFixedHeight(35)

class Register(Register_UI):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.btnRegister.clicked.connect(self.register)
        self.bntBack.clicked.connect(self.back)

    def register(self):
        """
        注册函数
        """
        username = self.lineEditUsername.text()
        password = self.lineEditPassword.text()
        confirm_password = self.lineEditConfirmPassword.text()
        if password == confirm_password:
            name = self.lineEditName.text()
            email = self.lineEditEmail.text()
            phone = self.lineEditPhone.text()
            sex = self.comboBoxSex.currentText()
            class_ = self.lineEditClass.text()
            if username and password and name and email and phone and sex and class_:
                if Database.insert_user(username, password, name, email, phone, sex, class_):
                    QMessageBox.information(self, "提示", "注册成功")
                    self.stacked_widget.setCurrentIndex(0)
                else:
                    QMessageBox.warning(self, "警告", "注册失败，请检查用户名是否已被注册")
            else:
                QMessageBox.warning(self, "警告", "请填写完整信息")
        else:
            QMessageBox.warning(self, "警告", "两次输入的密码不一致")
            self.lineEditPassword.clear()
            self.lineEditConfirmPassword.clear()

    def back(self):
        """
        返回函数
        """
        self.stacked_widget.setCurrentIndex(0)
