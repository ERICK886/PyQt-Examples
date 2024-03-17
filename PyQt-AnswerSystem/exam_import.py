import pymysql
import openpyxl
from pymysql.cursors import DictCursor

# 连接数据库
conn = pymysql.connect(host='114.55.248.117', user='root', password='Lj2003!@#', db='exam', cursorclass=DictCursor)
cur = conn.cursor()

# 加载Excel文件
read_excel = openpyxl.load_workbook('exam_2.xlsx')
sheet = read_excel.active

# 遍历Excel表格的第二行及以后的行
for row in sheet.iter_rows(min_row=2):
    # 从Excel表格中获取数据
    id = row[0].value
    info = row[1].value
    title = f"第{row[0].value}题"
    answer = row[3].value
    item_type = row[5].value
    score = row[6].value

    # 创建一个空字典
    dic = {}

    # 将选择题的选项添加到字典中
    for i in row[2].value.split(','):
        dic[i.split(':')[0]] = i.split(':')[1]

    # 判断题型并执行相应的SQL语句
    if item_type == '单选题':
        sql = f"insert into exam_2(id,title,answer, info,type,score,radio) values(%s,%s,%s,%s,%s,%s,%s)"
        cur.execute(sql, (id, title, answer, info, item_type, score, str(dic)))
        conn.commit()
        print(f"第{row[0].value}题插入成功")
    elif item_type == '多选题':
        sql = f"insert into exam_2(id,title,answer, info,type,score, `check`) values(%s,%s,%s,%s,%s,%s,%s)"
        cur.execute(sql, (id, title, answer, info, item_type, score, str(dic)))
        conn.commit()
        print(f"第{row[0].value}题插入成功")
