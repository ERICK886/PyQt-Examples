import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, \
    QColorDialog
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt, QPoint, QRect


class PaintWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('画图工具')

        # 创建一个标签用于显示画布
        self.canvas = QLabel()
        self.canvas.setAlignment(Qt.AlignCenter)
        self.canvas.setFixedSize(400, 400)
        self.canvas.setPixmap(QPixmap(400, 400))
        self.canvas.pixmap().fill(Qt.white)

        # 创建按钮用于清空画布
        self.clear_button = QPushButton('清空画布')
        self.clear_button.clicked.connect(self.clear_canvas)

        # 创建按钮用于绘制直线
        self.line_button = QPushButton('直线')
        self.line_button.clicked.connect(self.draw_line)

        # 创建按钮用于绘制矩形
        self.rect_button = QPushButton('矩形')
        self.rect_button.clicked.connect(self.draw_rectangle)

        # 创建按钮用于绘制椭圆
        self.ellipse_button = QPushButton('椭圆')
        self.ellipse_button.clicked.connect(self.draw_ellipse)

        # 创建按钮用于填充颜色
        self.fill_color_button = QPushButton('填充颜色')
        self.fill_color_button.clicked.connect(self.set_fill_color)

        # 创建按钮用于设置线条颜色
        self.line_color_button = QPushButton('线条颜色')
        self.line_color_button.clicked.connect(self.set_line_color)

        # 创建垂直布局，并将画布添加到布局中
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)

        buttons_layout = QHBoxLayout()  # 创建一个水平布局

        buttons_layout.addWidget(self.clear_button)  # 将清除按钮添加到布局
        buttons_layout.addWidget(self.line_button)  # 将直线按钮添加到布局
        buttons_layout.addWidget(self.rect_button)  # 将矩形按钮添加到布局
        buttons_layout.addWidget(self.ellipse_button)  # 将椭圆按钮添加到布局
        buttons_layout.addWidget(self.fill_color_button)  # 将填充颜色按钮添加到布局
        buttons_layout.addWidget(self.line_color_button)  # 将线条颜色按钮添加到布局

        self.layout.addLayout(buttons_layout)  # 将按钮布局添加到主布局中
        self.central_widget = QWidget()  # 创建一个QWidget对象作为中央小部件
        self.central_widget.setLayout(self.layout)  # 为中央小部件设置布局
        self.setCentralWidget(self.central_widget)  # 将中央小部件设置为窗口的中央小部件

        self.drawing = False  # 初始化绘画状态为False
        self.start_pos = QPoint()  # 初始化起始位置为QPoint对象
        self.end_pos = QPoint()  # 初始化结束位置为QPoint对象
        self.fill_color = Qt.white  # 设置填充颜色为白色
        self.line_color = Qt.black  # 设置线条颜色为黑色

    def paintEvent(self, event):
        # 绘制事件，用于重绘画布
        painter = QPainter(self.canvas.pixmap())
        pen = QPen(self.line_color, 2)
        painter.setPen(pen)

        if self.drawing:
            # 如果正在绘制
            if self.shape == 'line':
                # 如果绘制的形状为线段
                painter.drawLine(self.start_pos, self.end_pos)
            elif self.shape == 'rectangle':
                # 如果绘制的形状为矩形
                rect = QRect(self.start_pos, self.end_pos)
                if self.fill_color != Qt.transparent:
                    # 如果需要填充颜色
                    painter.fillRect(rect, self.fill_color)
                painter.drawRect(rect)
            elif self.shape == 'ellipse':
                # 如果绘制的形状为椭圆
                rect = QRect(self.start_pos, self.end_pos)
                if self.fill_color != Qt.transparent:
                    # 如果需要填充颜色
                    painter.setBrush(self.fill_color)
                    painter.setPen(Qt.NoPen)
                    painter.drawEllipse(rect)
                painter.setBrush(Qt.NoBrush)
                painter.drawEllipse(rect)

    def mousePressEvent(self, event):
        """
        鼠标点击事件的回调函数，当鼠标左键被点击时触发

        Args:
            event: 鼠标事件对象，包含了鼠标点击的位置信息

        Returns:
            None
        """
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.start_pos = event.pos()
            self.end_pos = event.pos()

    def mouseMoveEvent(self, event):
        """
        鼠标移动事件的回调函数

        Args:
            event: 鼠标移动事件对象

        Returns:
            None
        """
        if self.drawing:
            self.end_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        """
        鼠标释放事件的回调函数
        :param event: 鼠标事件对象
        :return: None
        """
        if event.button() == Qt.LeftButton:  # 判断鼠标是否是左键释放
            self.drawing = False  # 设置绘画标志为False，表示停止绘画
            self.update()  # 更新绘图区域

    def clear_canvas(self):
        # 清除画布上的图像
        self.canvas.pixmap().fill(Qt.white)
        # 更新画布
        self.update()

    def draw_line(self):
        # 绘制直线
        self.shape = 'line'

    def draw_rectangle(self):
        # 绘制矩形
        self.shape = 'rectangle'

    def draw_ellipse(self):
        # 绘制椭圆
        self.shape = 'ellipse'

    def set_fill_color(self):
        # 设置填充颜色
        color = QColorDialog.getColor()
        if color.isValid():
            self.fill_color = color

    def set_line_color(self):
        # 设置边框颜色
        color = QColorDialog.getColor()
        if color.isValid():
            self.line_color = color


if __name__ == '__main__':
    # 创建一个应用程序对象
    app = QApplication(sys.argv)
    # 创建一个PaintWindow对象
    paint_window = PaintWindow()
    # 显示窗口
    paint_window.show()
    # 运行应用程序
    sys.exit(app.exec_())
