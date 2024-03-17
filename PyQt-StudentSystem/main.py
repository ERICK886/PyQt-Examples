import sys
from PyQt5.QtWidgets import QApplication, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, \
    QMessageBox, QDateEdit, QLabel, QWidget, QListWidget
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon
from manage import Data

data = Data()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('学生管理系统')  # 设置窗口标题
        self.setWindowIcon(QIcon('student.ico'))  # 设置窗口图标
        self.setFixedWidth(1000)
        self.initUI()

    def initUI(self):
        # 主窗口布局初始化
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.titleLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.titleLayout)
        self.title = QLabel('学生管理系统')  # 设置标题标签
        self.titleLayout.addWidget(self.title)
        self.titleLayout.setAlignment(Qt.AlignCenter)  # 设置标题标签对齐方式为居中对齐

        self.middleLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.middleLayout)
        self.leftlayout = QVBoxLayout()
        self.rightlayout = QVBoxLayout()
        self.middleLayout.addLayout(self.leftlayout)
        self.middleLayout.addLayout(self.rightlayout)

        self.leftlayout.setAlignment(Qt.AlignCenter)

        # 创建学号标签和文本编辑框
        self.labelSno = QLabel('学号')
        self.leftlayout.addWidget(self.labelSno)
        self.lineEditSno = QLineEdit()
        self.leftlayout.addWidget(self.lineEditSno)

        # 创建姓名标签和文本编辑框
        self.labelName = QLabel('姓名')
        self.leftlayout.addWidget(self.labelName)
        self.textEditName = QLineEdit()
        self.leftlayout.addWidget(self.textEditName)

        # 创建班级标签和下拉选择框
        self.labelClass = QLabel('班级')
        self.leftlayout.addWidget(self.labelClass)
        self.comboxClass = QComboBox()
        for k, v in data.get_classes().items():
            self.comboxClass.addItem(v)
        self.leftlayout.addWidget(self.comboxClass)

        # 创建性别标签和下拉选择框
        self.labelGender = QLabel('性别')
        self.leftlayout.addWidget(self.labelGender)
        self.comboxGender = QComboBox()
        self.leftlayout.addWidget(self.comboxGender)
        self.comboxGender.addItems(['男', '女'])

        # 创建出生日期标签和日期选择框
        self.labelBirthday = QLabel('出生日期')
        self.leftlayout.addWidget(self.labelBirthday)
        self.dateEditBirthday = QDateEdit()
        self.dateEditBirthday.setCalendarPopup(True)
        self.dateEditBirthday.setDate(QDate.currentDate())
        self.leftlayout.addWidget(self.dateEditBirthday)

        # 创建家庭住址标签和文本编辑框
        self.labelAddress = QLabel('家庭住址')
        self.leftlayout.addWidget(self.labelAddress)
        self.lineEditAddress = QLineEdit()
        self.leftlayout.addWidget(self.lineEditAddress)

        # 创建联系电话标签和文本编辑框
        self.labelPhone = QLabel('联系电话')
        self.leftlayout.addWidget(self.labelPhone)
        self.lineEditPhone = QLineEdit()
        self.leftlayout.addWidget(self.lineEditPhone)

        # 创建添加按钮，并连接点击事件
        self.btnAdd = QPushButton('添加')
        self.btnAdd.clicked.connect(self.add_student)
        self.leftlayout.addWidget(self.btnAdd)

        self.btnDelete = QPushButton('删除')
        self.btnDelete.clicked.connect(self.delete_student)
        self.leftlayout.addWidget(self.btnDelete)

        # 创建清空按钮，并连接点击事件
        self.btnClear = QPushButton('清空')
        self.btnClear.clicked.connect(self.clear_edits)
        self.leftlayout.addWidget(self.btnClear)

        self.listStudents = QListWidget()  # 创建一个可点击的列表小部件
        self.listStudents.setFixedWidth(640)
        self.rightlayout.addWidget(self.listStudents)  # 将列表小部件添加到布局中
        self.get_students()  # 获取学生信息

        # 创建退出按钮，并连接点击事件
        self.btnExit = QPushButton('退出')
        self.btnExit.clicked.connect(sys.exit)
        self.leftlayout.addWidget(self.btnExit)

    def add_student(self):
        '''
        添加学生信息
        '''
        if not self.lineEditSno.text() or not self.textEditName.text() or not self.comboxClass.currentText() \
                or not self.comboxGender.currentText() or not self.dateEditBirthday.date() \
                or not self.lineEditAddress.text() or not self.lineEditPhone.text():
            '''
            如果学生的必要信息填写不完整，则弹出警告窗口提醒用户填写完整信息
            '''
            QMessageBox.warning(self, '警告', '请将信息填写完整！')
        else:
            '''
            如果学生的必要信息填写完整，则调用data模块的insert_student函数插入学生信息，并根据返回结果进行相应处理
            '''
            res = data.insert_student(self.lineEditSno.text(), self.textEditName.text(),
                                      self.comboxClass.currentText(),
                                      self.lineEditPhone.text(),
                                      self.dateEditBirthday.date().toString('yyyy-MM-dd'),
                                      self.lineEditAddress.text(), self.comboxGender.currentText())
            if res == True:
                '''
                如果插入成功，则弹出提示窗口告知用户添加成功
                '''
                QMessageBox.information(self, '提示', '添加成功！')
                self.clear_edits()
                self.clear_tab1_students()
                self.get_students()

            else:
                '''
                如果插入失败，则弹出警告窗口告知用户添加失败并显示失败原因
                '''
                QMessageBox.warning(self, '警告', f'添加失败！{res}')
                self.clear_edits()
                self.clear_tab1_students()
                self.get_students()

    def clear_edits(self):
        # 清空第二个标签页的文本框中的内容
        self.lineEditSno.clear()
        # 清空第二个标签页的文本框中的内容
        self.textEditName.clear()
        # 设置第二个标签页的下拉框当前选中索引为0
        self.comboxClass.setCurrentIndex(0)
        # 设置第二个标签页的下拉框当前选中索引为0
        self.comboxGender.setCurrentIndex(0)
        # 设置第二个标签页的日期编辑框中的日期为当前日期
        self.dateEditBirthday.setDate(QDate.currentDate())
        # 清空第二个标签页的文本框中的内容
        self.lineEditAddress.clear()
        # 清空第二个标签页的文本框中的内容
        self.lineEditPhone.clear()

    def get_students(self):
        # 调用data模块的get_students函数获取学生信息
        self.clear_tab1_students()
        students = data.get_students()

        # 遍历每个学生信息
        for student in students:
            # 获取学生信息的各个字段
            sno = students[student]['学号']
            name = students[student]['姓名']
            class_ = students[student]['班级']
            gender = students[student]['性别']
            birthday = students[student]['生日']
            address = students[student]['地址']
            phone = students[student]['联系电话']

            # 将学生信息添加到列表控件listStudents中
            self.listStudents.addItem(
                # 将学号、姓名、班级、性别、生日、地址、电话拼接成字符串后添加到列表控件中
                str(sno) + '\t' + name + '\t' + class_ + '\t' + gender + '\t' + birthday + '\t' + address + '\t' + phone)

    def clear_tab1_students(self):
        # 清空学生信息表格
        self.listStudents.clear()
        # 添加列标题
        self.listStudents.addItem('学号\t姓名\t班级\t性别\t出生日期\t\t家庭住址\t联系电话')

    def delete_student(self):
        # 如果没有选中当前行，则弹出警告框提示用户选择要删除的行
        if not self.listStudents.currentRow():
            QMessageBox.warning(self, '警告', '请先选择要删除的行！')
        else:
            # 获取当前行的sno，使用制表符分割后取第一个元素
            sno = self.listStudents.currentItem().text().split('\t')[0]
            # 调用data模块中的delete_student函数，将sno作为参数传入，并将返回的结果赋给res变量
            res = data.delete_student(sno)
            # 如果res为True，则弹出提示框告知用户删除成功，并清空tab2中的学生信息，最后重新获取学生信息
            if res:
                QMessageBox.information(self, '提示', '删除成功！')
                self.clear_tab1_students()
                self.get_students()
            # 否则，弹出警告框告知用户删除失败，并将res的内容作为参数传入
            else:
                QMessageBox.warning(self, '警告', f'删除失败！{res}')


# 如果该脚本被作为主程序执行
if __name__ == '__main__':
    # 创建一个应用对象
    app = QApplication(sys.argv)
    # 设置窗口的宽度为720
    width = 720
    # 设置窗口的高度为480
    height = 480
    # 创建一个主窗口对象
    window = MainWindow()
    # 设置窗口的大小为指定的宽度和高度
    window.resize(width, height)
    # 显示窗口
    window.show()
    # 退出应用程序
    sys.exit(app.exec_())
