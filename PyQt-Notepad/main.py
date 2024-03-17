import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QFontDialog
from PyQt5.QtGui import QIcon

class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('notepad.ico'))
        self.initUI()

    def initUI(self):
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)

        # 创建菜单栏
        menubar = self.menuBar()

        fileMenu = menubar.addMenu('文件')
        formatMenu = menubar.addMenu('格式')

        # 创建保存和退出的动作
        saveAction = QAction('保存', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(self.saveFile)

        exitAction = QAction('退出', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)

        # 创建字体设置的动作
        fontAction = QAction('字体设置', self)
        fontAction.triggered.connect(self.setFont)

        # 将动作添加到菜单栏
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)

        formatMenu.addAction(fontAction)

        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('记事本')
        self.show()

    def saveFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getSaveFileName(self, "保存文件", "", "Text Files (*.txt);;All Files (*)",
                                              options=options)
        if file:
            with open(file, 'w') as f:
                f.write(self.textEdit.toPlainText())

    def setFont(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.textEdit.setFont(font)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    notepad = Notepad()
    sys.exit(app.exec_())
