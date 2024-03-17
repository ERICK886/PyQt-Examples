from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QComboBox, \
    QPushButton, QMessageBox, QDateTimeEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDateTime
import sys
import json

publishers = [
    '北京大学出版社', '清华大学出版社', '人民邮电出版社', '中国人民大学出版社', '中国人民公共出版社',
    '中国人民教育出版社', '中国社会科学出版社', '中国科学技术出版社', '中国农业大学出版社',
    '中国农业出版社', '中国石油大学出版社', '中国矿业大学出版社', '中国石化大学出版社', '作家出版社',
    '中国电力出版社', '中国水利水电出版社', '中国石化工业出版社', '中国化学工业出版社',
    '中国机械工业出版社', '河南文艺出版社'
]

classes = [
    '文学', '艺术', '教育', '科技', '社会', '自然', '历史', '社会科学', '军事科学', '心理学', '法律', '军事', '经济',
    '人文', '心理健康', '人类学', '哲学', '宗教', '社会学', '历史学', '地理', '生物学', '天文学', '地质学', '医学',
    '小说', '魔幻', '玄幻', '奇幻', '武侠', '仙侠', '都市', '穿越', '游戏', '竞技', '体育'
]


class Json:
    def __init__(self):
        self.path = 'book.json'

    def read(self):
        """读取json文件"""
        with open(self.path, 'r', encoding='utf-8') as f:
            books = json.load(f)
        return books

    def write(self, books):
        """写入json文件"""
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(books, f, ensure_ascii=False, indent=4)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.width = 800  # 窗口宽度
        self.height = 600  # 窗口高度
        self.file = Json()  # 创建一个Json对象用于处理文件读写
        self.setWindowTitle('书记管理系统')  # 设置窗口标题为'书记管理系统'
        self.setWindowIcon(QIcon('book.ico'))  # 设置窗口图标为'book.ico'
        self.resize(self.width, self.height)  # 调整窗口大小为指定的宽度和高度
        self.show()  # 显示窗口
        self.initUI()  # 初始化窗口界面

    def initUI(self):
        # 创建一个水平布局对象
        self.mainLayout = QHBoxLayout()
        # 将该布局对象设置为窗口的布局
        self.setLayout(self.mainLayout)
        # 创建一个垂直布局对象
        self.leftLayout = QVBoxLayout()
        # 将该布局对象添加到主布局中
        self.mainLayout.addLayout(self.leftLayout)
        # 创建一个标签对象，文本为'&书名：'
        self.labelBookName = QLabel('&书名：', self)
        # 创建一个编辑框对象
        self.editBookName = QLineEdit(self)
        # 将编辑框与标签进行关联
        self.labelBookName.setBuddy(self.editBookName)
        # 将标签添加到左侧布局中
        self.leftLayout.addWidget(self.labelBookName)
        # 将编辑框添加到左侧布局中
        self.leftLayout.addWidget(self.editBookName)

        self.labelISBN = QLabel('&ISBN：', self)  # 创建一个 QLabel 对象，显示 "ISBN：" 文本，使用 &, 在窗口中显示为粗体
        self.editISBN = QLineEdit(self)  # 创建一个 QLineEdit 对象，用于输入 ISBN 编号
        self.labelISBN.setBuddy(self.editISBN)  # 将 QLabel 对象与 QLineEdit 对象关联，使 QLineEdit 对象在鼠标悬停时显示工具提示
        self.leftLayout.addWidget(self.labelISBN)  # 将 QLabel 对象添加到左侧布局中
        self.leftLayout.addWidget(self.editISBN)  # 将 QLineEdit 对象添加到左侧布局中

        # 创建一个 QLabel 对象，显示 "作者：" 文本，使用 &, 在窗口中显示为粗体
        self.labelAuthor = QLabel('&作者：', self)
        # 创建一个 QLineEdit 对象，用于输入作者姓名
        self.editAuthor = QLineEdit(self)
        # 将 QLabel 对象与 QLineEdit 对象关联，使 QLineEdit 对象在鼠标悬停时显示工具提示
        self.labelAuthor.setBuddy(self.editAuthor)
        # 将 QLabel 对象添加到左侧布局中
        self.leftLayout.addWidget(self.labelAuthor)
        # 将 QLineEdit 对象添加到左侧布局中
        self.leftLayout.addWidget(self.editAuthor)

        self.labelPublisher = QLabel('&出版社：', self)  # 创建一个 QLabel 对象，显示 "出版社：" 文本，使用 &, 在窗口中显示为粗体
        self.comboBoxPublisher = QComboBox(self)  # 创建一个 QComboBox 对象，用于显示下拉选项框
        self.showPublisher()  # 显示出版社列表
        self.labelPublisher.setBuddy(self.comboBoxPublisher)  # 将 QLabel 对象与 QComboBox 对象关联，使 QComboBox 对象在鼠标悬停时显示工具提示
        self.leftLayout.addWidget(self.labelPublisher)  # 将 QLabel 对象添加到左侧布局中
        self.leftLayout.addWidget(self.comboBoxPublisher)  # 将 QComboBox 对象添加到左侧布局中

        self.labelPrice = QLabel('&价格：', self)  # 创建一个QLabel对象，显示"价格："，buddy属性与下面的QLineEdit对象关联
        self.editPrice = QLineEdit(self)  # 创建一个QLineEdit对象，用于输入价格
        self.labelPrice.setBuddy(self.editPrice)  # 设置QLabel对象的buddy属性为QLineEdit对象，使两者之间建立关联
        self.leftLayout.addWidget(self.labelPrice)  # 将QLabel对象添加到布局中
        self.leftLayout.addWidget(self.editPrice)  # 将QLineEdit对象添加到布局中

        self.labelSale = QLabel('&销量：', self)  # 创建一个QLabel对象，显示"销量："，使用setBuddy方法将QLineEdit对象与QLabel对象关联
        self.editSale = QLineEdit(self)  # 创建一个QLineEdit对象，用于输入销量
        self.labelSale.setBuddy(self.editSale)  # 将QLineEdit对象与QLabel对象关联，使得当QLabel对象丢失时，QLineEdit对象也会丢失
        self.leftLayout.addWidget(self.labelSale)  # 将QLabel对象添加到布局中
        self.leftLayout.addWidget(self.editSale)  # 将QLineEdit对象添加到布局中
        # 创建一个QLabel对象，显示"库存："，并将其指定为父对象
        self.labelStock = QLabel('&库存：', self)
        # 创建一个QLineEdit对象，并将其指定为父对象
        self.editStock = QLineEdit(self)
        # 将QLineEdit对象与QLabel对象关联，使得当QLabel对象丢失时，QLineEdit对象也会丢失
        self.labelStock.setBuddy(self.editStock)
        # 将QLabel对象添加到布局中
        self.leftLayout.addWidget(self.labelStock)
        # 将QLineEdit对象添加到布局中
        self.leftLayout.addWidget(self.editStock)
        # 创建一个 QLabel 对象 self.labelPubDate，并设置文本为 '&出版日期：'
        self.labelPubDate = QLabel('&出版日期：', self)
        # 创建一个 QDateTimeEdit 对象 self.datePubDate，并将其父对象设置为当前窗口
        self.datePubDate = QDateTimeEdit(self)
        # 设置 QDateTimeEdit 对象 self.datePubDate 的显示格式为 'yyyy-MM-dd'
        self.datePubDate.setDisplayFormat('yyyy-MM-dd')
        # 设置 QDateTimeEdit 对象 self.datePubDate 的日期时间为当前日期时间
        self.datePubDate.setDateTime(QDateTime.currentDateTime())
        # 设置 QDateTimeEdit 对象 self.datePubDate 的日历弹出窗口显示
        self.datePubDate.setCalendarPopup(True)
        # 将 QLabel 对象 self.labelPubDate 和 QDateTimeEdit 对象 self.datePubDate 设置为“好友”关系
        self.labelPubDate.setBuddy(self.datePubDate)
        # 将 QLabel 对象 self.labelPubDate 添加到布局 self.leftLayout 中
        self.leftLayout.addWidget(self.labelPubDate)
        # 将 QDateTimeEdit 对象 self.datePubDate 添加到布局 self.leftLayout 中
        self.leftLayout.addWidget(self.datePubDate)

        self.labelClass = QLabel('&分类：', self)  # 创建一个标签，显示为"分类："，使用了 QLabel 的构造函数
        self.comboBoxClass = QComboBox(self)  # 创建一个下拉框，使用了 QComboBox 的构造函数
        self.showClass()  # 调用了一个名为 showClass 的函数
        self.labelClass.setBuddy(self.comboBoxClass)  # 使用 setBuddy 方法将标签和下拉框关联起来
        self.leftLayout.addWidget(self.labelClass)  # 将标签添加到 leftLayout 布局中
        self.leftLayout.addWidget(self.comboBoxClass)  # 将下拉框添加到 leftLayout 布局中

        self.buttonAddBook = QPushButton('&添加', self)  # 创建一个名为buttonAddBook的QPushButton对象，显示为"添加"，父对象为self
        self.buttonAddBook.clicked.connect(self.addBook)  # 当buttonAddBook被点击时，触发addBook函数
        self.leftLayout.addWidget(self.buttonAddBook)  # 将buttonAddBook添加到leftLayout布局中

        self.buttonDeleteBook = QPushButton('&删除', self)
        # 创建一个名为buttonDeleteBook的QPushButton对象，并显示文本来表示“删除”
        self.buttonDeleteBook.clicked.connect(self.deleteBook)
        # 当按钮被点击时，调用deleteBook方法
        self.leftLayout.addWidget(self.buttonDeleteBook)
        # 将按钮添加到leftLayout中

        self.buttonExit = QPushButton('&退出', self)  # 创建一个名为buttonExit的QPushButton对象，并显示文本来表示“退出”
        self.buttonExit.clicked.connect(self.close)  # 当按钮被点击时，调用close方法
        self.leftLayout.addWidget(self.buttonExit)  # 将按钮添加到leftLayout中

        self.rightLayout = QVBoxLayout()  # 创建一个垂直布局的容器，用于放置右侧的组件
        self.mainLayout.addLayout(self.rightLayout)  # 将右侧布局容器添加到主布局中
        self.listWidget = QListWidget(self)  # 创建一个QListWidget对象，用于显示列表
        self.showBook()  # 调用showBook方法，显示书籍列表
        self.listWidget.setFixedWidth(450)  # 设置列表宽度为固定值450
        self.rightLayout.addWidget(self.listWidget)  # 将列表组件添加到右侧布局容器中

    def showPublisher(self):
        """显示出版社"""
        self.comboBoxPublisher.addItems(publishers)

    def showClass(self):
        """显示分类"""
        self.comboBoxClass.addItems(classes)

    def addBook(self):
        """添加书籍"""
        bookName = self.editBookName.text()  # 读取编辑框中的书名
        ISBN = self.editISBN.text()  # 读取编辑框中的ISBN号
        author = self.editAuthor.text()  # 读取编辑框中的作者
        publisher = self.comboBoxPublisher.currentText()  # 读取下拉框中的出版社
        price = self.editPrice.text()  # 读取编辑框中的价格
        stock = self.editStock.text()  # 读取编辑框中的库存
        sales = self.editSale.text()  # 读取编辑框中的销量
        pubdate = self.datePubDate.dateTime().toString()  # 读取日期选择器中的出版日期
        class_ = self.comboBoxClass.currentText()  # 读取下拉框中的分类
        if bookName and ISBN and author and publisher and price and stock and sales and pubdate and class_:  # 检查必要信息是否填写完整
            data = self.file.read()  # 读取文件中的数据
            for book in data:  # 遍历数据中的每一本书
                if data[book]['ISBN'] == ISBN:  # 检查ISBN号是否已存在
                    QMessageBox.warning(self, '警告', '该ISBN已存在！')  # 警告用户该ISBN号已存在
                    return  # 返回函数
            data[bookName] = {  # 将新书的信息添加到数据中
                'ISBN': ISBN,
                '作者': author,
                '出版社': publisher,
                '价格': price,
                '库存': stock,
                '销量': sales,
                '出版日期': pubdate,
                '分类': class_
            }
            self.file.write(data)  # 将更新后的数据写入文件
            QMessageBox.information(self, '提示', '添加成功！')  # 告知用户添加成功
            self.showBook()  # 显示书籍列表
        else:
            QMessageBox.warning(self, '警告', '请填写完整信息！')  # 警告用户未填写完整信息

    def deleteBook(self):
        """
        删除书籍
        """
        item = self.listWidget.currentItem()  # 获取当前选中的列表项
        if item:  # 判断是否存在选中的列表项
            bookName = item.text().split('\n')[0].split(': ')[1]  # 获取书籍名称
            data = self.file.read()  # 读取文件中的数据
            if bookName in data:  # 判断书籍是否存在于数据中
                del data[bookName]  # 删除书籍数据
                self.file.write(data)  # 将更新后的数据写入文件
                QMessageBox.information(self, '提示', '删除成功！)')  # 显示成功提示消息
            else:
                QMessageBox.warning(self, '警告', '该书籍不存在！')  # 显示警告消息，书籍不存在
        self.showBook()  # 显示书籍列表

    def showBook(self):
        # 读取文件内容并赋值给self.data
        self.data = self.file.read()
        # 清空列表widget
        self.listWidget.clear()

        # 遍历self.data中的每一本书
        for book in self.data:
            arg = ''
            # 添加书名信息到arg
            arg += f"书名: {book}\n"
            # 遍历每一本书的每一个属性和值
            for key, value in self.data[book].items():
                # 添加属性和值信息到arg
                arg += f"{key}: {value}\n"
            # 将arg添加到列表widget中
            self.listWidget.addItem(arg)


# 如果该脚本是作为主程序运行则执行以下代码
if __name__ == '__main__':
    # 创建一个应用程序对象
    app = QApplication(sys.argv)
    # 创建一个主窗口对象
    mainWin = MainWindow()
    # 运行应用程序，直到主循环结束
    sys.exit(app.exec_())
