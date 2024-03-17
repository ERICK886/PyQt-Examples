import sys
import os
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        # 设置对话框的名称和大小
        Dialog.setWindowTitle("音乐播放器")
        Dialog.setFixedSize(400, 300)

        # 创建groupBox控件并设置位置和大小
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 20, 381, 221))
        self.groupBox.setTitle("详情")

        # 在groupBox控件中创建label控件并设置位置、对齐方式和内容
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 20, 381, 221))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText("暂无歌曲")

        # 创建layoutWidget控件并设置位置
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 270, 401, 25))

        # 在layoutWidget控件中创建水平布局
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        # 在水平布局中添加按钮pushButton_4
        self.pushButton_4 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_4.setText("音量+")
        self.horizontalLayout.addWidget(self.pushButton_4)

        # 在水平布局中添加按钮pushButton_2
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setText("上一首")
        self.horizontalLayout.addWidget(self.pushButton_2)

        # 在水平布局中添加按钮pushButton
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setText("播放")
        self.horizontalLayout.addWidget(self.pushButton)

        # 在水平布局中添加按钮pushButton_3
        self.pushButton_3 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_3.setText("下一首")
        self.horizontalLayout.addWidget(self.pushButton_3)

        # 在水平布局中添加按钮pushButton_5
        self.pushButton_5 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_5.setText("音量-")
        self.horizontalLayout.addWidget(self.pushButton_5)


class MainWin(QMainWindow, Ui_Dialog):
    def __init__(self, parent=None):
        super(MainWin, self).__init__(parent)
        self.setupUi(self)
        # 新建QMediaPlayer对象
        self.player = QMediaPlayer()
        # 当前播放状态标志位，False表示当前处于暂停状态，True表示当前处于播放状态
        self.player_state = False
        # 歌曲存放目录
        self.mp3filedir = "./music/"
        # 用于存放歌曲名称的空列表
        self.music_list = []
        # 当前播放歌曲在列表中的位置
        self.music_index = 0
        # 音量设置
        self.voice_level = 50
        # 从歌曲存放目录中读取所有文件名，并放入列表中
        for file_name in os.listdir(self.mp3filedir):
            self.music_list.append(file_name)
        # 获取歌曲总数
        self.music_all_num = len(self.music_list)
        # 拼接歌曲存放目录和歌曲名成完整路径，获取到文件
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.mp3filedir + self.music_list[self.music_index])))
        # 文件名展示
        self.music_detail()
        # 音量设置
        self.player.setVolume(self.voice_level)
        # 播放按钮绑定函数
        self.pushButton.clicked.connect(self.player_state_change)
        # 下一首按钮绑定函数
        self.pushButton_2.clicked.connect(self.next_music)
        # 上一首按钮绑定函数
        self.pushButton_3.clicked.connect(self.previous_music)
        # 音量加按钮绑定函数
        self.pushButton_4.clicked.connect(self.voice_add)
        # 音量减按钮绑定函数
        self.pushButton_5.clicked.connect(self.voice_reduce)

    def player_state_change(self):
        # 通过self.player_state获取当前播放状态，再进行切换
        if self.player_state:
            # 停止播放
            self.player.stop()
            # 播放状态标志设置为False
            self.player_state = False
        else:
            # 播放当前音频
            self.player.play()
            # 播放状态标志设置为True
            self.player_state = True

    def next_music(self):
        # 如果当前播放的音频位置索引为列表中最后一首，则位置索引置为0，回到列表开头
        if self.music_index == self.music_all_num - 1:
            self.music_index = 0
        # 否则位置索引加1
        else:
            self.music_index += 1
        # 根据位置索引获取歌曲名，并和歌曲存放目录拼接获取文件
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.mp3filedir + self.music_list[self.music_index])))
        # 歌曲名展示更新
        self.music_detail()
        # 进行播放
        self.player.play()

    def previous_music(self):
        # 如果当前播放的音频位置索引为列表中第一首，则位置索引置为列表长度减一，到列表末尾
        if self.music_index == 0:
            self.music_index = self.music_all_num - 1
        # 否则位置索引减1
        else:
            self.music_index -= 1
        # 根据位置索引获取歌曲名，并和歌曲存放目录拼接获取文件
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.mp3filedir + self.music_list[self.music_index])))
        # 歌曲名展示更新
        self.music_detail()
        # 进行播放
        self.player.play()

    def music_detail(self):
        """
        更新音乐详细信息的标签显示
        """
        self.label.setText(self.music_list[self.music_index])

    def voice_add(self):
        """
        增加音量级别
        """
        if self.voice_level < 100:
            self.voice_level += 10
        self.player.setVolume(self.voice_level)

    def voice_reduce(self):
        """
        减少音量级别
        """
        if self.voice_level > 0:
            self.voice_level -= 10
        self.player.setVolume(self.voice_level)


if __name__ == '__main__':
    # 屏幕分辨率适配
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    main = MainWin()
    main.show()
    sys.exit(app.exec_())
