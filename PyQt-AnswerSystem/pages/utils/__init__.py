import json
import pymysql
from pymysql.cursors import DictCursor
from PyQt5.QtCore import QThread, pyqtSignal
from .style import *
from pathlib import Path


class Database:
    def __init__(self):
        """
        初始化数据库连接和游标
        """
        with open(Path(__file__).parent / 'config.json', 'r') as f:
            data = json.load(f)
        if data:
            self.user = data['user']
            self.password = data['password']
            self.database = data['database']
            self.host = data['host']
            self.port = data['port']
        else:
            self.user = 'root'
            self.password = '123456'
            self.database = 'exam'
            self.host = 'localhost'
            self.port = 3306

        self.conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
            cursorclass=DictCursor,
        )
        self.cursor = self.conn.cursor()

    def close(self):
        """
        关闭数据库连接
        """
        self.conn.close()

    def select_user_exam(self, userid):
        """
        查询用户考试信息

        Args:
            userid: 用户ID

        Returns:
            查询结果
        """
        sql = 'select * from userexam join exam e on userexam.examid = e.examid where userid=%s'
        self.cursor.execute(sql, (userid,))
        result = self.cursor.fetchall()
        return result

    def select_users(self):
        """
        查询所有用户信息

        Returns:
            查询结果
        """
        try:
            sql = 'select * from users'
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print(e)
            return None

    def insert_user(self, username, password, name, email, phone, sex, class_):
        """
        插入新用户信息

        Args:
            username: 用户名
            password: 密码
            name: 姓名
            email: 邮箱
            phone: 电话
            sex: 性别
            class_: 班级

        Returns:
            插入成功返回True，否则返回False
        """
        sql = 'insert into users(username, password, name, classname, email, phone, gender) values(%s, %s, %s, %s, %s, %s, %s)'
        try:
            self.cursor.execute(sql, (username, password, name, class_, email, phone, sex))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def select_user_exam_by_id(self, id):
        """
        根据考试ID查询用户考试信息

        Args:
            id: 考试ID

        Returns:
            查询结果
        """
        sql = 'select * from userexam where examid=%s'
        self.cursor.execute(sql, (id,))
        result = self.cursor.fetchone()
        return result

    def select_exam_by_id(self, id):
        """
        根据考试ID查询考试信息

        Args:
            id: 考试ID

        Returns:
            查询结果
        """
        sql = 'select * from exam where examid=%s'
        self.cursor.execute(sql, (id,))
        result = self.cursor.fetchone()
        return result

    def select_questions_by_examid(self, id):
        """
        根据考试ID查询题目信息

        Args:
            id: 考试ID

        Returns:
            查询结果
        """
        table = f'exam_{id}'
        sql = f'select * from {table}'
        self.cursor.execute(sql, )
        result = self.cursor.fetchall()
        return result

    def update_exam_con_by_userid_examid(self, userid, examid, con):
        """
        根据用户ID和考试ID更新考试成绩

        Args:
            userid: 用户ID
            examid: 考试ID
            con: 成绩

        Returns:
            更新结果
        """
        sql = 'update userexam set con=%s where userid=%s and examid=%s'
        self.cursor.execute(sql, (int(con), userid, examid))
        self.conn.commit()

    def update_exam_score_by_userid_examid(self, userid, examid, score):
        """
        根据用户ID和考试ID更新考试成绩

        Args:
            userid: 用户ID
            examid: 考试ID
            score: 成绩

        Returns:
            更新结果
        """
        sql = 'update userexam set score=%s where userid=%s and examid=%s'
        self.cursor.execute(sql, (int(score), userid, examid))
        self.conn.commit()


class UserFile:
    def __init__(self):
        # 使用Path对象来定义文件路径
        self.path = (Path(__file__).parent / 'user' / 'user.json').resolve()

    def read(self):
        try:
            with self.path.open('r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            # 如果文件无法被解析为合法的JSON格式，打印错误信息
            print(f'无法读取JSON文件：{e}，将文件视为新文件处理')
            # 如果文件不存在，则创建一个新字典
            with self.path.open('w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=4)

    def write(self, data):
        # 直接使用json.dump将数据写入文件
        with self.path.open('w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True


class ExamFile:
    def __init__(self):
        # 使用Path对象来定义文件路径
        self.path = (Path(__file__).parent / 'exam' / 'exam.json').resolve()

    def read(self):
        try:
            with self.path.open('r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f'无法读取JSON文件：{e}，将文件视为新文件处理')
            # 如果文件不存在，则创建一个新字典
            with self.path.open('w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=4)
            return {}

    def write(self, data):
        # 写入操作直接使用json.dump
        with self.path.open('w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True

    def write_exam(self, data, order):
        try:
            read = self.read()
            read['exam'][str(order)]['question'] = data
        except json.JSONDecodeError:
            print('文件不是有效的JSON格式，将无法更新。')
            return False
        with self.path.open('w', encoding='utf-8') as f:
            data = json.dumps(read, ensure_ascii=False, indent=4)
            f.write(data)
        return True

    def write_score(self, score, order):
        try:
            read = self.read()
            read['exam'][str(order)]['score'] = score
        except json.JSONDecodeError:
            print('文件不是有效的JSON格式，将无法更新。')
            return False
        with self.path.open('w', encoding='utf-8') as f:
            data = json.dumps(read, ensure_ascii=False, indent=4)
            f.write(data)
        return True


class CheckExamThread(QThread):
    signal = pyqtSignal(bool)

    def __init__(self, examData, answer):
        super().__init__()
        self.examData = examData
        self.answer = answer

    def run(self):
        self.currectAnswer = self.examData['answer']
        # 检查题型为单选题
        if self.examData['type'] == "单选题":
            if self.answer == self.currectAnswer:
                self.signal.emit(True)
            else:
                self.signal.emit(False)
        # 检查题型为多选题
        elif self.examData['type'] == "多选题":
            if set(self.answer) == set(self.currectAnswer):
                self.signal.emit(True)
            else:
                self.signal.emit(False)
