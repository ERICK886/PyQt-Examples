import sys
from PyQt5.QtWidgets import QApplication, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, \
    QMessageBox, QDesktopWidget, QLabel, QWidget, QDateTimeEdit, QListWidget
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon
from tools import *

sql_manage = SqlData()


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.title = '记账管理系统'
        self.ico = 'reward.ico'
        self.setFixedSize(window_width, window_height)
        qr = self.frameGeometry()  # 获取窗口的几何信息
        cp = QDesktopWidget().availableGeometry().center()  # 获取桌面的可用几何信息的中心点
        qr.moveCenter(cp)  # 移动窗口的中心点到桌面的可用几何信息的中心点
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(self.ico))
        self.layoutRward = QVBoxLayout()
        self.setLayout(self.layoutRward)

        self.layoutTitle = QHBoxLayout()
        self.labelTitle = QLabel('记账管理系统')
        self.labelTitle.setAlignment(Qt.AlignCenter)
        self.layoutTitle.addWidget(self.labelTitle)
        self.layoutRward.addLayout(self.layoutTitle)

        self.layoutEdit = QHBoxLayout()

        self.editIncome = QLineEdit()
        self.editExpense = QLineEdit()
        self.editDatetime = QDateTimeEdit()
        self.comboxClassify = QComboBox()
        self.btnAdd = QPushButton('添加账务')
        self.btnAdd.clicked.connect(self.addReward)
        self.editIncome.setPlaceholderText('收入')
        self.editExpense.setPlaceholderText('支出')
        self.editIncome.setFixedSize(80, 25)
        self.editExpense.setFixedSize(80, 25)
        self.editDatetime.setFixedSize(180, 25)
        self.btnAdd.setFixedSize(100, 25)
        self.comboxClassify.addItem('生活支出')
        self.comboxClassify.addItem('生活收入')
        self.comboxClassify.addItem('娱乐支出')
        self.comboxClassify.addItem('娱乐收入')
        self.comboxClassify.addItem('学习支出')
        self.comboxClassify.addItem('学习收入')
        self.comboxClassify.addItem('交通支出')
        self.comboxClassify.addItem('交通收入')
        self.comboxClassify.addItem('其他支出')
        self.comboxClassify.addItem('其他收入')
        self.editDatetime.setMinimumDate(QDate.currentDate().addDays(-365))
        self.editDatetime.setMaximumDate(QDate.currentDate().addDays(365))
        self.editDatetime.setDisplayFormat('yyyy-MM-dd HH:mm:ss')
        self.layoutEdit.addWidget(self.editIncome)
        self.layoutEdit.addWidget(self.editExpense)
        self.layoutEdit.addWidget(self.editDatetime)
        self.layoutEdit.addWidget(self.comboxClassify)
        self.layoutEdit.addWidget(self.btnAdd)
        self.layoutRward.addLayout(self.layoutEdit)

        self.layoutList = QHBoxLayout()
        self.listReward = QListWidget()
        self.listReward.addItem('收入\t支出\t分类\t创建时间\t\t更新时间')

        self.layoutList.addWidget(self.listReward)
        self.layoutRward.addLayout(self.layoutList)

        self.layoutFooter = QHBoxLayout()
        self.btnShow = QPushButton('删除账务')
        self.btnShow.clicked.connect(self.deleteReward)
        self.layoutRward.addWidget(self.btnShow)
        self.layoutRward.addLayout(self.layoutFooter)
        self.getReward()

    def clearList(self):
        for i in range(self.listReward.count()):
            self.listReward.takeItem(0)
        self.listReward.addItem('序号\t收入\t支出\t分类\t\t创建时间')

    def deleteReward(self):
        for item in self.listReward.selectedItems():
            itemID = item.text().split('\t')[0]
            if itemID == '序号':
                pass
            else:
                if QMessageBox.question(self, '提示', '确定删除该条账务？',
                                        QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                    res = sql_manage.deleteReward(itemID)
                    if res == True:
                        QMessageBox.information(self, '提示', '删除成功！')
                    else:
                        QMessageBox.warning(self, '警告', f'删除失败！{res}')
                    self.getReward()

    def getReward(self):
        self.clearList()
        rewards = sql_manage.getReward()
        for reward in rewards:
            self.listReward.addItem(
                str(reward[0]) + '\t' + str(reward[1]) + '\t' + str(-1 * (reward[2])) + '\t' + reward[3] + '\t\t' +
                reward[4])

    def addReward(self):
        if self.editIncome.text() == '' or self.editExpense.text() == '' or self.editDatetime.dateTime() == '':
            QMessageBox.warning(self, '警告', '收入、支出和时间不能为空！')
        else:
            res = sql_manage.addReward(self.editIncome.text(), -1 * int(self.editExpense.text()),
                                       self.comboxClassify.currentText(), self.editDatetime.dateTime().toString(
                    'yyyy-MM-dd HH:mm:ss'))
            if res == True:
                QMessageBox.information(self, '提示', '添加成功！')
            else:
                QMessageBox.warning(self, '警告', f'添加失败！{res}')
            self.getReward()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window_width = 600
    window_height = 350
    window = Window()
    window.show()
    sys.exit(app.exec_())
