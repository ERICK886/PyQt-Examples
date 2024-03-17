from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon, QFont


class MessageBox(QMessageBox):
    def __init__(self):
        super().__init__()

    def main(self, title, text, ico):
        msgBox = QMessageBox()
        msgBox.setWindowIcon(QIcon("logo.ico"))
        msgBox.setIconPixmap(QIcon(f"resources/ico/{ico}").pixmap(64, 64))
        msgBox.setText(text)
        msgBox.setWindowTitle(title)
        msgBox.setFont(QFont("HarmonyOS Sans SC", 10))
        okButton = msgBox.addButton("确定", QMessageBox.AcceptRole)
        cancelButton = msgBox.addButton("取消", QMessageBox.RejectRole)
        okButton.setStyleSheet("""QPushButton{
                                            font: 57 9pt "HarmonyOS Sans SC";
                                            background-color: #C32E24;
                                            color: white;
                                            border: none;
                                            border-radius: 5px;
                                            width: 100px;
                                            height: 30px;
                                        }

                                        QPushButton:hover {
                                            background-color: white;
                                            color: #C32E24;
                                        }""")
        cancelButton.setStyleSheet("""QPushButton{
                                                font: 57 9pt "HarmonyOS Sans SC";
                                                background-color: #C32E24;
                                                color: white;
                                                border: none;
                                                border-radius: 5px;
                                                width: 100px;
                                                height: 30px;
                                            }

                                            QPushButton:hover {
                                                background-color: white;
                                                color: #C32E24;
                                            }""")
        msgBox.setStyleSheet("QMessageBox {background-color: #FFFFFF; color: #000000;}")
        msgBox.exec_()
        if msgBox.clickedButton() == okButton:
            return True
        elif msgBox.clickedButton() == cancelButton:
            return False

    def info(self, title, text):
        ico = "info.ico"
        res = self.main(title, text, ico)
        return res

    def warn(self, title, text):
        ico = "warn.ico"
        res = self.main(title, text, ico)
        return res

    def quest(self, title, text):
        ico = "question.ico"
        res = self.main(title, text, ico)
        return res
