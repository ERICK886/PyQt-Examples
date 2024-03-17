import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMessageBox, QHBoxLayout, QTextEdit, QLabel, QLineEdit, \
    QPushButton, QListWidget, QFontDialog, QColorDialog
from PyQt5.QtGui import QIcon

class ReadNovel:
    def __init__(self):
        self.dir = "novels"
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)

    def list_novels(self):
        items = []
        for filename in os.listdir(self.dir):
            if filename.endswith(".txt"):
                items.append(filename.split(".")[0])
        return items

    def read_novel(self, filename):
        with open(f"novels/{filename}", "r", encoding="utf-8") as f:
            content = f.read()
            return content


class NovelReader(QWidget):
    def __init__(self):
        super().__init__()
        self.reader = ReadNovel()
        self.setWindowTitle("小说阅读器")
        self.setWindowIcon(QIcon("reader.ico"))
        self.setGeometry(100, 100, 800, 600)
        self.novel = None
        self.chapters = ['请选择小说']
        self.current_chapter_index = 0
        self.content = None
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # 小说标题
        self.title_label = QLabel()
        self.title_label.setText("小说标题")
        main_layout.addWidget(self.title_label)

        select_layout = QVBoxLayout()
        main_layout.addLayout(select_layout)
        select_layout.addWidget(QLabel("选择小说"))
        self.select_list = QListWidget()
        novels = self.reader.list_novels()
        if novels:
            for novel in novels:
                self.select_list.addItem(novel)
        else:
            self.select_list.addItem("没有小说")
        self.select_list.itemClicked.connect(self.select_novel)
        self.select_list.setFixedHeight(100)
        select_layout.addWidget(self.select_list)

        # 章节选择
        chapter_layout = QHBoxLayout()
        prev_button = QPushButton("上一章")
        prev_button.clicked.connect(self.prev_chapter)
        chapter_layout.addWidget(prev_button)

        next_button = QPushButton("下一章")
        next_button.clicked.connect(self.next_chapter)
        chapter_layout.addWidget(next_button)
        main_layout.addLayout(chapter_layout)

        change_font_button = QPushButton("改变字体")
        change_font_button.clicked.connect(self.change_font)
        chapter_layout.addWidget(change_font_button)

        change_color_button = QPushButton("改变颜色")
        change_color_button.clicked.connect(self.change_color)
        chapter_layout.addWidget(change_color_button)

        # 小说内容
        self.novel_text_edit = QTextEdit()
        self.novel_text_edit.setFixedHeight(600)
        main_layout.addWidget(self.novel_text_edit)
        self.setLayout(main_layout)
        main_layout.addStretch()

    def change_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.novel_text_edit.setFont(font)

    def change_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.novel_text_edit.setTextColor(color)


    def select_novel(self):
        index = self.select_list.currentRow()
        if self.select_list.item(index).text() == "没有小说":
            QMessageBox.information(self, "提示", "请导入小说")
        else:
            self.novel = self.reader.read_novel(f"{self.reader.list_novels()[index]}.txt")
            self.content = self.novel.split("------------")
            self.chapters = [f"第{chapter + 1}章" for chapter in range(len(self.content))]
            self.current_chapter_index = 0
            self.update_chapter()

    def prev_chapter(self):
        if self.current_chapter_index > 0:
            self.current_chapter_index -= 1
            self.update_chapter()

    def next_chapter(self):
        if self.current_chapter_index < len(self.chapters) - 1:
            self.current_chapter_index += 1
            self.update_chapter()

    def update_chapter(self):
        self.novel_text_edit.clear()
        self.title_label.setText(self.chapters[self.current_chapter_index])
        self.novel_text_edit.setText(self.content[self.current_chapter_index + 1])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    novel_reader = NovelReader()
    novel_reader.show()
    sys.exit(app.exec_())
