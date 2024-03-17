import json
from PyQt5.QtWidgets import QMessageBox


class Data:
    def __init__(self):
        # 初始化数据，设置json文件地址
        # student.json格式:
        #
        # {
        #   "student": {
        #     "666": {
        #       "学号": "666",
        #       "姓名": "老刘"
        #       "班级": "学前221",
        #       "性别": "男",
        #       "生日": "2003-11-21",
        #       "地址": "深圳",
        #       "联系电话": "15148751564"
        #     }
        #   },
        #   "class": {
        #     "1": "网络221",
        #     "2": "网络222",
        #     "3": "网络223",
        #     "4": "网络224",
        #     "5": "计算机221",
        #     "6": "计算机222",
        #     "7": "计算机223",
        #     "8": "计算机224",
        #     "9": "小教221",
        #     "10": "小教222",
        #     "11": "小教223",
        #     "12": "小教224",
        #     "13": "学前221",
        #     "14": "学前222",
        #     "15": "学前223",
        #     "16": "学前224"
        #   }
        # }
        self.path = "student.json"

    def read(self):
        try:
            # 读取json文件函数，返回字典
            with open(self.path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data

        except FileNotFoundError:
            # 如果文件不存在，创建文件
            with open(self.path, 'w', encoding='utf-8') as f:
                f.write('{"student": {}, "class": {}}')
            return {"student": {}, "class": {}}

    def write(self, data):
        # 向json文件中写入数据函数
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            return True

    def get_students(self):
        # 获取所有学生信息函数，返回查询结果
        data = self.read()
        if data["student"]:
            return data['student']
        else:
            return {}

    def get_student(self, sno):
        # 根据学号获取学生信息函数，返回查询结果
        data = self.read()
        if data["student"]:
            for k, v in data['student'].items():
                if sno == v['学号']:
                    return v
        else:
            return {}

    def insert_student(self, sno, name, class_, phone, birthday, address, gender):
        # 插入学生信息函数，返回插入结果或异常信息
        data = self.read()
        if data["student"]:
            for k, v in data['student'].items():
                if sno == v['学号']:
                    return "该学号已存在"
        try:
            data['student'][sno] = {
                "学号": sno,
                "姓名": name,
                "班级": class_,
                "性别": gender,
                "生日": birthday,
                "地址": address,
                "联系电话": phone
            }
        except Exception as e:
            QMessageBox.warning(None, "警告", f"插入失败，请检查输入是否正确{e}")
        self.write(data)
        return True

    def delete_student(self, sno):
        # 根据学号删除学生信息函数，返回删除结果或异常信息
        data = self.read()
        if data["student"]:
            for k, v in data['student'].items():
                if sno == v['学号']:
                    del data['student'][k]
                    self.write(data)
                    return True

        else:
            return False

    def edit_student(self, sno, name, class_, phone, birthday, address, gender):
        # 根据学号修改学生信息函数，返回修改结果或异常信息
        data = self.read()
        if data["student"]:
            for k, v in data['student'].items():
                if sno == v['学号']:
                    data['student'][k]['姓名'] = name
                    data['student'][k]['班级'] = class_
                    data['student'][k]['性别'] = gender
                    data['student'][k]['生日'] = birthday
                    data['student'][k]['地址'] = address
                    data['student'][k]['联系电话'] = phone
                    self.write(data)
                    return True

        return False

    def get_classes(self):
        # 获取所有班级信息函数，返回查询结果
        data = self.read()
        print(data["class"])
        if data["class"]:
            return data['class']

        else:
            return {}
