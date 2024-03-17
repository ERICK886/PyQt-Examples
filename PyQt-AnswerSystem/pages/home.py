import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
import time
from PyQt5.QtCore import Qt, QTimer
from .utils import *
from .answer import *


class Home_UI(QWidget):
    def __init__(self):
        super().__init__()
        self.topLevel = QDialog(self)
        # 创建主窗口布局
        self.layoutWindow = QVBoxLayout()
        self.setLayout(self.layoutWindow)

        # 创建头部组件布局
        self.layoutHeader = QHBoxLayout()

        # 添加头部组件
        self.labelWelcome = QLabel("欢迎使用考试答题系统")
        self.labelWelcome.setStyleSheet(title_style)
        self.labelWelcome.setAlignment(Qt.AlignCenter)
        self.layoutHeader.addWidget(self.labelWelcome)
        self.layoutWindow.addLayout(self.layoutHeader)

        # 创建中间布局
        self.layoutBody = QHBoxLayout()
        self.layoutWindow.addLayout(self.layoutBody)

        # 创建左侧布局
        self.layoutListExams0 = QVBoxLayout()
        self.layoutBody.addLayout(self.layoutListExams0)
        # 创建右侧布局
        self.layoutListExams1 = QVBoxLayout()
        self.layoutBody.addLayout(self.layoutListExams1)

        # 添加左侧布局中的考试列表标签和标题
        self.labelExams0 = QLabel("我未完成的考试")
        self.labelExams0.setStyleSheet(h4)
        self.layoutListExams0.addWidget(self.labelExams0)
        # 添加右侧布局中的考试列表标签和标题
        self.labelExams1 = QLabel("我完成的考试")
        self.labelExams1.setStyleSheet(h4)
        self.layoutListExams1.addWidget(self.labelExams1)

        # 添加左侧布局和右侧布局中的考试列表组件
        self.listExams0 = QListWidget(self)
        self.layoutListExams0.addWidget(self.listExams0)
        self.listExams1 = QListWidget(self)
        self.layoutListExams1.addWidget(self.listExams1)

        # 添加开始答题按钮
        self.btnStart = QPushButton("开始答题")
        self.setStyleSheet(btn_primary)
        self.layoutBody.addWidget(self.btnStart)
        self.btnStart.setFixedWidth(100)
        self.btnStart.setFixedHeight(30)

        # 创建底部布局
        self.layoutFooter = QHBoxLayout()
        self.labelTime = QLabel()
        self.layoutFooter.addWidget(self.labelTime)
        self.layoutWindow.addLayout(self.layoutFooter)
        self.layoutFooter.addStretch()

        # 添加刷新按钮
        self.btnFresh = QPushButton("刷新")
        self.btnFresh.setStyleSheet(btn_success)
        # 添加退出按钮
        self.btnExit = QPushButton("退出")
        self.btnExit.setStyleSheet(btn_secondary)
        self.btnFresh.setFixedWidth(100)
        self.btnFresh.setFixedHeight(30)
        self.btnExit.setFixedWidth(100)
        self.btnExit.setFixedHeight(30)
        self.layoutFooter.addWidget(self.btnFresh)
        self.layoutFooter.addWidget(self.btnExit)


class Home(Home_UI):
    def __init__(self, stacked_widget):
        super().__init__()
        self.userid = int(UserFile().read()['userid'])
        self.selectExam = None
        self.stacked_widget = stacked_widget
        self.get_user_exams(self.userid)
        self.btnExit.clicked.connect(self.exit)
        self.btnStart.clicked.connect(self.start_exam)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.listExams0.itemClicked.connect(self.exam_selected0)
        self.listExams1.itemClicked.connect(self.exam_selected1)
        self.btnFresh.clicked.connect(self.fresh)

    def fresh(self):
        # 清空左侧和右侧的考试列表
        for i in range(self.listExams0.count()):
            self.listExams0.takeItem(0)

        for i in range(self.listExams1.count()):
            self.listExams1.takeItem(0)
        self.get_user_exams(self.userid)



    def get_user_exams(self, userid):
        # 从数据库中获取用户考试信息
        exams = Database.select_user_exam(userid)
        for exam in exams:
            if exam['con'] == 0:
                # 构造考试信息并添加到左侧列表
                item = f"{exam['e.examid']}   {exam['examname']}    ({exam['examstart'].strftime('%m/%d %H:%M:%S')}-{exam['examend'].strftime('%m/%d %H:%M:%S')})    {exam['examtype']}"
                self.listExams0.addItem(item)
            elif exam['con'] == 1:
                # 构造考试信息并添加到右侧列表
                item = f"{exam['e.examid']}   {exam['examname']}    ({exam['examstart'].strftime('%m/%d %H:%M:%S')}-{exam['examend'].strftime('%m/%d %H:%M:%S')})    {exam['examtype']}    已完成   得分{exam['score']}"
                self.listExams1.addItem(item)

    def update_time(self):
        # 更新当前时间显示
        self.labelTime.setText("当前时间：" + time.strftime("%Y-%m-%d %H:%M:%S"))

    def exam_selected0(self):
        selected_items = self.listExams0.selectedItems()  # 获取被选择的列表项
        for item in selected_items:
            # 获取考试信息并开始考试
            examid = int(item.text().split('   ')[0])
            self.selectExam = self.getExam(examid)

    def exam_selected1(self):
        selected_items = self.listExams1.selectedItems()  # 获取被选择的列表项
        for item in selected_items:
            # 获取考试信息并开始考试
            examid = int(item.text().split('   ')[0])
            self.selectExam = self.getExam(examid)

    def getExam(self, examid):
        # 从数据库中获取考试信息
        exam = Database.select_user_exam_by_id(examid)
        return exam

    def start_exam(self):
        if self.selectExam:
            if self.selectExam['con'] == 0 or self.selectExam['con'] == 2:
                # 初始化考试信息和答案组件
                self.stackedDict = {}
                self.examData = Database.select_questions_by_examid(self.selectExam['examid'])
                length = len(self.examData)
                examfile = ExamFile()
                read = {'exam': {}, 'score': 0}
                for i in range(length):
                    read['exam'][str(i + 1)] = {}
                    read['exam'][str(i + 1)]['question'] = None
                    read['exam'][str(i + 1)]['score'] = 0
                examfile.write(read)

                i = 0
                for question in self.examData:
                    i += 1
                    if question:
                        order = i
                        self.stackedDict[i] = Answer(question, self.stacked_widget, order, length, self.selectExam['examid'], self.stackedDict)
                        self.stacked_widget.addWidget(self.stackedDict[i])
                self.stacked_widget.setCurrentIndex(3)
            elif self.selectExam['con'] == 1:
                QMessageBox.information(None, "提示", "您已完成该考试")
        else:
            QMessageBox.information(None, "提示", "请选择考试")

    def exit(self):
        # 退出程序
        sys.exit()
