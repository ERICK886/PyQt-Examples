import sys
import math
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QVBoxLayout, QLineEdit, QPushButton
from PyQt5.QtGui import QIcon


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('计算器')
        self.setWindowIcon(QIcon('./calculate.ico'))

        # 创建一个垂直布局和一个文本框
        layout = QVBoxLayout()
        self.text_box = QLineEdit()
        layout.addWidget(self.text_box)

        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()
        layout4 = QHBoxLayout()
        layout5 = QHBoxLayout()
        layout6 = QHBoxLayout()

        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(layout3)
        layout.addLayout(layout4)
        layout.addLayout(layout5)
        layout.addLayout(layout6)

        # 创建按钮并将其连接到处理函数
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            'sin', 'cos', 'tan', 'C',
            'log', 'exp', 'sqrt'
        ]
        for i in range(len(buttons)):
            button = QPushButton(buttons[i])
            button.clicked.connect(self.button_clicked)
            if i < 4:
                layout1.addWidget(button)
            elif i < 8:
                layout2.addWidget(button)
            elif i < 12:
                layout3.addWidget(button)
            elif i < 16:
                layout4.addWidget(button)
            elif i < 20:
                layout5.addWidget(button)
            elif i < 23:
                layout6.addWidget(button)

        self.setLayout(layout)

    def button_clicked(self):
        button = self.sender()
        text = button.text()

        if text == '=':
            # 处理等号按钮
            try:
                result = eval(self.text_box.text())
                self.text_box.setText(str(result))
            except:
                self.text_box.setText('Error')
        elif text in ('sin', 'cos', 'tan'):
            # 处理三角函数按钮
            try:
                angle = float(self.text_box.text())
                if text == 'sin':
                    result = round(math.sin(math.radians(angle)), 5)
                elif text == 'cos':
                    result = round(math.cos(math.radians(angle)), 5)
                elif text == 'tan':
                    result = round(math.tan(math.radians(angle)), 5)
                self.text_box.setText(str(result))
            except:
                self.text_box.setText('Error')
        elif text in ('log', 'exp', 'sqrt'):
            # 处理对数和平方根按钮
            try:
                number = float(self.text_box.text())
                if text == 'log':
                    result = round(math.log10(number), 5)
                elif text == 'exp':
                    result = round(math.exp(number), 5)
                elif text == 'sqrt':
                    result = round(math.sqrt(number), 5)
                self.text_box.setText(str(result))
            except:
                self.text_box.setText('Error')
        elif text == 'C':
            # 清空文本框
            self.text_box.setText('')
        else:
            # 处理其他运算符和数字
            self.text_box.setText(self.text_box.text() + text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec_())
