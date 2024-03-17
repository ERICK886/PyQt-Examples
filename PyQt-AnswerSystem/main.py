from pages import *


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("考试答题系统")  # 设置窗口标题
        self.setFixedSize(window_width, window_height)  # 设置窗口大小为固定值
        self.setWindowIcon(QIcon("icon.ico"))  # 设置窗口图标
        qr = self.frameGeometry()  # 获取窗口的几何信息
        cp = QDesktopWidget().availableGeometry().center()  # 获取桌面的可用几何信息的中心点
        qr.moveCenter(cp)  # 移动窗口的中心点到桌面的可用几何信息的中心点

        # 创建堆栈窗口，并将登录界面和首页界面添加到其中
        self.stacked_widget = QStackedWidget()  # 创建堆栈窗口
        self.login = Login(self.stacked_widget)  # 创建登录界面
        self.register = Register(self.stacked_widget)  # 创建注册界面
        self.stacked_widget.addWidget(self.login)  # 将登录界面添加到堆栈窗口中
        self.stacked_widget.addWidget(self.register)  # 将注册界面添加到堆栈窗口中

        # 将堆栈窗口添加到主窗口中
        vbox = QVBoxLayout()  # 创建垂直布局
        vbox.addWidget(self.stacked_widget)  # 将堆栈窗口添加到垂直布局中
        self.setLayout(vbox)  # 将垂直布局设置为主窗口的布局


if __name__ == "__main__":
    app = QApplication(sys.argv)  # 创建应用对象
    window = MainWindow()  # 创建主窗口对象
    window.setAutoFillBackground(True)  # 设置自动填充背景
    palette = QPalette()  # 创建调色板对象

    palette.setColor(QPalette.Window, QColor(bg_100))  # 设置窗口背景颜色
    window.setPalette(palette)  # 设置窗口调色板
    window.show()  # 显示窗口
    sys.exit(app.exec_())  # 运行应用
