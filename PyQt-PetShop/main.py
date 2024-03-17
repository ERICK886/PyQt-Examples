from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QComboBox, \
    QListWidget, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt
import sys
import json


class File:
    def __init__(self):
        self.path = "pets.json"  # 文件路径

    def read(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            return json.loads(f.read())  # 读取文件内容并解析为JSON格式数据

    def write(self, data):
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)  # 将数据以JSON格式写入文件


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.file = File()  # 创建File对象
        self.pets = None  # 初始化pets为None
        self.setWindowTitle("宠物商店")  # 设置窗口标题为"宠物商店"
        self.setFixedSize(630, 620)  # 设置窗口大小为600x620
        self.setWindowIcon(QIcon("petshop.ico"))  # 设置窗口图标为"petshop.ico"
        self.initUI()  # 初始化界面

    def initUI(self):
        # 创建主布局
        self.mainLayout = QVBoxLayout()
        # 设置布局
        self.setLayout(self.mainLayout)

        # 创建标题布局
        self.titleLayout = QVBoxLayout()
        # 将标题布局添加到主布局中
        self.mainLayout.addLayout(self.titleLayout)

        # 创建标题标签
        self.title = QLabel("欢迎光临宠物商店")
        # 设置标题字体
        self.title.setFont(QFont("微软雅黑", 16))
        # 设置标题对齐方式
        self.title.setAlignment(Qt.AlignCenter)
        # 将标题标签添加到标题布局中
        self.titleLayout.addWidget(self.title)

        # 创建搜索标签
        self.searchLabel = QLabel("查询宠物")
        # 设置搜索标签字体
        self.searchLabel.setFont(QFont("微软雅黑", 10))
        # 设置标题对齐方式
        self.searchLabel.setAlignment(Qt.AlignCenter)
        # 将搜索标签添加到标题布局中
        self.titleLayout.addWidget(self.searchLabel)

        # 创建搜索布局
        self.searchLayout = QHBoxLayout()

        # 将搜索布局添加到标题布局中
        self.titleLayout.addLayout(self.searchLayout)

        # 创建搜索组合框
        self.searchBox = QComboBox()
        # 添加搜索选项
        self.searchBox.addItem("查询所有宠物")
        self.searchBox.addItem("查询指定宠物")
        self.searchBox.addItem("根据种类查询")
        self.searchBox.addItem("根据品种查询")
        self.searchBox.addItem("根据价格查询")
        # 设置搜索组合框字体
        self.searchBox.setFont(QFont("微软雅黑", 10))
        # 将搜索组合框添加到搜索布局中
        self.searchLayout.addWidget(self.searchBox)

        # 创建搜索文本框
        self.searchEdit = QLineEdit()
        # 设置搜索文本框字体
        self.searchEdit.setFont(QFont("微软雅黑", 10))
        # 将搜索文本框添加到搜索布局中
        self.searchLayout.addWidget(self.searchEdit)

        # 创建搜索按钮
        self.searchButton = QPushButton("查询")
        # 连接搜索按钮的点击事件到search函数
        self.searchButton.clicked.connect(self.search)
        # 设置搜索按钮字体
        self.searchButton.setFont(QFont("微软雅黑", 10))
        # 将搜索按钮添加到搜索布局中
        self.searchLayout.addWidget(self.searchButton)

        # 创建主体布局
        self.bodyLayout = QHBoxLayout()
        # 将主体布局添加到主布局中
        self.mainLayout.addLayout(self.bodyLayout)

        # 创建左侧布局
        self.leftLayout = QVBoxLayout()
        # 设置左侧布局对齐方式
        self.leftLayout.setAlignment(Qt.AlignLeft)
        # 将左侧布局添加到主体布局中
        self.bodyLayout.addLayout(self.leftLayout)

        # 创建搜索列表
        self.searchList = QListWidget()
        # 设置搜索列表字体
        self.searchList.setFont(QFont("微软雅黑", 10))
        # 设置搜索列表固定大小
        self.searchList.setFixedSize(300, 400)
        # 连接搜索列表的点击事件到showinfo函数
        self.searchList.itemClicked.connect(self.showinfo)
        # 将搜索列表添加到左侧布局中
        self.leftLayout.addWidget(self.searchList)

        # 创建购买按钮
        self.buyButton = QPushButton("购买")
        # 设置购买按钮字体
        self.buyButton.setFont(QFont("微软雅黑", 10))
        # 连接购买按钮的点击事件到buy函数
        self.buyButton.clicked.connect(self.buy)
        # 将购买按钮添加到左侧布局中
        self.leftLayout.addWidget(self.buyButton)

        # 创建退出按钮
        self.exitButton = QPushButton("退出")
        # 设置退出按钮字体
        self.exitButton.setFont(QFont("微软雅黑", 10))
        # 连接退出按钮的点击事件到close函数
        self.exitButton.clicked.connect(self.close)
        # 将退出按钮添加到左侧布局中
        self.leftLayout.addWidget(self.exitButton)

        # 创建右侧布局
        self.rightLayout = QVBoxLayout()
        # 将右侧布局添加到主体布局中
        self.bodyLayout.addLayout(self.rightLayout)

        # 创建图片标签
        self.imgLabel = QLabel()
        # 设置图片标签固定大小
        self.imgLabel.setFixedSize(300, 320)
        # 设置图片标签对齐方式
        self.imgLabel.setAlignment(Qt.AlignCenter)
        # 将图片标签添加到右侧布局中
        self.rightLayout.addWidget(self.imgLabel)

        # 创建信息列表
        self.infoList = QListWidget()
        # 设置信息列表字体
        self.infoList.setFont(QFont("微软雅黑", 10))
        # 设置信息列表固定宽度
        self.infoList.setFixedWidth(300)
        # 将信息列表添加到右侧布局中
        self.rightLayout.addWidget(self.infoList)

    def search(self):
        self.searchList.clear()  # 清空搜索列表
        data = {}  # 创建一个空字典data
        if self.searchBox.currentText() == "查询所有宠物":  # 如果当前文本为"查询所有宠物"
            data = self.file.read()  # 读取文件中的所有数据并赋值给data
            for k, v in data.items():  # 遍历data字典的键值对
                self.searchList.addItem(v["姓名"])  # 将每个宠物的姓名添加到搜索列表中

        elif self.searchBox.currentText() == "查询指定宠物":  # 如果当前文本为"查询指定宠物"
            if self.searchEdit.text() == "":  # 如果搜索编辑框中没有输入内容
                return QMessageBox.warning(self, "警告", "请输入要查询的宠物名称")  # 弹出警告对话框，提示用户输入查询的宠物名称
            data = self.file.read()  # 读取文件中的所有数据并赋值给data
            for k, v in data.items():  # 遍历data字典的键值对
                if self.searchEdit.text() in v["姓名"]:  # 如果搜索编辑框中的内容为宠物姓名的一部分
                    self.searchList.addItem(v["姓名"])  # 将该宠物的姓名添加到搜索列表中

        elif self.searchBox.currentText() == "根据种类查询":  # 如果当前文本为"根据种类查询"
            if self.searchEdit.text() == "":  # 如果搜索编辑框中没有输入内容
                return QMessageBox.warning(self, "警告", "请输入要查询的宠物种类")  # 弹出警告对话框，提示用户输入查询的宠物种类
            data = self.file.read()  # 读取文件中的所有数据并赋值给data
            for k, v in data.items():  # 遍历data字典的键值对
                if self.searchEdit.text() in v["种类"]:  # 如果搜索编辑框中的内容为宠物种类的一部分
                    self.searchList.addItem(v["姓名"])  # 将该宠物的姓名添加到搜索列表中

        elif self.searchBox.currentText() == "根据价格查询":  # 如果当前文本为"根据价格查询"
            if self.searchEdit.text() == "":  # 如果搜索编辑框中没有输入内容
                return QMessageBox.warning(self, "警告", "请输入要查询的宠物价格")  # 弹出警告对话框，提示用户输入查询的宠物价格
            data = self.file.read()  # 读取文件中的所有数据并赋值给data
            for k, v in data.items():  # 遍历data字典的键值对
                if self.searchEdit.text() in v["价格"]:  # 如果搜索编辑框中的内容为宠物价格的一部分
                    self.searchList.addItem(v["姓名"])  # 将该宠物的姓名添加到搜索列表中

        elif self.searchBox.currentText() == "根据品种查询":  # 如果当前文本为"根据品种查询"
            if self.searchEdit.text() == "":  # 如果搜索编辑框中没有输入内容
                return QMessageBox.warning(self, "警告", "请输入要查询的宠物品种")  # 弹出警告对话框，提示用户输入查询的宠物品种
            data = self.file.read()  # 读取文件中的所有数据并赋值给data
            for k, v in data.items():  # 遍历data字典的键值对
                if self.searchEdit.text() in v["品种"]:  # 如果搜索编辑框中的内容为宠物品种的一部分
                    self.searchList.addItem(v["姓名"])  # 将该宠物的姓名添加到搜索列表中

        self.pets = data  # 将data赋值给pets

    def showinfo(self):
        # 如果当前没有选中要购买的宠物，则弹出警告对话框
        if self.searchList.currentItem() is None:
            return QMessageBox.warning(self, "警告", "请先选择要购买的宠物")
        else:
            # 如果pets不为空
            if self.pets:
                # 遍历pets字典
                for k, v in self.pets.items():
                    # 如果当前选中项的文本等于v字典中的姓名
                    if self.searchList.currentItem().text() == v["姓名"]:
                        # 获取id和img
                        id = k
                        img = v["照片"]
                        # 生成info列表
                        info = [f"序号: {id}", f"姓名: {v['姓名']}", f"种类: {v['种类']}", f"品种: {v['品种']}",
                                f"描述: {v['描述']}", f"价格: {v['价格']} ￥"]
                        # 在imgLabel设置QPixmap并调整大小
                        self.imgLabel.setPixmap(QPixmap(img).scaled(300, 320))
                        self.infoList.clear()
                        # 在infoList中添加Items
                        self.infoList.addItems(info)

    def buy(self):
        # 判断当前是否选中了要购买的宠物
        if self.searchList.currentItem() is None:
            # 如果没有选中，则弹出警告对话框，提示选择要购买的宠物
            return QMessageBox.warning(self, "警告", "请先选择要购买的宠物")
        else:
            # 如果已经选中了要购买的宠物
            # 判断pets字典是否为空
            if self.pets:
                # 遍历pets字典
                for k, v in self.pets.items():
                    # 如果选中的宠物名称与字典中的姓名相等
                    if self.searchList.currentItem().text() == v["姓名"]:
                        # 从pets字典中删除该宠物
                        del self.pets[k]
                        # 将更新后的pets字典写入文件
                        self.file.write(self.pets)
                        # 更新搜索结果
                        self.search()
                        self.showinfo()
                        # 弹出提示对话框，提示购买成功
                        QMessageBox.information(self, "提示", "购买成功")
                        # 返回
                        return
            else:
                # 如果pets字典为空，则弹出警告对话框，提示没有该宠物可购买
                QMessageBox.warning(self, "警告", "购买失败，暂无该宠物")


# 如果该脚本是作为主程序运行时，则执行以下代码块
if __name__ == '__main__':
    # 创建一个应用程序对象
    app = QApplication(sys.argv)
    # 创建一个窗口对象
    window = Window()
    # 显示窗口
    window.show()
    # 运行应用程序，直到窗口关闭
    sys.exit(app.exec_())
