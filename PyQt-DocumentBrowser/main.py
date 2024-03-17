import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTreeView, QFileSystemModel, QPushButton, QLineEdit, \
    QMessageBox, QFileDialog, QInputDialog


class FileBrowser(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('文件浏览器')
        self.layout = QVBoxLayout()

        self.path_edit = QLineEdit()
        self.layout.addWidget(self.path_edit)

        self.tree_view = QTreeView()
        self.model = QFileSystemModel()
        self.model.setRootPath('')
        self.tree_view.setModel(self.model)
        self.layout.addWidget(self.tree_view)

        self.create_button = QPushButton('创建文件')
        self.create_button.clicked.connect(self.create_file)
        self.layout.addWidget(self.create_button)

        self.open_button = QPushButton('打开文件')
        self.open_button.clicked.connect(self.open_file)
        self.layout.addWidget(self.open_button)

        self.delete_button = QPushButton('删除文件')
        self.delete_button.clicked.connect(self.delete_file)
        self.layout.addWidget(self.delete_button)

        self.rename_button = QPushButton('重命名文件')
        self.rename_button.clicked.connect(self.rename_file)
        self.layout.addWidget(self.rename_button)

        self.setLayout(self.layout)

    def create_file(self):
        file_path, ok = QFileDialog.getSaveFileName(self, '创建文件')
        if ok:
            with open(file_path, 'w'):
                pass

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, '打开文件')
        if file_path:
            QMessageBox.information(self, '文件内容', open(file_path).read())

    def delete_file(self):
        file_path = self.model.filePath(self.tree_view.currentIndex())
        reply = QMessageBox.question(self, '确认删除', f'确定要删除文件\n{file_path}吗？')
        if reply == QMessageBox.Yes:
            self.model.remove(self.tree_view.currentIndex())


    def rename_file(self):
        # 获取当前选中的文件路径和索引
        file_path = self.model.filePath(self.tree_view.currentIndex())
        if not file_path:
            QMessageBox.warning(self, '警告', '请先选择一个文件。')
            return

        new_name, ok = QInputDialog.getText(self, '重命名文件', '请输入新的文件名')

        # 检查用户是否输入了文件名
        if ok and new_name:
            # 可以在这里添加一些文件名合法性检查，例如不允许空格等

            try:
                # 更新文件名
                self.model.setData(self.tree_view.currentIndex(), new_name)
                # 如果更新成功，可以显示一个保存成功的提示消息
            except Exception as e:
                QMessageBox.warning(self, '警告', '文件名无法更新: ' + str(e))
                # 日志记录可能也对调试有帮助
                # logger.warning('尝试更新文件名时出错: ' + str(e))
        else:
            # 如果用户没有选择保存，不执行任何操作
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    file_browser = FileBrowser()
    file_browser.show()
    sys.exit(app.exec_())
