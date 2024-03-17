import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from .utils import *

Database = Database()


class Answer_UI(QWidget):
    def __init__(self):
        super().__init__()
        self.layoutAnswer = QVBoxLayout()  # 垂直布局管理器，用于排列问题和答案
        self.setLayout(self.layoutAnswer)
        self.examfile = ExamFile()  # 考试文件对象
        self.layoutHeader = QHBoxLayout()  # 水平布局管理器，用于排列标题
        self.labelTitle = QLabel()  # 标题标签
        self.layoutHeader.addWidget(self.labelTitle)
        self.labelTitle.setStyleSheet(title_style)  # 设置标题样式
        self.layoutHeader.setAlignment(Qt.AlignCenter)  # 设置标题水平居中
        self.layoutAnswer.addLayout(self.layoutHeader)  # 将标题布局添加到答案布局

        self.layoutQuestion = QVBoxLayout()  # 垂直布局管理器，用于排列问题
        self.layoutAnswer.addLayout(self.layoutQuestion)
        self.labelOrder = QLabel()  # 问题序号标签
        self.labelOrder.setStyleSheet(h4)  # 设置问题序号标签样式
        self.layoutQuestion.addWidget(self.labelOrder)
        self.labelQuestion = QLabel()  # 问题标签
        self.labelQuestion.setStyleSheet(h4)  # 设置问题标签样式
        self.layoutQuestion.addWidget(self.labelQuestion)
        self.layoutAnswer.addStretch()  # 添加伸缩占位符

        self.layoutFooter = QHBoxLayout()  # 水平布局管理器，用于排列按钮
        self.btnBack = QPushButton("上一题")  # 返回上一题按钮
        self.btnNext = QPushButton("下一题")  # 下一题按钮
        self.btnSave = QPushButton("保存")  # 保存按钮
        self.btnFinish = QPushButton("完成")  # 完成按钮
        self.layoutFooter.addWidget(self.btnBack)
        self.layoutFooter.addWidget(self.btnNext)
        self.layoutFooter.addWidget(self.btnSave)
        self.layoutFooter.addWidget(self.btnFinish)
        self.btnNext.setStyleSheet(btn_primary)  # 设置下一题按钮样式
        self.btnBack.setStyleSheet(btn_secondary)  # 设置返回上一题按钮样式
        self.btnSave.setStyleSheet(btn_danger)  # 设置保存按钮样式
        self.btnFinish.setStyleSheet(btn_success)  # 设置完成按钮样式
        self.btnNext.setFixedSize(100, 35)  # 设置下一题按钮固定大小
        self.btnBack.setFixedSize(100, 35)  # 设置返回上一题按钮固定大小
        self.btnSave.setFixedSize(100, 35)  # 设置保存按钮固定大小
        self.btnFinish.setFixedSize(100, 35)  # 设置完成按钮固定大小
        self.layoutFooter.setAlignment(Qt.AlignCenter)  # 设置按钮水平居中
        self.layoutAnswer.addLayout(self.layoutFooter)  # 将按钮布局添加到答案布局



class Answer(Answer_UI):
    def __init__(self, examData, stacked_widget, order, length, id, stackedDict):
        super().__init__()
        self.examData = dict(examData)  # 将examData转化为字典类型并赋值给self.examData变量
        self.stackedDict = stackedDict  # 将stackedDict赋值给self.stackedDict变量
        self.id = id  # 将id赋值给self.id变量
        self.order = order  # 将order赋值给self.order变量
        self.length = length  # 将length赋值给self.length变量
        self.stackedWidget = stacked_widget  # 将stacked_widget赋值给self.stackedWidget变量
        self.checkAnswer = None  # 初始化self.checkAnswer变量为None
        self.filethread = None  # 初始化self.filethread变量为None
        self.showQuestion()  # 调用showQuestion函数
        self.btnBack.clicked.connect(self.back)  # 当btnBack按钮被点击时，调用back函数
        self.btnNext.clicked.connect(self.next)  # 当btnNext按钮被点击时，调用next函数
        self.btnFinish.clicked.connect(self.finish)  # 当btnFinish按钮被点击时，调用finish函数


    def showQuestion(self):
        # 显示题目信息
        self.labelOrder.setText(f"{self.examData['title']}（{self.examData['score']}）分")
        # 显示题目描述
        self.labelQuestion.setText(self.examData["info"])
        # 显示题目类型
        self.labelTitle.setText(self.examData['type'])

        # 题目类型为单选题
        if self.examData['type'] == "单选题":
            # 初始化答案
            self.answer = ''
            # 创建单选按钮字典
            radioDic = {}
            # 遍历单选按钮字典
            for k, v in eval(self.examData['radio']).items():
                radioDic[k] = {}
                # 创建单选按钮
                radioDic[k] = QRadioButton(f"{k}. {v}")
                radioDic[k].setStyleSheet(radio_style)
                radioDic[k].setFixedSize(400, 20)
                # 连接单选按钮的切换信号与槽函数
                radioDic[k].toggled.connect(self.radioChecks)
                # 将单选按钮添加到布局中
                self.layoutQuestion.addWidget(radioDic[k])
        # 题目类型为多选题
        elif self.examData['type'] == "多选题":
            # 初始化答案
            self.answer = []
            # 创建复选框字典
            checkDic = {}
            # 遍历复选框字典
            for k, v in eval(self.examData['check']).items():
                checkDic[k] = {}
                # 创建复选框
                checkDic[k] = QCheckBox(f"{k}. {v}")
                checkDic[k].setStyleSheet(check_style)
                checkDic[k].setFixedSize(400, 20)
                # 连接复选框的状态变化信号与槽函数
                checkDic[k].stateChanged.connect(self.checkChecks)
                # 将复选框添加到布局中
                self.layoutQuestion.addWidget(checkDic[k])


    def radioChecks(self, checked):
        # 当单选题的radio按钮被选中时触发
        if checked:
            btn = self.sender()
            msg = btn.text().split('. ')
            self.answer = msg[0]

    def checkChecks(self, checked):
        # 当多选题的checkbox被选中或取消选中时触发
        if checked == Qt.Checked:
            btn = self.sender()
            msg = btn.text().split('. ')
            self.answer.append(msg[0])
        else:
            btn = self.sender()
            msg = btn.text().split('. ')
            if msg[0] in self.answer:
                self.answer.remove(msg[0])

    def next(self):
        current_index = self.stackedWidget.currentIndex()  # 获取当前界面的索引
        stacklenth = self.stackedWidget.count()  # 获取界面栈的长度

        # 判断当前界面是否为最后一题
        if current_index < stacklenth - 1:
            if self.examData['type'] == "单选题":  # 判断题型为单选题
                if self.answer == '':  # 判断答案是否为空
                    QMessageBox.information(self, "提示", "请选择答案")  # 显示提示消息框，提示用户选择答案
                    return  # 返回上一个界面
                else:
                    self.stackedWidget.setCurrentIndex(current_index + 1)  # 显示下一题界面
            elif self.examData['type'] == "多选题":  # 判断题型为多选题
                if self.answer == []:  # 判断答案是否为空
                    QMessageBox.information(self, "提示", "请选择答案")  # 显示提示消息框，提示用户选择答案
                    return  # 返回上一个界面
                else:
                    self.stackedWidget.setCurrentIndex(current_index + 1)  # 显示下一题界面

            self.examfile.write_exam(self.answer, self.order)  # 将答案和题目编号写入考试文件
            self.checkAnswer = CheckExamThread(self.examData, self.answer)  # 创建检查试卷的线程
            self.checkAnswer.signal.connect(self.getscore)  # 连接检查试卷线程的得分信号
            self.checkAnswer.start()  # 启动检查试卷的线程

        else:
            QMessageBox.information(self, "提示", "这是最后一题")  # 显示提示消息框，提示用户这是最后一题


    def back(self):
        current_index = self.stackedWidget.currentIndex()  # 获取当前下标
        if current_index > 3:  # 如果下标大于3
            self.stackedWidget.setCurrentIndex(current_index - 1)  # 切换到前一个页面
        else:  # 否则
            QMessageBox.information(self, "提示", "这是第一题")  # 弹出提示框，显示“这是第一题”


    def finish(self):
        # 读取考试文件内容
        data = self.examfile.read()
        # 打印数据
        print(data)
        # 如果数据不为空
        if data != {}:
            # 弹出提示框询问是否提交答案
            QMessageBox.question(self, "提示", "是否提交答案", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            # 如果点击了是
            if QMessageBox.Yes == QMessageBox.Yes:
                # 写入答案到考试文件
                self.examfile.write_exam(self.answer, self.order)
                # 创建检查答案的线程
                self.checkAnswer = CheckExamThread(self.examData, self.answer)
                # 连接检查答案线程的信号与回调函数
                self.checkAnswer.signal.connect(self.getscore)
                # 启动检查答案的线程
                self.checkAnswer.start()
                # 获取当前用户ID
                self.userid = int(UserFile().read()['userid'])
                # 更新数据库中用户的考试状态为完成
                Database.update_exam_con_by_userid_examid(self.userid, self.id, 1)
                # 移除堆栈布局中的所有页面
                for i in range(len(self.stackedDict)):
                    self.stackedWidget.removeWidget(self.stackedDict[i + 1])
                # 计算总分数
                sum = 0
                for i in data['exam']:
                    sum = sum + int(data['exam'][i]['score'])
                # 更新数据库中用户的考试分数
                Database.update_exam_score_by_userid_examid(self.userid, self.id, sum)
                # 设置堆栈布局的当前索引为3
                self.stackedWidget.setCurrentIndex(2)
            else:
                pass
        else:
            # 弹出提示框提示先作答
            QMessageBox.information(self, "提示", "请先作答")


    def getscore(self, boolean):
        # 获取成绩
        if boolean:
            score = self.examData['score']
            self.examfile.write_score(score, self.order)
        else:
            score = 0
            self.examfile.write_score(score, self.order)
