# OpenStackClient环境部署

## 一、下载安装python

访问[Python官网](https://www.python.org/)或者网上查找Python3.9以上版本，下载并安装

## 二、安装必要依赖库

### 1、创建虚拟环境

打开文件资源管理器，新建文件夹，并改名，在地址栏输入`powershell`或者`cmd`访问终端界面。

![](assets\1.png)

输入`python.exe -m venv venv`进行安装虚拟环境

![](assets\2.png)

安装好后将项目文件，解压到当前目录

![](assets\3.png)

```
client
	├─ resources
	├─ ui
	├─ utils
	├─ venv
	├─ logo.ico
	├─ main.py
	└─ requirements.txt	
```

### 2、激活虚拟环境

命令行输入`.\venv\Scripts\activate`，激活虚拟环境

![](assets\4.png)

### 3、安装依赖库

激活后输入`pip install -r requirements.txt`，下载并安装依赖库。

![](assets\5.png)

## 三、启动主程序

输入`python.exe .\main.py`打开主程序

![](assets\6.png)

## 四、Pycharm编辑项目

在项目文件夹下右击，点击更多，选择以pycharm项目打开文件夹

![](assets\7.png)

## 五、主程序代码详解

### 1、主程序

```python
import sys  # 导入sys模块，用于处理命令行参数和退出代码
import webbrowser  # 导入webbrowser模块，用于打开浏览器
from utils import *  # 从utils模块中导入所有内容
from PyQt5.QtWidgets import *  # 从PyQt5.QtWidgets模块中导入所有内容
from PyQt5.QtCore import *  # 从PyQt5.QtCore模块中导入所有内容
from PyQt5.QtGui import *  # 从PyQt5.QtGui模块中导入所有内容
from ui import *  # 从ui模块中导入所有内容


class Login(QWidget, Ui_Login):
    """
    登录类
    """

    def __init__(self, openstack: QStackedWidget, parent):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.openstack = openstack
        self.reader = Session()
        self.pushButton_link.clicked.connect(self.login)
        self.pushButton_exit.clicked.connect(self.parent.close)

    def login(self):
        # 获取IP地址
        ip = self.lineEdit_ip.text()
        # 获取用户名
        username = self.lineEdit_username.text()
        # 获取密码
        password = self.lineEdit_password.text()
        # 获取用户域
        domain = self.lineEdit_userdomain.text()
        # 获取项目
        project = self.lineEdit_userproject.text()

        # 检查用户名和密码是否为空
        if username and password:
            # 创建Openstack连接
            conn = Openstack(ip, username, password, project, domain)
            # 登录并获取状态和令牌
            status, token = conn.login()

            # 如果登录成功
            if status:
                try:
                    # 更新父窗口标题
                    self.parent.setWindowTitle("OpenStack - " + ip)
                    # 创建Index页面
                    self.Index = Index(self.openstack)
                    # 将Index页面添加到openstack布局中
                    self.openstack.addWidget(self.Index)
                    # 设置openstack布局的当前索引为1
                    self.openstack.setCurrentIndex(1)
                except Exception as e:
                    # 弹出警告框提示登录失败以及错误信息
                    MessageBox().warn("警告", f"登录失败！f{e}")
            else:
                # 弹出警告框提示登录失败以及令牌信息
                MessageBox().warn("警告", f"登录失败！{token}")
        else:
            # 弹出警告框提示用户名和密码不能为空
            MessageBox().warn("警告", "用户名和密码不能为空！")


class Index(QWidget, Ui_Index):
    """
    首页类
    """

    def __init__(self, openstack):
        super().__init__()
        self.setupUi(self)  # 初始化界面
        self.reader = Session()  # 创建会话对象
        self.request = Request()  # 创建请求对象
        self.openstack = openstack  # 设置OpenStack对象
        self.adduserdialog = None  # 添加用户对话框初始化
        self.label_logo.setPixmap(QPixmap("resources/img/logo.png").scaled(200, 100, Qt.KeepAspectRatio))  # 设置logo图片
        data = self.reader.read()  # 读取数据
        self.label_link.setText(
            f"""连接IP: {data['ip']}\n用户名: {data['username']}\n域: {data['domain']}""")  # 设置链接IP，用户名和域的信息
        self.pushButton_user.clicked.connect(self.user)  # 用户按钮点击事件连接函数user
        self.pushButton_network.clicked.connect(self.network)  # 网络按钮点击事件连接函数network
        self.pushButton_image.clicked.connect(self.image)  # 镜像按钮点击事件连接函数image
        self.pushButton_server.clicked.connect(self.server)  # 服务器按钮点击事件连接函数server
        self.pushButton_flavor.clicked.connect(self.flavor)  # 实例类型按钮点击事件连接函数flavor
        self.pushButton_api.clicked.connect(self.api)  # API按钮点击事件连接函数api
        self.tree_users.setColumnWidth(0, 160)  # 设置用户树的列宽
        self.tree_users.setColumnWidth(1, 600)
        self.tree_users.setColumnWidth(2, 400)
        self.tree_users.setColumnWidth(3, 600)
        self.tree_users.setColumnWidth(4, 160)
        self.tree_users.setColumnWidth(5, 300)
        self.tree_users.setColumnWidth(6, 160)
        self.tree_users.setColumnWidth(7, 400)
        self.tree_networks.setColumnWidth(0, 260)  # 设置网络树的列宽
        self.tree_networks.setColumnWidth(1, 400)
        self.tree_networks.setColumnWidth(2, 400)
        self.tree_networks.setColumnWidth(3, 400)
        self.tree_networks.setColumnWidth(4, 160)
        self.tree_networks.setColumnWidth(5, 160)
        self.tree_networks.setColumnWidth(6, 160)
        self.tree_networks.setColumnWidth(7, 300)
        self.tree_images.setColumnWidth(0, 160)  # 设置镜像树的列宽
        self.tree_images.setColumnWidth(1, 500)
        self.tree_images.setColumnWidth(2, 400)
        self.tree_images.setColumnWidth(3, 160)
        self.tree_images.setColumnWidth(4, 160)
        self.tree_images.setColumnWidth(5, 160)
        self.tree_images.setColumnWidth(6, 160)
        self.tree_images.setColumnWidth(7, 200)
        self.tree_flavors.setColumnWidth(0, 180)  # 设置配置树的列宽
        self.tree_flavors.setColumnWidth(1, 400)
        self.tree_servers.setColumnWidth(0, 160)  # 设置服务器树的列宽
        self.tree_servers.setColumnWidth(1, 500)
        self.tree_servers.setColumnWidth(2, 500)
        self.tree_servers.setColumnWidth(3, 160)
        self.tree_servers.setColumnWidth(8, 160)
        self.pushButton_deluser.clicked.connect(self.user_del)  # 删除用户按钮点击事件连接函数user_del
        self.push_addneuser_time = QDateTime.currentDateTime()  # 设置添加用户时间
        self.pushButton_adduser.clicked.connect(self.user_add)  # 添加用户按钮点击事件连接函数user_add
        self.pushButton_addsubnet.clicked.connect(self.subnet_add)  # 添加子网按钮点击事件连接函数subnet_add
        self.pushButton_delnetwork.clicked.connect(self.network_del)  # 删除网络按钮点击事件连接函数network_del
        self.push_addnetwork_time = QDateTime.currentDateTime()  # 设置添加网络时间
        self.pushButton_addnetwork.clicked.connect(self.network_add)  # 添加网络按钮点击事件连接函数network_add
        self.pushButton_addimage.clicked.connect(self.image_add)  # 添加图片按钮点击事件连接函数image_add
        self.pushButton_delimage.clicked.connect(self.image_del)  # 删除图片按钮点击事件连接函数image_del
        self.pushButton_addflavors.clicked.connect(self.flavor_add)  # 添加配置按钮点击事件连接函数flavor_add
        self.pushButton_delflavors.clicked.connect(self.flavor_del)  # 删除配置按钮点击事件连接函数flavor_del
        self.pushButton_addservers.clicked.connect(self.server_add)  # 添加服务器按钮点击事件连接函数server_add
        self.pushButton_delservers.clicked.connect(self.server_del)  # 删除服务器按钮点击事件连接函数server_del
        self.pushButton_refresh.clicked.connect(self.refresh)  # 刷新按钮点击事件连接函数refresh
        self.push_refresh_time = QDateTime.currentDateTime()  # 设置刷新时间

    def refresh(self):
        # 刷新函数
        current_time = QDateTime.currentDateTime()
        if self.push_refresh_time.secsTo(current_time) > 5:
            # 如果距离上一次刷新时间大于5秒
            self.push_refresh_time = current_time
            self.show_server_tree_thread()
        else:
            # 如果距离上一次刷新时间小于等于5秒
            MessageBox().warn("警告", "刷新间隔不能小于5秒！")

    def show_user_tree_thread(self):
        # 显示用户树的线程
        self.userthread = ShowUserTrees(self)
        self.userthread.start()

        def finished(flag):
            # 结束信号的处理函数
            if flag:
                # 如果需要结束线程
                self.userthread.quit()
                self.userthread = None

        # 将结束信号的处理函数绑定到线程的信号上
        self.userthread.signal.connect(finished)

    def show_network_tree_thread(self):
        self.nethread = ShowNetworkTrees(self)  # 创建ShowNetworkTrees对象并赋值给self.nethread
        self.nethread.start()  # 启动self.nethread线程

        def finished(flag):
            if flag:  # 如果flag为True
                self.nethread.quit()  # 终止self.nethread线程
                self.nethread = None  # 将self.nethread置为None

        self.nethread.signal.connect(finished)  # 将finished函数连接到self.nethread的signal信号上

    def show_image_tree_thread(self):
        # 显示镜像树线程
        self.imgthread = ShowImageTrees(self)
        self.imgthread.start()

        def finished(flag):
            # 完成标志
            if flag:
                # 结束镜像树线程
                self.imgthread.quit()
                self.imgthread = None

        # 连接镜像树线程的信号
        self.imgthread.signal.connect(finished)

    def show_flavor_tree_thread(self):
        # 展示实例类型树线程
        self.flathread = ShowFlavorTrees(self)
        self.flathread.start()

        def finished(flag):
            # 如果标志为真
            if flag:
                # 结束实例类型树线程
                self.flathread.quit()
                self.flathread = None

        # 连接实例类型树线程的信号
        self.flathread.signal.connect(finished)

    def show_server_tree_thread(self):
        # 创建一个ShowServerTrees对象，传入self作为参数
        self.serthread = ShowServerTrees(self)
        # 启动线程
        self.serthread.start()
        # 禁用刷新按钮
        self.pushButton_refresh.setDisabled(True)

        def finished(flag):
            # 如果flag为真
            if flag:
                # 启用刷新按钮
                self.pushButton_refresh.setEnabled(True)
                # 结束线程
                self.serthread.quit()
                # 将线程置为None
                self.serthread = None

        # 连接线程的信号
        self.serthread.signal.connect(finished)

    def server_add(self):
        dialog = AddServer(self)
        dialog.exec_()

    def server_del(self):
        # 获取当前选择的项目
        item = self.tree_servers.currentItem()
        if item:
            # 判断文本是否为数字
            if item.text(0).isdigit():
                # 弹出确认对话框
                flag = MessageBox().quest("提示", "确定删除该云主机吗？")
                if flag:
                    try:
                        # 获取服务器ID
                        server_id = item.text(2)
                        # 发送删除服务器请求
                        res = self.request.delete_server(server_id)
                        if res:
                            # 更新服务器列表
                            self.show_server_tree_thread()
                            # 弹出删除成功提示框
                            MessageBox().info("提示", "云主机删除成功！")
                    except Exception as e:
                        # 弹出删除失败提示框，并显示错误信息
                        MessageBox().warn("警告", f"云主机删除失败！{e}")

    def flavor_add(self):
        dialog = AddFlavor(self)
        dialog.exec_()

    def flavor_del(self):
        """
        删除云主机类型
        """
        item = self.tree_flavors.currentItem()
        if item:
            if item.text(0).isdigit():
                flag = MessageBox().quest("提示", "确定删除该云主机类型吗？")
                if flag:
                    try:
                        flavor_id = item.text(2)
                        res = self.request.delete_flavor(flavor_id)
                        if res:
                            self.show_flavor_tree_thread()
                            MessageBox().info("提示", "云主机类型删除成功！")
                    except Exception as e:
                        MessageBox().warn("警告", f"云主机类型删除失败！{e}")

    def image_add(self):
        dialog = AddImage(self)
        dialog.exec_()

    def image_del(self):
        """
        删除镜像
        """
        # 获取当前选中的菜单项
        item = self.tree_images.currentItem()
        if item:
            # 检查选中的菜单项的第一列是否为数字
            if item.text(0).isdigit():
                # 弹出确认框，确认是否删除该镜像
                flag = MessageBox().quest("提示", "确定删除该镜像吗？")
                if flag:
                    try:
                        # 获取选中镜像的ID
                        image_id = item.text(2)
                        # 调用请求接口删除镜像
                        res = self.request.delete_image(image_id)
                        if res:
                            # 刷新镜像树表格
                            self.show_image_tree_thread()
                            # 弹出成功提示框
                            MessageBox().info("提示", "镜像删除成功！")
                        else:
                            # 弹出失败提示框
                            MessageBox().warn("警告", "镜像删除失败！")
                    except Exception as e:
                        # 弹出失败提示框，显示异常信息
                        MessageBox().warn("警告", f"镜像删除失败！{e}")

    def network_del(self):
        """
        删除网络
        """
        item = self.tree_networks.currentItem()  # 获取当前选中的树形控件项
        if item:  # 判断是否选择了项
            if item.text(0).isdigit():  # 判断该项的第一个文本是否为数字
                flag = MessageBox().quest("提示", "确定删除该网络吗？")  # 弹出确认窗口，询问是否删除该网络
                if flag:  # 如果用户选择确认删除
                    try:
                        network_id = item.text(2)  # 获取网络id
                        res = self.request.delete_network(network_id)  # 调用请求类的删除网络方法
                        if res:  # 如果删除成功
                            self.show_network_tree_thread()  # 显示网络树线程
                            MessageBox().info("提示", "网络删除成功！")  # 弹出提示窗口，显示网络删除成功
                        else:
                            MessageBox().warn("警告", "网络删除失败！")  # 弹出警告窗口，显示网络删除失败
                    except Exception as e:
                        MessageBox().warn("警告", f"网络删除失败！{e}")  # 弹出警告窗口，显示网络删除失败的原因

    def subnet_add(self):
        item = self.tree_networks.currentItem()  # 获取当前选中的树形控件项
        if item:  # 判断是否选择了项
            if item.text(0).isdigit():  # 判断该项的第一个文本是否为数字
                network_id = item.text(2)  # 获取网络id
                try:
                    dialog = AddSubnet(network_id)  # 创建添加子网对话框
                    if not dialog.exec():  # 如果对话框未执行成功
                        self.show_network_tree_thread()  # 显示网络树线程
                        return  # 返回
                except Exception as e:  # 捕获异常
                    MessageBox().warn("警告", f"添加子网失败！{e}")  # 弹出警告窗口，显示添加子网失败的原因

    def user_del(self):
        """
        删除用户函数
        """
        item = self.tree_users.currentItem()
        if item:
            if item.text(0).isdigit():
                flag = MessageBox().quest("提示", "确定删除该用户吗？")
                if flag:
                    admin_users = {'admin', 'glance', 'nova', 'cinder', 'keystone', 'neutron', 'heat', 'ceilometer',
                                   'trove', 'swift', 'designate', 'manila', 'ironic', 'magnum', 'heat_domain_admin',
                                   'placement', 'gnocchi', 'aodh', 'sahara', 'barbican', 'cloudkitty', 'demo'}

                    if item.text(1) in admin_users:
                        MessageBox().warn('警告', '不能删除系统用户')
                        return
                    try:
                        user_id = item.text(2)
                        res = self.request.delete_user(user_id)
                        if res:
                            MessageBox().info('提示', '删除用户成功')
                            self.show_user_tree_thread()
                    except Exception as e:
                        MessageBox().warn('警告', f'系统错误：{e}')

            else:
                MessageBox().warn('警告', '请选择用户')

    def user_add(self):
        # 获取当前时间
        current_time = QDateTime.currentDateTime()
        # 如果距离上一次添加用户时间小于4秒，则显示警告消息并返回
        if self.push_addneuser_time.secsTo(current_time) < 4:
            MessageBox().warn('警告', '请勿频繁添加用户')
            return
        # 将adduserdialog变量置为空
        self.adduserdialog = None
        # 实例化AddUser对话框并显示
        self.adduserdialog = AddUser(self)
        self.adduserdialog.show()
        # 更新push_addneuser_time变量为当前时间
        self.push_addneuser_time = QDateTime.currentDateTime()

    def network_add(self):
        # 获取当前时间
        current_time = QDateTime.currentDateTime()
        # 如果距离上一次添加网络时间小于4秒，则显示警告消息并返回
        if self.push_addnetwork_time.secsTo(current_time) < 4:
            MessageBox().warn('警告', '请勿频繁添加网络')
            return
        # 将addnetworkdialog变量置为空
        self.addnetworkdialog = None
        # 实例化AddNetwork对话框并显示
        self.addnetworkdialog = AddNetwork(self)
        self.addnetworkdialog.show()
        # 更新push_addnetwork_time变量为当前时间
        self.push_addnetwork_time = QDateTime.currentDateTime()

    def api(self):
        # 设置当前标签页为第一个标签页
        self.stackedWidget.setCurrentIndex(0)

    def user(self):
        # 设置当前标签页为第二个标签页
        self.stackedWidget.setCurrentIndex(1)

    def network(self):
        # 设置当前标签页为第三个标签页
        self.stackedWidget.setCurrentIndex(2)

    def image(self):
        # 设置当前标签页为第四个标签页
        self.stackedWidget.setCurrentIndex(3)

    def server(self):
        # 设置当前标签页为第五个标签页
        self.stackedWidget.setCurrentIndex(4)

    def flavor(self):
        # 设置当前标签页为第六个标签页
        self.stackedWidget.setCurrentIndex(5)


class AddServer(QDialog, Ui_AddServer):
    def __init__(self, parent: Index):
        super().__init__()
        self.setupUi(self)  # 初始化界面
        self.setWindowIcon(QIcon('logo.ico'))  # 设置窗口图标
        self.setWindowTitle('添加云主机')  # 设置窗口标题
        self.parent = parent  # 保存父对象
        self.request = Request()  # 创建Request对象
        self.server_name = ''  # 保存服务器名称
        self.image_id = ''  # 保存镜像ID
        self.flavor_id = ''  # 保存规格ID
        self.network_id = ''  # 保存网络ID
        self.show_add_server()  # 显示添加服务器界面
        self.zone_view = QListView()  # 创建区域视图
        self.zone_view.setStyleSheet("""QListView {
                                                    background-color: white;
                                                }
                                                
                                                QListView::item {
                                                    background-color: white;
                                                }
                                                
                                                QListView::item:selected {
                                                    background-color: #C32E24;
                                                    color: white;
                                                }""")
        self.comboBox_add_serverzone.setView(self.zone_view)  # 绑定区域下拉框和区域视图

        self.image_view = QListView()  # 创建镜像视图
        self.image_view.setStyleSheet("""QListView {
                                                    background-color: white;
                                                }
                                                
                                                QListView::item {
                                                    background-color: white;
                                                }
                                                
                                                QListView::item:selected {
                                                    background-color: #C32E24;
                                                    color: white;
                                                }""")
        self.comboBox_add_serverimage.setView(self.image_view)  # 绑定镜像下拉框和镜像视图

        self.flavor_view = QListView()  # 创建规格视图
        self.flavor_view.setStyleSheet("""QListView {
                                                    background-color: white;
                                                }
                                                
                                                QListView::item {
                                                    background-color: white;
                                                }
                                                
                                                QListView::item:selected {
                                                    background-color: #C32E24;
                                                    color: white;
                                                }""")
        self.comboBox_add_serverflavor.setView(self.flavor_view)  # 绑定规格下拉框和规格视图
        self.network_view = QListView()  # 创建网络视图
        self.network_view.setStyleSheet("""QListView {
                                                    background-color: white;
                                                }
                                                
                                                QListView::item {
                                                    background-color: white;
                                                }
                                                
                                                QListView::item:selected {
                                                    background-color: #C32E24;
                                                    color: white;
                                                }""")
        self.comboBox_add_servernetwork.setView(self.network_view)  # 绑定网络下拉框和网络视图
        self.comboBox_add_serverzone.addItem('nova')  # 添加区域下拉框选项
        self.pushButton_add_addserver.clicked.connect(self.add_server)  # 连接添加服务器按钮的点击事件和add_server函数

    def show_add_server(self):
        """
        显示添加服务器界面
        """
        try:
            images = self.request.get_images()  # 获取可用的镜像列表
            flavors = self.request.get_flavors()  # 获取可用的规格列表
            networks = self.request.get_networks()  # 获取可用的网络列表
            if images and flavors and networks:  # 判断是否有可用的镜像、规格和网络
                for image in images:  # 遍历镜像列表
                    self.comboBox_add_serverimage.addItem(image['name'])  # 将镜像名称添加到下拉框
                for flavor in flavors:  # 遍历规格列表
                    self.comboBox_add_serverflavor.addItem(flavor['name'])  # 将规格名称添加到下拉框
                self.comboBoxList = []  # 初始化组合框列表
                for network in networks:  # 遍历网络列表
                    self.comboBox_add_servernetwork.addItem(network['name'])  # 将网络名称添加到下拉框
        except Exception as e:  # 捕获异常
            MessageBox().warn('警告', f'系统错误：{e}')  # 弹出警告消息框，显示系统错误信息

    def add_server(self):
        try:
            # 获取输入的云主机名称
            self.server_name = self.lineEdit_add_servername.text()
            # 如果云主机名称为空，则弹出警告消息并返回
            if self.server_name == '':
                MessageBox().warn('警告', '请输入云主机名称')
                return
            # 遍历镜像列表，找到与下拉框中选中的镜像名称对应的镜像ID
            for image in self.request.get_images():
                if image['name'] == self.comboBox_add_serverimage.currentText():
                    self.image_id = image['id']
                    break
            # 遍历规格列表，找到与下拉框中选中的规格名称对应的规格ID
            for flavor in self.request.get_flavors():
                if flavor['name'] == self.comboBox_add_serverflavor.currentText():
                    self.flavor_id = flavor['id']
                    break
            # 遍历网络列表，找到与下拉框中选中的网络名称对应的网络ID
            for network in self.request.get_networks():
                if network['name'] == self.comboBox_add_servernetwork.currentText():
                    self.network_id = network['id']
                    break
            # 获取选择的可用区
            self.zone = self.comboBox_add_serverzone.currentText()
            # 调用请求对象的add_server方法添加云主机，参数为云主机名称、镜像ID、规格ID、网络ID和可用区
            res = self.request.add_server(self.server_name, self.image_id, self.flavor_id, self.network_id, self.zone)
            # 如果添加成功，弹出提示消息，刷新服务器树并关闭当前窗口
            if res:
                MessageBox().info('提示', '添加云主机成功')
                self.parent.show_server_tree_thread()
                self.close()
        except Exception as e:
            # 如果出现系统错误，弹出警告消息，错误信息为异常的字符串表示
            MessageBox().warn('警告', f'系统错误：{e}')


class AddFlavor(QDialog, Ui_AddFlavor):
    def __init__(self, parent: Index):
        super().__init__()
        self.setupUi(self)  # 初始化界面
        self.setWindowIcon(QIcon('logo.ico'))  # 设置窗口图标
        self.setWindowTitle('添加云主机类型')  # 设置窗口标题
        self.parent = parent  # 保存父对象
        self.request = Request()  # 创建请求对象
        self.flavor_name = ''  # 初始化云主机类型名称
        self.flavor_id = ''  # 初始化云主机类型ID
        self.vcpus = 0  # 初始化CPU核心数
        self.ram = 0  # 初始化内存大小
        self.disk = 0  # 初始化磁盘大小
        self.ephemeral = 0  # 初始化临时磁盘大小
        self.rxtx = 1  # 初始化网络带宽
        self.swap = 0  # 初始化交换区大小
        self.pushButton_add_addflavor.clicked.connect(self.add_flavor)  # 连接按钮点击事件到add_flavor方法

    def add_flavor(self):
        """
        添加云主机类型
        """
        try:
            # 获取输入的云主机类型名称
            self.flavor_name = self.lineEdit_add_flavorname.text()
            if self.flavor_name == '':
                # 如果名称为空，则弹出警告对话框提示用户输入云主机类型名称
                MessageBox().warn('警告', '请输入云主机类型名称')
                return

            # 获取输入的云主机类型CPU数量
            self.vcpus = int(self.spinBox_add_flavorvcpu.text())
            if self.vcpus == 0:
                # 如果CPU数量为0，则弹出警告对话框提示用户输入云主机类型CPU数量
                MessageBox().warn('警告', '请输入云主机类型CPU数量')
                return
            elif self.vcpus < 1:
                # 如果CPU数量小于1，则弹出警告对话框提示用户云主机类型CPU数量不能小于1
                MessageBox().warn('警告', '云主机类型CPU数量不能小于1')
                return

            # 获取输入的云主机类型内存大小
            self.ram = int(self.spinBox_add_flavorram.text())
            if self.ram == 0:
                # 如果内存大小为0，则弹出警告对话框提示用户输入云主机类型内存大小
                MessageBox().warn('警告', '请输入云主机类型内存大小')
                return
            elif self.ram < 1:
                # 如果内存大小小于1，则弹出警告对话框提示用户云主机类型内存大小不能小于1
                MessageBox().warn('警告', '云主机类型内存大小不能小于1')
                return

            # 获取输入的云主机类型磁盘大小
            self.disk = int(self.spinBox_add_flavordisk.text())
            if self.disk == 0:
                # 如果磁盘大小为0，则弹出警告对话框提示用户输入云主机类型磁盘大小
                MessageBox().warn('警告', '请输入云主机类型磁盘大小')
                return
            elif self.disk < 1:
                # 如果磁盘大小小于1，则弹出警告对话框提示用户云主机类型磁盘大小不能小于1
                MessageBox().warn('警告', '云主机类型磁盘大小不能小于1')
                return

            # 获取输入的云主机类型ID
            self.flavor_id = self.lineEdit_add_flavorid.text()
            if self.flavor_id != '':
                # 遍历已存在的云主机类型，如果输入的ID已存在，则弹出警告对话框提示用户
                for flavor in self.request.get_flavors():
                    if flavor['id'] == self.flavor_id:
                        MessageBox().warn('警告', '云主机类型ID已存在')
                        return

            # 获取输入的交换区大小
            self.swap = self.spinBox_add_flavorswap.text()
            # 获取输入的临时磁盘大小
            self.ephemeral = self.spinBox_add_flavorephemeral.text()
            # 获取输入的网络带宽
            self.rxtx = self.spinBox_add_flavorrxtx.text()
            # 调用请求对象的add_flavor方法，传入参数，并获取返回结果
            res = self.request.add_flavor(self.flavor_name, self.ram, self.vcpus, self.disk, self.ephemeral, self.swap,
                                          self.rxtx, self.flavor_id)
            if res:
                # 如果添加成功，则弹出提示对话框提示用户添加云主机类型成功
                MessageBox().info('提示', '添加云主机类型成功')
                # 重新显示 flavor tree
                self.parent.show_flavor_tree_thread()
                # 关闭当前窗口
                self.close()
        except Exception as e:
            # 如果发生系统错误，则弹出警告对话框显示错误信息
            MessageBox().warn('警告', f'系统错误：{e}')


class AddImage(QDialog, Ui_AddImage):
    def __init__(self, parent: Index):
        super().__init__()
        self.setupUi(self)  # 设置UI布局
        self.setWindowIcon(QIcon('logo.ico'))  # 设置窗口图标
        self.setWindowTitle('添加镜像')  # 设置窗口标题
        self.parent = parent  # 保存父对象
        self.request = Request()  # 创建请求对象
        self.file = None  # 初始化文件变量
        self.visibility = 'shared'  # 初始化可见性变量
        self.prtected = False  # 初始化保护变量
        self.disk_format_listview = QListView()  # 创建磁盘格式的QListView对象
        self.disk_format_listview.setStyleSheet("""QListView {
                                                    background-color: white;
                                                }
                                                
                                                QListView::item {
                                                    background-color: white;
                                                }
                                                
                                                QListView::item:selected {
                                                    background-color: #C32E24;
                                                    color: white;
                                                }""")  # 设置QListView样式表
        self.comboBox_add_disk_format.setView(self.disk_format_listview)  # 设置下拉框的视图为QListView
        self.comboBox_add_disk_format.addItems(  # 添加下拉框的选项
            ['iso-光盘镜像', 'ova-开放式虚拟设备', 'ploop-并行回环磁盘', 'qcow2-QEMU模拟器', 'vdi-虚拟磁盘镜像',
             'vhd-虚拟硬盘', 'vmdk-虚拟机磁盘', 'aki-Amazon 内核镜像', 'ami-Amazon 机器镜像', 'ari-Amazon Ramdisk镜像',
             'docker-Docker镜像'])  # 添加下拉框的选项
        self.lineEdit_add_imagefile.setReadOnly(True)  # 设置文本框只读
        self.pushButton_add_addimage.clicked.connect(self.add_image)  # 连接添加按钮的点击事件到add_image函数
        self.pushButton_add_imagefile.clicked.connect(self.select_file)  # 连接选择文件按钮的点击事件到select_file函数
        self.checkBox_add_add_ifprotected.toggled.connect(
            self.check_add_ifprotected)  # 连接复选框的选中/取消事件到check_add_ifprotected函数
        self.radioButton_add_public.clicked.connect(self.radio_visibility)  # 连接公共广播按钮的点击事件到radio_visibility函数
        self.radioButton_add_private.clicked.connect(self.radio_visibility)  # 连接私有广播按钮的点击事件到radio_visibility函数
        self.radioButton_add_shared.clicked.connect(self.radio_visibility)  # 连接共享广播按钮的点击事件到radio_visibility函数
        self.radioButton_add_social.clicked.connect(self.radio_visibility)  # 连接社交广播按钮的点击事件到radio_visibility函数

    def radio_visibility(self):
        # 当单击公共广播按钮时，将visibility设置为'public'
        if self.radioButton_add_public.isChecked():
            self.visibility = 'public'
        # 当单击私有广播按钮时，将visibility设置为'private'
        elif self.radioButton_add_private.isChecked():
            self.visibility = 'private'
        # 当单击共享广播按钮时，将visibility设置为'shared'
        elif self.radioButton_add_shared.isChecked():
            self.visibility = 'shared'
        # 当单击社交广播按钮时，将visibility设置为'community'
        elif self.radioButton_add_social.isChecked():
            self.visibility = 'community'
        # 如果没有选中上述任何一个广播按钮，则将visibility设置为'shared'的默认值
        else:
            self.visibility = 'shared'

    def check_add_ifprotected(self):
        if self.checkBox_add_add_ifprotected.isChecked():
            self.prtected = True
        else:
            self.prtected = False

    def select_file(self):
        # 选择镜像文件
        # 获取打开文件对话框选中的文件路径和文件名
        self.file, _ = QFileDialog.getOpenFileName(self, '选择镜像文件', 'D:/', 'All Files (*.*)')
        # 如果选中了文件
        if self.file:
            # 在lineEdit_add_imagefile文本框中输入选中的文件路径和文件名
            self.lineEdit_add_imagefile.setText(self.file)
        # 如果未选中文件
        else:
            # 在lineEdit_add_imagefile文本框中输入空文本
            self.lineEdit_add_imagefile.setText('')

    def add_image(self):
        # 添加镜像函数

        try:
            # 获取镜像名称
            self.imagename = self.lineEdit_add_imagename.text()
            # 判断镜像名称是否为空
            if self.imagename == '':
                # 如果为空，则显示警告消息并返回
                MessageBox().warn('警告', '镜像名称不能为空')
                return

            # 获取镜像描述
            self.imagedesc = self.lineEdit_add_imagedesc.text()
            # 获取磁盘格式
            self.disk_format = self.comboBox_add_disk_format.currentText().split('-')[0]
            # 获取最小磁盘大小
            self.min_disk = self.spinBox_add_min_disk.text()
            # 获取最小内存大小
            self.min_ram = self.spinBox_add_min_ram.text()
            # 如果未选择镜像文件，则显示警告消息并返回
            if self.file is None:
                MessageBox().warn('警告', '请选择镜像文件')
                return

            # 创建上传镜像文件的线程对象
            self.uploadimgthread = UploadImageFileThread(self)
            # 绑定线程结束信号与finished方法
            self.uploadimgthread.signal.connect(self.finished)
            # 启动线程

        except Exception as e:
            # 如果发生异常，则显示警告消息并输出错误信息
            MessageBox().warn('警告', f'系统错误：{e}')

    def finished(self):
        """
        完成上传镜像文件的操作，并执行以下操作：
        1. 弹出一个提示框，显示"添加镜像成功"
        2. 调用父窗口的方法，显示图像树
        3. 关闭上传线程
        4. 将上传线程置为空
        5. 关闭当前窗口
        """
        MessageBox().info('提示', '添加镜像成功')
        self.parent.show_image_tree_thread()
        self.uploadimgthread.quit()
        self.uploadimgthread = None
        self.close()


class AddSubnet(QDialog, Ui_AddSubnet):
    def __init__(self, network_id):
        super().__init__()
        self.setupUi(self)  # 设置对话框的布局和组件
        self.request = Request()  # 创建一个Request对象
        self.network_id = network_id  # 子网所属的网络ID
        self.setWindowIcon(QIcon('logo.ico'))  # 设置对话框的窗口图标
        self.setWindowTitle('添加子网')  # 设置对话框的标题
        self.show_version()  # 显示版本信息
        self.subnet_name = ''  # 子网名称初始化为空字符串
        self.ip_version = 4  # IP版本初始化为4
        self.cidr = ''  # CIDR初始化为空字符串
        self.gateway_ip = ''  # 网关IP初始化为空字符串
        self.bangateway = True  # 是否设置网关初始化为True
        self.dhcp = False  # 是否开启DHCP初始化为False
        self.ip_pools = []  # IP池初始化为空列表
        self.dns_nameservers = []  # DNS服务器初始化为空列表
        self.hosts_routes = []  # 主机路由初始化为空列表
        self.add_subnetipversion = QListView()  # 创建一个QListView对象用于显示IP版本
        self.add_subnetipversion.setStyleSheet("""QListView{background-color: white;}QListView::item{background-color: white
                                                        ;}QListView::item:selected {background-color: #C32E24;color: white;}""")  # 设置QListView的样式
        self.comboBox_add_subnetipversion.setView(self.add_subnetipversion)  # 将QComboBox的视图设置为QListView
        self.pushButton_add_addsubnet.clicked.connect(self.add_subnet)  # 连接按钮的点击事件与add_subnet函数
        self.checkBox_add_subnetifgateway.clicked.connect(self.ifgateway)  # 连接复选框的点击事件与ifgateway函数

    def show_version(self):
        # 展示可用的IP版本
        ip_versions = ['IPv4', 'IPv6']
        for i in range(0, 2):
            self.comboBox_add_subnetipversion.addItem(ip_versions[i])

    def ifgateway(self):
        # 判断是否设置网关
        if self.checkBox_add_subnetifgateway.isChecked():
            self.lineEdit_add_subnetgatewayip.setText('')
            self.lineEdit_add_subnetgatewayip.setEnabled(False)
        else:
            self.lineEdit_add_subnetgatewayip.setEnabled(True)

    def add_subnet(self):
        """
        添加子网
        """
        self.subnet_name = ''
        self.ip_version = 4
        self.cidr = ''
        self.gateway_ip = ''
        self.bangateway = True
        self.dhcp = False
        self.ip_pools = []
        self.dns_nameservers = []
        self.hosts_routes = []

        try:
            self.subnet_name = self.lineEdit_add_subnetname.text()
            if self.subnet_name == '':
                MessageBox().warn('警告', '请输入子网名称')
                return
            if self.network_id == '':
                MessageBox().warn('警告', '请选择网络')
                return

            # 获取子网IP版本
            self.ip_version = self.comboBox_add_subnetipversion.currentText()
            self.ip_version = int(str(self.ip_version)[-1])

            # 获取子网CIDR
            self.cidr = self.lineEdit_add_subnetcidr.text()

            # 判断是否设置网关
            if self.checkBox_add_subnetifgateway.isChecked():
                self.bangateway = True
                self.gateway_ip = ''
            else:
                self.gateway_ip = self.lineEdit_add_subnetgatewayip.text()
                self.bangateway = False

            # 判断是否开启DHCP
            self.dhcp = self.checkBox_add_subnetifdhcp.isChecked()

            try:
                # 获取地址池信息
                ip_pools = self.textEdit_add_subnetipool.toPlainText()
                if ip_pools != '':
                    for ip_pool in ip_pools.split('\n'):
                        ip_pool = ip_pool.strip().split(',')
                        ip_dict = {'start': ip_pool[0], 'end': ip_pool[1]}
                        if ip_pools != {}:
                            self.ip_pools.append(ip_dict)
            except Exception as e:
                MessageBox().warn('警告',
                                  f'输入错误，地址池格式：开始IP结束IP(例如：192.168.1.100,192.168.1.120)，每行一条记录')
                return

            try:
                # 获取DNS服务器信息
                dns_nameservers = self.textEdit_add_subnetdns.toPlainText()
                if dns_nameservers != '':
                    for dns_nameserver in dns_nameservers.split('\n'):
                        dns_nameserver = dns_nameserver.strip()
                        if dns_nameserver != '':
                            self.dns_nameservers.append(dns_nameserver)
            except Exception as e:
                MessageBox().warn('警告', f'输入错误，DNS服务器格式：IP地址(例如：8.8.8.8)，每行一条记录')
                return

            try:
                # 获取路由信息
                host_routes = self.textEdit_add_subnetroute.toPlainText()
                if host_routes != '':
                    for host_route in host_routes.split('\n'):
                        host_route = host_route.strip().split(',')
                        host_route_dict = {'destination': host_route[0], 'nexthop': host_route[1]}
                        if host_route != '':
                            self.hosts_routes.append(host_route_dict)
            except Exception as e:
                MessageBox().warn('警告',
                                  f'输入错误，路由格式：目的CIDR，下一跳(例如192.168.200.0/24,10.56.1.254)，每行一条记录')
                return

            # 调用接口添加子网
            res = self.request.add_subnet(self.subnet_name, self.network_id, self.ip_version, self.cidr, self.dhcp,
                                          self.gateway_ip, self.ip_pools, self.dns_nameservers,
                                          self.hosts_routes)

            if res:
                self.close()
                MessageBox().info('提示', '添加子网成功')
        except Exception as e:
            MessageBox().warn('警告', f'添加子网失败，错误信息：{e}')


class AddUser(QDialog, Ui_AddUser):
    def __init__(self, parent: Index):
        super().__init__()
        self.setupUi(self)  # 设置UI布局
        self.request = Request()  # 创建Request对象
        self.parent = parent  # 设置父对象
        self.setWindowIcon(QIcon('logo.ico'))  # 设置窗口图标
        self.setWindowTitle('添加用户')  # 设置窗口标题
        self.show_domain_project()  # 显示域名和项目
        self.domain_listview = QListView()  # 创建域名列表视图
        self.domain_listview.setStyleSheet("""QListView{background-color: white;}QListView::item{background-color: white
                                                        ;}QListView::item:selected {background-color: #C32E24;color: white;}""")
        self.comboBox_add_domain.setView(self.domain_listview)  # 设置域名下拉框的视图
        self.project_listview = QListView()  # 创建项目列表视图
        self.project_listview.setStyleSheet("""QListView{background-color: white;}QListView::item{background-color: white
                                                        ;}QListView::item:selected {background-color: #C32E24;color: white;}""")
        self.comboBox_add_project.setView(self.project_listview)  # 设置项目下拉框的视图
        self.pushButton_add_adduer.clicked.connect(self.add_user)  # 连接添加用户按钮的点击事件
        self.pushButton_add_cancel.clicked.connect(self.close)  # 连接取消按钮的点击事件

    def show_domain_project(self):
        """
        显示域名与项目

        """
        try:
            self.combox_domain = {}  # 域名字典
            self.combox_project = {}  # 项目字典
            domains = self.request.get_domains()  # 获取域名列表
            for domain in domains:
                self.combox_domain[domain['id']] = domain['name']  # 将域名id与名称对应关系存入字典
                self.comboBox_add_domain.addItem(domain['name'])  # 向添加域名下拉框添加选项

            projects = self.request.get_projects()  # 获取项目列表
            for project in projects:
                self.combox_project[project['id']] = project['name']  # 将项目id与名称对应关系存入字典
                self.comboBox_add_project.addItem(project['name'])  # 向添加项目下拉框添加选项
        except Exception as e:
            MessageBox().warn('警告', f'系统错误：{e}')  # 弹出警告窗口提示系统错误信息

    def add_user(self):
        # 添加用户函数
        if self.lineEdit_add_username.text() == '':
            # 如果用户名为空，则弹出警告提示
            MessageBox().warn('警告', '用户名不能为空')
        elif self.lineEdit_add_password.text() == '':
            # 如果密码为空，则弹出警告提示
            MessageBox().warn('警告', '密码不能为空')
        else:
            try:
                users = self.request.get_users()
                # 获取用户名、密码、领域ID、项目ID和描述信息
                username = self.lineEdit_add_username.text()
                for user in users:
                    if user['name'] == username:
                        MessageBox().warn('警告', '用户名已存在')
                        return
                password = self.lineEdit_add_password.text()
                domain_id = ''
                project_id = ''

                # 遍历领域下拉框，如果当前选中的文本与下拉框某个项相等，则将该项的键值赋给领域ID
                for k, v in self.combox_domain.items():
                    if v == self.comboBox_add_domain.currentText():
                        domain_id = k

                # 遍历项目下拉框，如果当前选中的文本与下拉框某个项相等，则将该项的键值赋给项目ID
                for k, v in self.combox_project.items():
                    if v == self.comboBox_add_project.currentText():
                        project_id = k

                # 获取描述信息
                desc = self.lineEdit_add_desc.text()

                # 调用request对象的add_user方法添加用户
                res = self.request.add_user(username, password, domain_id, project_id, desc)

                if res:
                    # 如果添加用户成功，则弹出提示框，刷新父窗口并关闭当前窗口
                    MessageBox().info('提示', '添加用户成功')
                    self.parent.show_user_tree_thread()
                    self.close()
                else:
                    # 如果添加用户失败，则弹出警告提示
                    MessageBox().warn('警告', '添加用户失败')
            except Exception as e:
                # 捕获异常并弹出警告提示，显示系统错误信息
                MessageBox().warn('警告', f'系统错误：{e}')


class AddNetwork(QDialog, Ui_AddNetwork):
    def __init__(self, parent: Index):
        super().__init__()
        self.parent = parent
        self.provider = ''  # 服务提供者
        self.zone = ''  # 区域
        self.networktype = ''  # 网络类型
        self.network_projectid = ''  # 网络项目ID
        self.networkname = ''  # 网络名称
        self.networkdesc = ''  # 网络描述
        self.admin_state_up = False  # 管理状态
        self.shared = False  # 是否共享
        self.outnetwork = False  # 是否外部网络
        self.ifsubnet = False  # 是否有子网
        self.setupUi(self)  # 设置UI
        self.request = Request()  # 请求对象
        self.setWindowIcon(QIcon('logo.ico'))  # 设置窗口图标
        self.setWindowTitle('创建网络')  # 设置窗口标题
        self.show_add_network()  # 显示添加网络界面
        self.add_networkproject_listview = QListView()  # 添加网络项目列表视图
        self.add_networkproject_listview.setStyleSheet("""QListView{background-color: white;}QListView::item{background-color: white
                                                        ;}QListView::item:selected {background-color: #C32E24;color: white;}""")
        self.comboBox_add_networkproject.setView(self.add_networkproject_listview)  # 设置组合框视图为网络项目列表视图

        self.add_networktype_listview = QListView()  # 添加网络类型列表视图
        self.add_networktype_listview.setStyleSheet("""QListView{background-color: white;}QListView::item{background-color: white
                                                        ;}QListView::item:selected {background-color: #C32E24;color: white;}""")
        self.comboBox_add_networktype.setView(self.add_networktype_listview)  # 设置组合框视图为网络类型列表视图

        self.add_networkzone_listview = QListView()  # 添加网络区域列表视图
        self.add_networkzone_listview.setStyleSheet("""QListView{background-color: white;}QListView::item{background-color: white
                                                        ;}QListView::item:selected {background-color: #C32E24;color: white;}""")
        self.comboBox_add_networkzone.setView(self.add_networkzone_listview)  # 设置组合框视图为网络区域列表视图
        self.pushButton_add_addnetwork.clicked.connect(self.create_network)  # 连接添加网络按钮的点击事件到create_network函数
        self.pushButton_add_cancelnetwork.clicked.connect(self.close)  # 连接取消网络按钮的点击事件到close函数

    def show_add_network(self):
        """
        显示添加网络页面

        :param self: 当前对象
        """
        try:
            projects = self.request.get_projects()  # 获取项目列表
            for project in projects:  # 遍历项目列表
                self.comboBox_add_networkproject.addItem(project['name'])  # 将项目名称添加到下拉框
            network_type_items = ['vlan', 'vxlan', 'geneve', 'gre', 'flat', 'local']  # 网络类型列表
            for network_type in network_type_items:  # 遍历网络类型列表
                self.comboBox_add_networktype.addItem(network_type)  # 将网络类型添加到下拉框
            zones = ['nova']  # 区域列表
            for zone in zones:  # 遍历区域列表
                self.comboBox_add_networkzone.addItem(zone)  # 将区域添加到下拉框
        except Exception as e:  # 异常处理
            MessageBox().warn('警告', f'系统错误：{e}')  # 显示警告消息，提示系统错误信息

    def create_network(self):
        """
        创建网络函数
        """
        try:
            projects = self.request.get_projects()  # 获取项目列表
            networks = self.request.get_networks()  # 获取网络列表
            if self.lineEdit_add_networkname.text() == '':
                MessageBox().warn('警告', '网络名称不能为空')  # 提示网络名称不能为空
                return
            self.networkname = self.lineEdit_add_networkname.text()  # 获取网络名称
            for network in networks:
                if network['name'] == self.networkname:
                    MessageBox().warn('警告', '网络名称已存在')  # 提示网络名称已存在
                    return
            projectname = self.comboBox_add_networkproject.currentText()  # 获取项目名称
            for project in projects:
                if project['name'] == projectname:
                    self.network_projectid = project['id']  # 获取项目id
            self.networktype = self.comboBox_add_networktype.currentText()  # 获取网络类型
            self.zone = self.comboBox_add_networkzone.currentText()  # 获取网络区域

            self.networkdesc = self.lineEdit_add_networkdesc.text()  # 获取网络描述
            self.admin_state_up = self.checkBox_add_networkadmin.isChecked()  # 获取管理员状态
            self.shared = self.checkBox_add_networkshared.isChecked()  # 获取共享状态
            self.outnetwork = self.checkBox_add_networkout.isChecked()  # 获取外部访问状态
            self.ifsubnet = self.checkBox_add_networkifsubnet.isChecked()  # 获取是否添加子网状态
            if self.networktype in ['vlan', 'vxlan']:
                self.dialog_networktypevlan()  # 调用vlan或vxlan网络类型对话框
            elif self.networktype == 'local':
                res = self.request.add_network(self.networkname, self.admin_state_up, self.shared,
                                               self.network_projectid,
                                               self.networkdesc, self.networktype, self.outnetwork)  # 添加网络
                if res:
                    self.network_id = res['id']  # 获取网络id
                    if self.ifsubnet:
                        subnet_dialog = AddSubnet(self.network_id)  # 创建子网对话框
                        if not subnet_dialog.exec_():
                            self.parent.show_network_tree_thread()  # 显示网络树线程
                            self.close()  # 关闭窗口
            else:
                self.dialog_networktype()  # 调用网络类型对话框
        except Exception as e:
            MessageBox().warn('警告', f'系统错误：{e}')  # 提示系统错误
            return

    def dialog_networktype(self):
        """
        对话框用于设置网络类型
        """
        dialog = NetworkType(self)  # 创建网络类型对话框实例
        if not dialog.exec_():  # 如果对话框取消
            self.provider = dialog.provider  # 更新提供者
            res = self.request.add_network(self.networkname, self.admin_state_up, self.shared, self.network_projectid,self.networkdesc, self.networktype, self.outnetwork,
                                           self.provider)  # 添加网络
            if res:  # 如果添加成功
                self.network_id = res['id']  # 更新网络ID
                if self.ifsubnet:  # 如果需要添加子网
                    subnet_dialog = AddSubnet(self.network_id)  # 创建添加子网对话框实例
                    if not subnet_dialog.exec_():  # 如果对话框取消
                        self.parent.show_network_tree_thread()  # 显示网络树
                        self.close()  # 关闭当前窗口

    def dialog_networktypevlan(self):
        """
        VLAN网络类型对话框函数
        """
        dialog = NetworkTypeVlan(self)  # 创建VLAN网络类型对话框实例
        if not dialog.exec_():  # 如果对话框取消
            self.provider = dialog.provider  # 更新提供者
            self.vlan_id = dialog.vlan_id  # 更新VLAN ID
            res = self.request.add_network(self.networkname, self.admin_state_up, self.shared, self.network_projectid,self.networkdesc, self.networktype, self.outnetwork, self.provider, self.vlan_id)  # 添加网络
            if res:  # 如果添加成功
                self.network_id = res['id']  # 更新网络ID
                if self.ifsubnet:  # 如果需要添加子网
                    subnet_dialog = AddSubnet(self.network_id)  # 创建添加子网对话框实例
                    if not subnet_dialog.exec_():  # 如果对话框取消
                        self.parent.show_network_tree_thread()  # 显示网络树
                        self.close()  # 关闭当前窗口


class NetworkTypeVlan(QDialog, Ui_NetworkTypeVlan):
    def __init__(self, master: AddNetwork):
        super().__init__()
        self.master = master  # 创建一个AddNetwork类型的实例变量master，用于传递父类的引用
        self.provider = ''  # 创建一个空字符串类型的变量provider，用于存储提供者信息
        self.vlan_id = ''  # 创建一个空字符串类型的变量vlan_id，用于存储VLAN ID
        self.setupUi(self)  # 调用setupUi方法进行UI布局初始化
        self.request = Request()  # 创建一个Request类的实例变量request
        self.setWindowIcon(QIcon('logo.ico'))  # 设置窗口图标
        self.setWindowTitle('Vlan网络类型')  # 设置窗口标题
        self.label_addnetworktypetitle.setText('Vlan网络类型')  # 设置标签文本
        self.pushButton_add_addunetworktype.clicked.connect(self.add_networkvlan)  # 当按钮被点击时，调用add_networkvlan方法

    def add_networkvlan(self):
        """
        添加VLAN网络类型
        """
        try:
            provider = self.lineEdit_add_networktype.text()  # 获取提供者文本
            vlan_id = self.lineEdit_add_networkvlanid.text()  # 获取VLAN ID文本
            if vlan_id == '':  # 判断VLAN ID是否为空
                MessageBox().warn('警告', 'Vlan ID不能为空')  # 若为空，弹出警告消息框
                return  # 返回
            else:
                self.provider = provider  # 将提供者赋值给实例变量
                self.vlan_id = vlan_id  # 将VLAN ID赋值给实例变量
                self.close()  # 关闭对话框
        except Exception as e:  # 捕获异常
            MessageBox().warn('警告', f'系统错误：{e}')  # 弹出警告


class NetworkType(QDialog, Ui_NetworkType):
    def __init__(self, master: AddNetwork):
        super().__init__()
        self.setupUi(self)  # 初始化界面
        self.master = master  # 传入的参数
        self.provider = None  # 初始化变量
        self.request = Request()  # 初始化变量
        self.setWindowIcon(QIcon('logo.ico'))  # 设置窗口图标
        self.setWindowTitle(self.master.networktype)  # 设置窗口标题
        self.label_addnetworktypetitle.setText(f"{self.master.networktype}网络类型")  # 设置标签文本
        self.pushButton_add_addunetworktype.clicked.connect(self.add_networkprovider)  # 连接按钮点击事件方法

    def add_networkprovider(self):
        # 添加网络提供商
        try:
            # 检查输入的物理网络是否为空
            if self.lineEdit_add_networktype.text() == '':
                # 显示警告消息框
                MessageBox().warn('警告', '物理网络不能为空')
                return
            # 获取输入的网络提供商
            self.provider = self.lineEdit_add_networktype.text()
            # 关闭对话框
            self.close()
        except Exception as e:
            # 显示警告消息框，提示系统错误信息
            MessageBox().warn('警告', f'系统错误：{e}')


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 设置UI界面
        self.setWindowIcon(QIcon("logo.ico"))  # 设置窗口图标
        self.setWindowTitle("OpenStack")  # 设置窗口标题
        self.setFixedSize(1120, 800)  # 设置窗口固定大小
        self.session = Session()  # 创建会话对象
        self.action_OpenStack.triggered.connect(self.get_openstack_url)  # 连接OpenStack操作
        self.action_OpenStackDocs.triggered.connect(self.get_docs_openstack_url)  # 连接OpenStack文档操作
        self.action_CSDN.triggered.connect(self.get_csdn_url)  # 连接CSDN操作

        self.openstack = QStackedWidget()  # 创建堆叠式窗口部件
        self.Login = Login(self.openstack, self)  # 创建Login窗口部件
        self.openstack.addWidget(self.Login)  # 将Login窗口部件添加到堆叠式窗口部件中

        self.setCentralWidget(self.openstack)  # 设置中央窗口部件为堆叠式窗口部件

    def get_openstack_url(self):
        url = "https://www.openstack.org/"  # 定义OpenStack官网的URL链接
        webbrowser.open(url)  # 打开浏览器并访问URL链接

    def get_docs_openstack_url(self):
        url = "https://docs.openstack.org/zh_CN/"  # 定义OpenStack中文文档的URL链接
        webbrowser.open(url)  # 打开浏览器并访问URL链接

    def get_csdn_url(self):
        url = "https://blog.csdn.net/lj2023103338"  # 定义CSDN博客的URL链接
        webbrowser.open(url)  # 打开浏览器并访问URL链接

    def closeEvent(self, event):
        flag = MessageBox().quest('退出', '是否退出？')  # 弹出对话框询问是否退出
        if flag:  # 如果点击“确定”退出
            self.session.write({  # 写入会话数据
                "ip": "",
                "username": "",
                "password": "",
                "domain": "",
                "project": "",
                "token": "",
                "headers": ""
            })
            event.accept()  # 接受关闭事件
        else:  # 如果点击“取消”不退出
            event.ignore()  # 忽略关闭事件


if __name__ == "__main__":
    # 创建一个应用程序实例
    app = QApplication(sys.argv)
    # 添加一个字体到字体数据库
    QFontDatabase.addApplicationFont("resources/fonts/HarmonyOS_Sans_SC_Medium.ttf")
    # 创建一个主窗口
    window = MainWindow()
    # 显示主窗口
    window.show()
    # 运行应用程序的事件循环
    sys.exit(app.exec_())
```

### 2、线程类定义

```python
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QTreeWidgetItem
from utils.messagebox import MessageBox


class ShowUserTrees(QThread):
    signal = pyqtSignal(bool)  # 定义一个信号signal，用于传递信号

    def __init__(self, parent: QWidget):
        super().__init__()
        self.parent = parent  # 初始化父类指针

    def run(self):
        try:
            self.parent.tree_users.clear()  # 清空父类的tree_users
            users = self.parent.request.get_users()  # 调用父类的get_users方法获取用户信息
            domains = self.parent.request.get_domains()  # 调用父类的get_domains方法获取域信息
            projects = self.parent.request.get_projects()  # 调用父类的get_projects方法获取项目信息
            roots = {}  # 创建空字典roots，用于存储根节点
            children = {}  # 创建空字典children，用于存储子节点
            for i in range(len(users)):  # 遍历用户列表
                roots[i] = QTreeWidgetItem(self.parent.tree_users)  # 在tree_users中创建根节点
                roots[i].setText(0, str(i + 1))  # 设置根节点的第0列文本
                roots[i].setText(1, users[i]['name'])  # 设置根节点的第1列文本
                roots[i].setText(2, users[i]['id'])  # 设置根节点的第2列文本
                roots[i].setText(3, users[i]['links']['self'])  # 设置根节点的第3列文本
                for domain in domains:  # 遍历域列表
                    if domain['id'] == users[i]['domain_id']:  # 如果域的ID与用户的域ID相等
                        roots[i].setText(4, domain['name'])  # 设置根节点的第4列文本为域的名称
                        break  # 跳出循环
                roots[i].setText(5, users[i]['domain_id'])  # 设置根节点的第5列文本为用户的域ID
                try:
                    for project in projects:  # 遍历项目列表
                        if project['id'] == users[i]['default_project_id']:  # 如果项目的ID与用户的默认项目ID相等
                            roots[i].setText(6, project['name'])  # 设置根节点的第6列文本为项目的名称
                            break  # 跳出循环
                    roots[i].setText(7, users[i]['default_project_id'])  # 设置根节点的第7列文本为用户的默认项目ID
                except KeyError:
                    roots[i].setText(6, '无')  # 设置根节点的第6列文本为"无"
                    roots[i].setText(7, '无')  # 设置根节点的第7列文本为"无"
                children[i] = {}  # 创建空字典children[i]，用于存储用户的子节点
                children[i]["name"] = QTreeWidgetItem(roots[i])  # 在roots[i]中创建子节点"name"
                children[i]["name"].setText(0, "用户名：")  # 设置子节点"name"的第0列文本
                children[i]["name"].setText(1, users[i]['name'])  # 设置子节点"name"的第1列文本
                children[i]["id"] = QTreeWidgetItem(roots[i])  # 在roots[i]中创建子节点"id"
                children[i]["id"].setText(0, "用户ID：")  # 设置子节点"id"的第0列文本
                children[i]["id"].setText(1, users[i]['id'])  # 设置子节点"id"的第1列文本
                children[i]["links"] = QTreeWidgetItem(roots[i])  # 在roots[i]中创建子节点"links"
                children[i]["links"].setText(0, "用户链接：")  # 设置子节点"links"的第0列文本
                children[i]["links"].setText(1, users[i]['links']['self'])  # 设置子节点"links"的第1列文本
                children[i]["domain"] = QTreeWidgetItem(roots[i])  # 在roots[i]中创建子节点"domain"
                children[i]["domain"].setText(0, "域ID：")  # 设置子节点"domain"的第0列文本
                children[i]["domain"].setText(1, users[i]['domain_id'])  # 设置子节点"domain"的第1列文本
                children[i]["default_project"] = QTreeWidgetItem(roots[i])  # 在roots[i]中创建子节点"default_project"
                try:
                    children[i]["default_project"].setText(0, "项目ID：")  # 设置子节点"default_project"的第0列文本
                    children[i]["default_project"].setText(1, users[i][
                        'default_project_id'])  # 设置子节点"default_project"的第1列文本
                except KeyError:
                    children[i]["default_project"].setText(0, "项目：")  # 设置子节点"default_project"的第0列文本为"项目"
                    children[i]["default_project"].setText(1, '无')  # 设置子节点"default_project"的第1列文本为"无"
        except Exception as e:
            MessageBox().warn("错误", str(e))  # 弹出警告框提示错误信息

        self.signal.emit(True)  # 通过信号发送True值


class ShowNetworkTrees(QThread):
    """
    展示网络树的类

    参数:
        parent: QWidget, 父窗口对象
    """

    signal = pyqtSignal(bool)  # pyqtSignal类创建一个信号

    def __init__(self, parent: QWidget):
        """
        初始化方法

        参数:
            parent: QWidget, 父窗口对象
        """
        super().__init__()
        self.parent = parent

    def run(self):
        """
        运行方法，用于展示网络树
        """
        try:
            self.parent.tree_networks.clear()  # 清空树形视图
            networks = self.parent.request.get_networks()  # 获取网络列表
            subnets = self.parent.request.get_subnets()  # 获取子网列表
            roots = {}  # 创建字典roots，用于存储每个网络的根节点
            children = {}  # 创建字典children，用于存储每个网络的子节点
            for i in range(len(networks)):  # 遍历网络列表
                roots[i] = QTreeWidgetItem(self.parent.tree_networks)  # 在树形视图中创建一个节点
                roots[i].setText(0, str(i + 1))  # 设置节点的第0列文本
                roots[i].setText(1, networks[i]['name'])  # 设置节点的第1列文本
                ...
                children[i]["description"] = QTreeWidgetItem(roots[i])  # 在roots[i]节点下创建一个节点
                if networks[i]['description'] == 'None':
                    children[i]["description"].setText(0, "描述：")  # 设置节点的第0列文本
                    children[i]["description"].setText(1, "无")  # 设置节点的第1列文本
                else:
                    children[i]["description"].setText(0, "描述：")  # 设置节点的第0列文本
                    children[i]["description"].setText(1, networks[i]['description'])  # 设置节点的第1列文本
        except Exception as e:
            MessageBox().warn("错误", str(e))  # 弹出错误对话框，提示错误信息
        self.signal.emit(True)  # 发送信号，表示树形视图已更新


class ShowImageTrees(QThread):
    signal = pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def run(self):
        try:
            self.parent.tree_images.clear()  # 清空父类的tree_images列表
            images = self.parent.request.get_images()  # 获取父类request的images数据
            roots = {}  # 创建空字典roots，用于存储根节点信息
            children = {}  # 创建空字典children，用于存储子节点信息

            # 遍历images列表
            for i in range(len(images)):
                # 在roots字典中添加根节点
                roots[i] = QTreeWidgetItem(self.parent.tree_images)
                roots[i].setText(0, str(i + 1))  # 设置根节点的第一个文本
                roots[i].setText(1, images[i]['name'])  # 设置根节点的第二个文本
                roots[i].setText(2, images[i]['id'])  # 设置根节点的第三个文本
                roots[i].setText(3, f"{images[i]['size'] / 1024 / 1024 / 8:.2f}MB")  # 设置根节点的第四个文本
                roots[i].setText(4, images[i]['container_format'])  # 设置根节点的第五个文本
                roots[i].setText(5, images[i]['disk_format'])  # 设置根节点的第六个文本
                if images[i]['status'] == 'active':
                    roots[i].setText(6, "运行中")  # 设置根节点的第七个文本
                else:
                    roots[i].setText(6, "已停止")  # 设置根节点的第七个文本
                roots[i].setText(7, images[i]['created_at'])  # 设置根节点的第八个文本

                # 遍历images[i]字典中的键值对
                for k, v in images[i].items():
                    if k == 'id':
                        if v:  # 判断键值对的值是否存在
                            # 在roots[i]的子节点中添加键值对的键
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '镜像ID')  # 设置子节点的文本
                            children[i][k].setText(1, v)  # 设置子节点的文本
                        else:
                            pass
                    elif k == 'container_format':
                        if v:
                            # 在roots[i]的子节点中添加键值对的键
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '容器格式')  # 设置子节点的文本
                            children[i][k].setText(1, v)  # 设置子节点的文本
                        else:
                            pass
                    elif k == 'disk_format':
                        if v:
                            # 在roots[i]的子节点中添加键值对的键
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '镜像格式')  # 设置子节点的文本
                            children[i][k].setText(1, v)  # 设置子节点的文本
                        else:
                            pass
                    elif k == 'status':
                        if v == 'active':
                            # 在roots[i]的子节点中添加键值对的键
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '状态')  # 设置子节点的文本
                            children[i][k].setText(1, '运行中')  # 设置子节点的文本
                        else:
                            # 在roots[i]的子节点中添加键值对的键
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '状态')  # 设置子节点的文本
                            children[i][k].setText(1, '已停止')  # 设置子节点的文本
                    elif k == 'created_at':
                        if v:
                            # 在roots[i]的子节点中添加键值对的键
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '创建时间')  # 设置子节点的文本
                            children[i][k].setText(1, v)  # 设置子节点的文本
                        else:
                            pass
                    elif k == 'updated_at':
                        if v:
                            # 在roots[i]的子节点中添加键值对的键
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '更新时间')  # 设置子节点的文本
                            children[i][k].setText(1, v)  # 设置子节点的文本
                        else:
                            pass
                    elif k == 'name':
                        if v:
                            # 在roots[i]的子节点中添加键值对的键
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '名称')  # 设置子节点的文本
                            children[i][k].setText(1, v)  # 设置子节点的文本
                        else:
                            pass
                    elif k == 'size':
                        if v:
                            # 在roots[i]的子节点中添加键值对的键
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '大小')  # 设置子节点的文本
                            children[i][k].setText(1, f"{v / 1024 / 1024 / 8:.2f}MB")  # 设置子节点的文本
                        else:
                            pass
                    elif k == 'description':
                        if v:
                            # 在roots[i]的子节点中添加键值对的键
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '描述')  # 设置子节点的文本
                            children[i][k].setText(1, v)  # 设置子节点的文本
                        else:
                            pass
                    elif k == 'min_ram':
                        if v:
                            # 在roots[i]的子节点中添加键值对的键
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '最小内存')  # 设置子节点的文本
                            children[i][k].setText(1, str(v))  # 设置子节点的文本
                        else:
                            pass
                    elif k == 'min_disk':
                        if v:
                            # 在roots[i]的子节点中添加键值对的键
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '最小磁盘')  # 设置子节点的文本
                            children[i][k].setText(1, str(v))  # 设置子节点的文本
                        else:
                            pass
                    elif k == 'file':
                        if v:
                            # 在roots[i]的子节点中添加键值对的键
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '文件')  # 设置子节点的文本
                            children[i][k].setText(1, v)  # 设置子节点的文本
                        else:
                            pass
                    elif k == 'owner':
                        if v:
                            # 在roots[i]的子节点中添加键值对的键
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '所有者')  # 设置子节点的文本
                            children[i][k].setText(1, v)  # 设置子节点的文本
                        else:
                            pass
                    elif k == 'visibility':
                        if v:
                            # 在roots[i]的子节点中添加键值对的键
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '可见性')  # 设置子节点的文本
                            children[i][k].setText(1, v)  # 设置子节点的文本
                        else:
                            pass
                    elif k == 'protected':
                        # 在roots[i]的子节点中添加键值对的键
                        children[i][k] = QTreeWidgetItem(roots[i])
                        children[i][k].setText(0, '是否保护')  # 设置子节点的文本
                        if v:
                            children[i][k].setText(1, '受保护的')  # 设置子节点的文本
                        else:
                            children[i][k].setText(1, '未受保护的')  # 设置子节点的文本
                    elif k == 'tags':
                        if v:
                            # 在roots[i]的子节点中添加键值对的键
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '标签')  # 设置子节点的文本
                            children[i][k].setText(1, v)  # 设置子节点的文本
                        else:
                            pass
                    elif k == 'self':
                        if v:
                            # 在roots[i]的子节点中添加键值对的键
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, 'self')  # 设置子节点的文本
                            children[i][k].setText(1, v)  # 设置子节点的文本
                        else:
                            pass
                    elif k == 'schema':
                        if v:
                            # 在roots[i]的子节点中添加键值对的键
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, 'schema')  # 设置子节点的文本
                            children[i][k].setText(1, v)  # 设置子节点的文本
                        else:
                            pass
                    elif k == 'os_hash_algo':
                        if v:
                            # 在roots[i]的子节点中添加键值对的键
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, 'hash算法')  # 设置子节点的文本
                            children[i][k].setText(1, v)  # 设置子节点的文本
                        else:
                            pass
                    elif k == 'virtual_size':
                        if v:
                            # 在roots[i]的子节点中添加键值对的键
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '虚拟大小')  # 设置子节点的文本
                            children[i][k].setText(1, f"{v / 1024 / 1024 / 8:.2f}MB")  # 设置子节点的文本
                        else:
                            pass
                    elif k == 'checksum':
                        if v:
                            # 在roots[i]的子节点中添加键值对的键
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, 'checksum')  # 设置子节点的文本
                            children[i][k].setText(1, v)  # 设置子节点的文本
                        else:
                            pass
                    elif k == 'os_hash_value':
                        if v:
                            # 在roots[i]的子节点中添加键值对的键
                            children[i][k] = QTreeWidgetItem(roots[i])

                            children[i][k].setText(0, 'hash值')
                            children[i][k].setText(1, v)
                        else:
                            pass
                    elif k == 'os_hidden':
                        children[i][k] = QTreeWidgetItem(roots[i])
                        children[i][k].setText(0, '是否隐藏')
                        if v:
                            children[i][k].setText(1, '隐藏的')
                        else:
                            children[i][k].setText(1, '未隐藏的')

        except Exception as e:
            MessageBox().warn("警告", f"获取镜像列表失败！f{e}")

        self.signal.emit(True)


class ShowFlavorTrees(QThread):
    signal = pyqtSignal(bool)  # 定义一个信号signal，类型为bool

    def __init__(self, parent):
        super(ShowFlavorTrees, self).__init__()
        self.parent = parent  # 父对象

    def run(self):
        try:
            self.parent.tree_flavors.clear()  # 清空父对象的tree_flavors属性
            flavors = self.parent.request.get_flavors()  # 获取flavors数据
            roots = {}  # 初始化roots字典，用于存储树的根节点
            children = {}  # 初始化children字典，用于存储树的子节点
            for i in range(len(flavors)):
                roots[i] = QTreeWidgetItem(self.parent.tree_flavors)  # 在tree_flavors中添加根节点
                roots[i].setText(0, str(i + 1))  # 设置根节点的第1列文本
                roots[i].setText(1, flavors[i]['name'])  # 设置根节点的第2列文本
                roots[i].setText(2, flavors[i]['id'])  # 设置根节点的第3列文本
                roots[i].setText(3, str(flavors[i]['vcpus']))  # 设置根节点的第4列文本
                roots[i].setText(4, f"{flavors[i]['ram']}MB")  # 设置根节点的第5列文本
                roots[i].setText(5, f"{flavors[i]['disk']}GB")  # 设置根节点的第6列文本
                roots[i].setText(6, f"{flavors[i]['OS-FLV-EXT-DATA:ephemeral']}GB")  # 设置根节点的第7列文本
                if flavors[i]['swap']:  # 如果有swap
                    roots[i].setText(7, f"{flavors[i]['swap']}MB")  # 设置根节点的第8列文本
                else:
                    roots[i].setText(7, "0MB")  # 设置根节点的第8列文本为0MB
                roots[i].setText(8, f"{flavors[i]['rxtx_factor']}")  # 设置根节点的第9列文本
                children[i] = {}  # 初始化children字典的第i个键值对
                for key, value in flavors[i].items():  # 遍历flavors[i]中的键值对
                    if key == 'links':  # 如果键为'links'
                        children[i]['links'] = {}  # 初始化children[i]['links']字典
                        children[i]['links']['item'] = QTreeWidgetItem(roots[i])  # 在roots[i]中添加链接的子节点
                        children[i]['links']['item'].setText(0, '链接')  # 设置链接子节点的文本
                        children[i]['links']['info'] = {}  # 初始化children[i]['links']['info']字典
                        for link in value:  # 遍历链接
                            children[i]['links']['info'][link['rel']] = QTreeWidgetItem(
                                children[i]['links']['item'])  # 在链接子节点中添加信息的子节点
                            children[i]['links']['info'][link['rel']].setText(0, link['rel'])  # 设置信息子节点的文本
                            children[i]['links']['info'][link['rel']].setText(1, link['href'])  # 设置信息子节点的文本
                    elif key == 'ram':  # 如果键为'ram'
                        children[i]['ram'] = QTreeWidgetItem(roots[i])  # 在roots[i]中添加内存大小的子节点
                        children[i]['ram'].setText(0, '内存大小')  # 设置内存大小子节点的文本
                        children[i]['ram'].setText(1, str(value) + "MB")  # 设置内存大小子节点的文本
                    elif key == 'disk':  # 如果键为'disk'
                        children[i]['disk'] = QTreeWidgetItem(roots[i])  # 在roots[i]中添加磁盘大小的子节点
                        children[i]['disk'].setText(0, '磁盘大小')  # 设置磁盘大小子节点的文本
                        children[i]['disk'].setText(1, str(value) + "GB")  # 设置磁盘大小子节点的文本
                    elif key == 'OS-FLV-EXT-DATA:ephemeral':  # 如果键为'OS-FLV-EXT-DATA:ephemeral'
                        children[i]['ephemeral'] = QTreeWidgetItem(roots[i])  # 在roots[i]中添加临时磁盘大小的子节点
                        children[i]['ephemeral'].setText(0, '临时磁盘大小')  # 设置临时磁盘大小子节点的文本
                        children[i]['ephemeral'].setText(1, str(value) + "GB")  # 设置临时磁盘大小子节点的文本
                    elif key == 'swap':  # 如果键为'swap'
                        children[i]['swap'] = QTreeWidgetItem(roots[i])  # 在roots[i]中添加Swap磁盘大小的子节点
                        children[i]['swap'].setText(0, 'Swap磁盘大小')  # 设置Swap磁盘大小子节点的文本
                        if value:  # 如果有值
                            children[i]['swap'].setText(1, str(value) + "MB")  # 设置Swap磁盘大小子节点的文本
                        else:
                            children[i]['swap'].setText(1, "0MB")  # 设置Swap磁盘大小子节点的文本为0MB
                    elif key == 'rxtx_factor':  # 如果键为'rxtx_factor'
                        children[i]['rxtx_factor'] = QTreeWidgetItem(roots[i])  # 在roots[i]中添加RX/TX因子的子节点
                        children[i]['rxtx_factor'].setText(0, 'RX/TX因子')  # 设置RX/TX因子子节点的文本
                        children[i]['rxtx_factor'].setText(1, str(value))  # 设置RX/TX因子子节点的文本
                    elif key == 'OS-FLV-DISABLED:disabled':  # 如果键为'OS-FLV-DISABLED:disabled'
                        children[i]['disabled'] = QTreeWidgetItem(roots[i])  # 在roots[i]中添加是否禁用的子节点
                        children[i]['disabled'].setText(0, '是否禁用')  # 设置是否禁用子节点的文本
                        if value:  # 如果值为真
                            children[i]['disabled'].setText(1, '是')  # 设置是否禁用子节点的文本为'是'
                        else:
                            children[i]['disabled'].setText(1, '否')  # 设置是否禁用子节点的文本为'否'
                    elif key == 'os-flavor-access:is_public':  # 如果键为'os-flavor-access:is_public'
                        children[i]['is_public'] = QTreeWidgetItem(roots[i])  # 在roots[i]中添加是否公开的子节点
                        children[i]['is_public'].setText(0, '是否公开')  # 设置是否公开子节点的文本
                        if value:  # 如果值为真
                            children[i]['is_public'].setText(1, '是')  # 设置是否公开子节点的文本为'是'
                        else:
                            children[i]['is_public'].setText(1, '否')  # 设置是否公开子节点的文本为'否'
                    elif key == 'id':  # 如果键为'id'
                        children[i]['id'] = QTreeWidgetItem(roots[i])  # 在roots[i]中添加云主机类型ID的子节点
                        children[i]['id'].setText(0, '云主机类型ID')  # 设置云主机类型ID子节点的文本
                        children[i]['id'].setText(1, str(value))  # 设置云主机类型ID子节点的文本
                    elif key == 'name':  # 如果键为'name'
                        children[i]['name'] = QTreeWidgetItem(roots[i])  # 在roots[i]中添加云主机类型名称的子节点
                        children[i]['name'].setText(0, '云主机类型名称')  # 设置云主机类型名称子节点的文本
                        children[i]['name'].setText(1, str(value))  # 设置云主机类型名称子节点的文本
        except Exception as e:
            MessageBox().warn("警告", f"系统错误！{e}")  # 弹出警告框提示系统错误，并显示错误信息
        self.signal.emit(True)  # 发送信号指示完成


class ShowServerTrees(QThread):
    """
    展示云服务器树形结构的类

    参数:
        parent: 父窗口的实例

    属性:
        parent: 父窗口的实例

    方法:
        run(): 运行该线程，展示云服务器树形结构
    """
    signal = pyqtSignal(bool)

    def __init__(self, parent):
        super(ShowServerTrees, self).__init__()
        self.parent = parent

    def run(self):
        """
        运行该线程，展示云服务器树形结构的方法

        异常:
            Exception: 获取云主机列表失败时的异常
        """
        try:
            self.parent.tree_servers.clear()
            servers = self.parent.request.get_servers()
            flavors = self.parent.request.get_flavors()
            roots = {}
            children = {}

            for i in range(len(servers)):
                roots[i] = QTreeWidgetItem(self.parent.tree_servers)
                roots[i].setText(0, str(i + 1))
                roots[i].setText(1, servers[i]['name'])
                roots[i].setText(2, servers[i]['id'])

                if servers[i]['addresses']:
                    for net in servers[i]['addresses']:
                        for ip in servers[i]['addresses'][net]:
                            roots[i].setText(3, ip['addr'])

                for flavor in servers[i]['flavor']['id']:
                    for flavor_name in flavors:
                        if flavor_name['id'] == flavor:
                            roots[i].setText(4, flavor_name['name'])

                if servers[i]['status'] == 'ACTIVE':
                    roots[i].setText(5, '运行中')
                elif servers[i]['status'] == 'ERROR':
                    roots[i].setText(5, '错误')
                elif servers[i]['status'] == 'BUILD':
                    roots[i].setText(5, '正在创建')
                else:
                    roots[i].setText(5, '已关机')

                roots[i].setText(6, servers[i]['OS-EXT-AZ:availability_zone'])

                if servers[i]['key_name']:
                    roots[i].setText(7, servers[i]['key_name'])
                else:
                    roots[i].setText(7, '无')

                roots[i].setText(8, servers[i]['created'])

                children[i] = {}

                for k, v in servers[i].items():
                    if k == 'OS-EXT-STS:task_state':
                        if v:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '任务')
                            children[i][k].setText(1, v)
                        else:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '任务')
                            children[i][k].setText(1, '无')
                    elif k == 'addresses':
                        if v:
                            children[i][k] = {}
                            children[i][k]['item'] = QTreeWidgetItem(roots[i])
                            children[i][k]['item'].setText(0, '网络')
                            for net in v:
                                children[i][k][net] = QTreeWidgetItem(children[i][k]['item'])
                                children[i][k][net].setText(0, '网络名称')
                                children[i][k][net].setText(1, net)

                                for item in range(len(v[net])):
                                    children[i][k][item] = {}
                                    for o, m in v[net][item].items():
                                        if o == 'addr':
                                            if m:
                                                children[i][k][item][o] = QTreeWidgetItem(children[i][k][net])
                                                children[i][k][item][o].setText(0, 'IP地址')
                                                children[i][k][item][o].setText(1, m)
                                            else:
                                                children[i][k][item][o] = QTreeWidgetItem(children[i][k][net])
                                                children[i][k][item][o].setText(0, 'IP地址')
                                                children[i][k][item][o].setText(1, '无')
                                        elif o == 'OS-EXT-IPS:type':
                                            if m:
                                                children[i][k][item][o] = QTreeWidgetItem(children[i][k][net])
                                                children[i][k][item][o].setText(0, 'IP类型')
                                                children[i][k][item][o].setText(1, m)
                                            else:
                                                children[i][k][item][o] = QTreeWidgetItem(children[i][k][net])
                                                children[i][k][item][o].setText(0, 'IP类型')
                                                children[i][k][item][o].setText(1, '无')
                                        elif o == 'OS-EXT-IPS-MAC:mac_addr':
                                            if m:
                                                children[i][k][item][o] = QTreeWidgetItem(children[i][k][net])
                                                children[i][k][item][o].setText(0, 'MAC地址')
                                                children[i][k][item][o].setText(1, str(m))
                                            else:
                                                children[i][k][item][o] = QTreeWidgetItem(children[i][k][net])
                                                children[i][k][item][o].setText(0, 'MAC地址')
                                                children[i][k][item][o].setText(1, '无')
                                        elif o == 'version':
                                            if m:
                                                children[i][k][item][o] = QTreeWidgetItem(children[i][k][net])
                                                children[i][k][item][o].setText(0, '版本')
                                                children[i][k][item][o].setText(1, f"IPv{m}")
                                            else:
                                                children[i][k][item][o] = QTreeWidgetItem(children[i][k][net])
                                                children[i][k][item][o].setText(0, '版本')
                                                children[i][k][item][o].setText(1, '无')
                        else:
                            children[i][k] = {}
                            children[i][k]['item'] = QTreeWidgetItem(roots[i])
                            children[i][k]['item'].setText(0, '网络')
                            children[i][k]['item'].setText(1, '无')
                    elif k == 'links':
                        if v:
                            children[i][k] = {}
                            children[i][k]['item'] = QTreeWidgetItem(roots[i])
                            children[i][k]['item'].setText(0, '链接')
                            for item in range(len(v)):
                                children[i][k][item] = QTreeWidgetItem(children[i][k]['item'])
                                children[i][k][item].setText(0, v[item]['rel'])
                                children[i][k][item].setText(1, v[item]['href'])
                        else:
                            children[i][k] = {}
                            children[i][k]['item'] = QTreeWidgetItem(roots[i])
                            children[i][k]['item'].setText(0, '链接')
                            children[i][k]['item'].setText(1, '无')
                    elif k == 'OS-EXT-STS:vm_state':
                        if v == 'active':
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '状态')
                            children[i][k].setText(1, v)
                        else:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '状态')
                            children[i][k].setText(1, '无')
                    elif k == 'OS-EXT-SRV-ATTR:instance_name':
                        if v:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '实例名称')
                            children[i][k].setText(1, v)
                        else:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '实例名称')
                            children[i][k].setText(1, '无')

                    elif k == 'OS-SRV-USG:launched_at':
                        if v:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '启动时间')
                            children[i][k].setText(1, v)
                        else:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '启动时间')
                            children[i][k].setText(1, '无')
                    elif k == 'security_groups':
                        if v:
                            children[i][k] = {}
                            children[i][k]['item'] = QTreeWidgetItem(roots[i])
                            children[i][k]['item'].setText(0, '安全组')
                            for item in range(len(v)):
                                children[i][k][item] = QTreeWidgetItem(children[i][k]['item'])
                                children[i][k][item].setText(0, v[item]['name'])
                        else:
                            children[i][k] = {}
                            children[i][k]['item'] = QTreeWidgetItem(roots[i])
                            children[i][k]['item'].setText(0, '安全组')
                            children[i][k]['item'].setText(1, '无')

                    elif k == 'user_id':
                        if v:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '用户ID')
                            children[i][k].setText(1, v)
                        else:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '用户ID')
                            children[i][k].setText(1, '无')
                    elif k == 'OS-DCF:diskConfig':
                        if v:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '磁盘配置')
                            children[i][k].setText(1, v)
                        else:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '磁盘配置')
                            children[i][k].setText(1, '无')

                    elif k == 'OS-EXT-STS:power_state':
                        if v == 1:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '运行状态')
                            children[i][k].setText(1, '运行中')
                        elif v == 0:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '运行状态')
                            children[i][k].setText(1, '关机')
                        else:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '运行状态')
                            children[i][k].setText(1, '未知')
                    elif k == 'hostId':
                        if v:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '主机ID')
                            children[i][k].setText(1, v)
                        else:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '主机ID')
                            children[i][k].setText(1, '无')
                    elif k == 'OS-EXT-SRV-ATTR:hypervisor_hostname':
                        if v:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '主机名')
                            children[i][k].setText(1, v)
                        else:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '主机名')
                            children[i][k].setText(1, '无')
                    elif k == 'key_name':
                        if v:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '密钥')
                            children[i][k].setText(1, v)
                        else:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '密钥对')
                            children[i][k].setText(1, '无')
                    elif k == 'name':
                        if v:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '名称')
                            children[i][k].setText(1, v)
                        else:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '名称')
                            children[i][k].setText(1, '无')
                    elif k == 'created':

                        if v:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '创建时间')
                            children[i][k].setText(1, v)
                        else:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '创建时间')
                            children[i][k].setText(1, '无')
                    elif k == 'tenant_id':

                        if v:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '租户ID')
                            children[i][k].setText(1, v)
                        else:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '租户ID')
                            children[i][k].setText(1, '无')

                    elif k == 'os-extended-volumes:volumes_attached':
                        children[i][k] = {}
                        if v:
                            children[i][k]['item'] = QTreeWidgetItem(roots[i])
                            children[i][k]['item'].setText(0, '云硬盘')
                            for item in range(len(v)):
                                for o, m in v[item].items():
                                    if o == 'id':
                                        children[i][k][item] = QTreeWidgetItem(children[i][k]['item'])
                                        children[i][k][item].setText(0, '云硬盘ID')
                                        children[i][k][item].setText(1, m)
                        else:
                            children[i][k]['item'] = QTreeWidgetItem(roots[i])
                            children[i][k]['item'].setText(0, '云硬盘')
                            children[i][k]['item'].setText(1, '无')
                    elif k == 'memadata':

                        if v:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '元数据')
                            children[i][k].setText(1, str(v))
                        else:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '元数据')
                            children[i][k].setText(1, '无')

        except Exception as e:
            MessageBox().warn("警告", f"获取云主机列表失败！{e}")
        self.signal.emit(True)


class UploadImageFileThread(QThread):
    signal = pyqtSignal(bool)  # 定义一个信号，传递一个布尔类型的参数

    def __init__(self, parent):
        super().__init__()
        self.parent = parent  # 存储父类对象

    def run(self):
        """
        线程执行的方法，用于上传图片文件
        """
        self.parent.request.add_image(self.parent.imagename, self.parent.disk_format, self.parent.imagedesc,
                                      self.parent.min_disk, self.parent.min_ram,
                                      self.parent.visibility, self.parent.prtected, self.parent.file)
        self.signal.emit(True)  # 发送信号，传递True给主线程
```

### 3、消息弹窗类

```python
from PyQt5.QtWidgets import QMessageBox  # 导入QMessageBox类
from PyQt5.QtGui import QIcon, QFont  # 导入QIcon和QFont类


class MessageBox(QMessageBox):  # 定义一个MessageBox类，继承自QMessageBox类
    def __init__(self):  # 构造函数
        super().__init__()  # 调用父类的构造函数

    def main(self, title, text, ico):  # 定义一个main方法
        msgBox = QMessageBox()  # 创建QMessageBox对象
        msgBox.setWindowIcon(QIcon("logo.ico"))  # 设置窗口图标
        msgBox.setIconPixmap(QIcon(f"resources/ico/{ico}").pixmap(64, 64))  # 设置图标
        msgBox.setText(text)  # 设置文本内容
        msgBox.setWindowTitle(title)  # 设置窗口标题
        msgBox.setFont(QFont("HarmonyOS Sans SC", 10))  # 设置字体
        okButton = msgBox.addButton("确定", QMessageBox.AcceptRole)  # 添加确定按钮
        cancelButton = msgBox.addButton("取消", QMessageBox.RejectRole)  # 添加取消按钮
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
                                        }""")  # 设置确定按钮的样式
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
                                            }""")  # 设置取消按钮的样式
        msgBox.setStyleSheet("QMessageBox {background-color: #FFFFFF; color: #000000;}")  # 设置消息框的样式
        msgBox.exec_()  # 显示消息框并等待用户操作
        if msgBox.clickedButton() == okButton:  # 如果用户点击的是确定按钮
            return True  # 返回True
        elif msgBox.clickedButton() == cancelButton:  # 如果用户点击的是取消按钮
            return False  # 返回False

    def info(self, title, text):  # 定义一个info方法
        ico = "info.ico"  # 设置图标为info.ico
        res = self.main(title, text, ico)  # 调用main方法
        return res  # 返回结果

    def warn(self, title, text):  # 定义一个warn方法
        ico = "warn.ico"  # 设置图标为warn.ico
        res = self.main(title, text, ico)  # 调用main方法
        return res  # 返回结果

    def quest(self, title, text):  # 定义一个quest方法
        ico = "question.ico"  # 设置图标为question.ico
        res = self.main(title, text, ico)  # 调用main方法
        return res  # 返回结果
```

### 4、API调用类以及文件操作类

```python
import requests
import json
from pathlib import Path
from .threads import *
from .messagebox import *


class Session(object):
    def __init__(self):
        # 初始化会话对象
        # 获取当前文件所在目录的路径
        self.session_path = Path(__file__).parent / "session.json"

    def read(self):
        try:
            # 尝试读取会话文件
            # 如果文件存在，使用utf-8编码打开文件并加载为json格式数据
            with open(self.session_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # 如果文件不存在，则创建一个新的会话数据
            # 使用utf-8编码打开文件，并以json格式存储数据
            # 返回存储的数据
            with open(self.session_path, 'w', encoding='utf-8') as f:
                data = {
                    "ip": "",
                    "username": "",
                    "password": "",
                    "domain": "",
                    "token": "",
                    "headers": ""
                }
                json.dump(data, f, indent=2, ensure_ascii=False)
                return data

    def write(self, data):
        # 将数据写入会话文件
        # 使用utf-8编码打开文件，并以json格式存储数据
        with open(self.session_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


session = Session()


class Openstack(object):
    def __init__(self, ip, username, password, project_name, domain_name):
        # Openstack类用于操作Openstack资源的类
        # 初始化函数，用于设置Openstack资源的参数
        self.ip = ip  # Openstack服务器的IP地址
        self.username = username  # 登录Openstack服务器的用户名
        self.password = password  # 登录Openstack服务器的密码
        self.project_name = project_name  # Openstack项目名称
        self.domain_name = domain_name  # Openstack域名

        # 认证地址
        self.auth_url = f"http://{self.ip}:5000/v3/auth/tokens"
        # 认证信息
        self.auth_data = {
            'auth': {
                'identity': {
                    'methods': ['password'],
                    'password': {
                        'user': {
                            'name': f'{self.username}',
                            'domain': {
                                'name': f'{self.domain_name}'
                            },
                            'password': f'{self.password}'
                        }
                    }
                },
                'scope': {
                    'project': {
                        'domain': {
                            'name': f'{self.domain_name}'
                        },
                        'name': f'{self.project_name}'
                    }
                }
            }
        }

        self.headers = {'Content-Type': 'application/json'}  # 告诉服务器请求主体为json格式的数据

    def get_token(self):
        """
        获取令牌
        """
        token = requests.post(self.auth_url, headers=self.headers, json=self.auth_data).headers['X-Subject-Token']
        return token

    def login(self):
        """
        登录函数
        """
        try:
            token = self.get_token()
            self.headers['X-Auth-Token'] = token
            Session().write(
                {"ip": self.ip, "username": self.username, "password": self.password, "domain": self.domain_name,
                 "project": self.project_name, "token": token, "headers": self.headers})
            return True, token
        except Exception as e:
            return False, e


class Request:
    def __init__(self):
        # 会话对象，读取之前保存的会话信息
        self.session = Session().read()
        # 获取IP地址
        self.ip = self.session['ip']
        # 获取请求头信息
        self.headers = self.session['headers']
        # 认证地址
        self.auth_url = f"http://{self.ip}:5000/v3/auth/tokens"
        # 用户创建地址
        self.user_url = f"http://{self.ip}:5000/v3/users"
        # 创建网络的url
        self.network_url = f"http://{self.ip}:9696/v2.0/networks"
        # 创建子网的url
        self.subnet_url = f"http://{self.ip}:9696/v2.0/subnets"
        # 创建域名的url
        self.domain_url = f"http://{self.ip}:5000/v3/domains"
        # 创建项目的url
        self.project_url = f"http://{self.ip}:5000/v3/projects"
        # 获取镜像的url
        self.image_url = f"http://{self.ip}:9292/v2/images"
        # 获取镜像类型的url
        self.flavor_url = f"http://{self.ip}:8774/v2/flavors"
        # 获取服务器的url
        self.server_url = f"http://{self.ip}:8774/v2/servers"

    def get_users(self):
        # 获取用户列表
        users = requests.get(self.user_url, headers=self.headers).json()['users']
        return users

    def get_domains(self):
        # 获取域名列表
        domains = requests.get(self.domain_url, headers=self.headers).json()['domains']
        return domains

    def get_projects(self):
        # 获取项目列表
        projects = requests.get(self.project_url, headers=self.headers).json()['projects']
        return projects

    def get_networks(self):
        # 获取网络列表
        networks = requests.get(self.network_url, headers=self.headers).json()['networks']
        return networks

    def get_subnets(self):
        """
        获取子网信息

        Returns:
            list: 子网列表
        """
        subnets = requests.get(self.subnet_url, headers=self.headers).json()['subnets']
        return subnets

    def get_images(self):
        """
        获取镜像信息

        Returns:
            list: 镜像列表
        """
        images = requests.get(self.image_url, headers=self.headers).json()['images']
        return images

    def get_flavors(self):
        """
        获取规格信息

        Returns:
            list: 规格列表
        """
        flavors = requests.get(self.flavor_url, headers=self.headers).json()['flavors']
        n_flavors = []
        for flavor in flavors:
            n_flavors.append(requests.get(f"{self.flavor_url}/{flavor['id']}", headers=self.headers).json()['flavor'])
        return n_flavors

    def get_servers(self):
        """
        获取服务器信息

        Returns:
            list: 服务器列表
        """
        servers = requests.get(self.server_url, headers=self.headers).json()['servers']
        n_servers = []
        for server in servers:
            n_servers.append(requests.get(f"{self.server_url}/{server['id']}", headers=self.headers).json()['server'])
        return n_servers

    def delete_user(self, user_id):
        """
        删除用户
        :param user_id: 用户ID
        :return: 删除成功返回True，否则返回False
        """
        try:
            requests.delete(f"{self.user_url}/{user_id}", headers=self.headers)
            return True
        except Exception as e:
            MessageBox().warn('警告', f'用户删除失败，错误信息：{e}')
            return False

    def delete_network(self, network_id):
        """
        删除网络
        :param network_id: 网络ID
        :return: 删除成功返回True，否则返回False
        """
        try:
            requests.delete(f"{self.network_url}/{network_id}", headers=self.headers)
            return True
        except Exception as e:
            MessageBox().warn('警告', f'网络删除失败，错误信息：{e}')
            return False

    def delete_image(self, image_id):
        """
        删除镜像
        :param image_id: 镜像ID
        :return: 删除成功返回True，否则返回False
        """
        try:
            requests.delete(f"{self.image_url}/{image_id}", headers=self.headers)
            return True
        except Exception as e:
            MessageBox().warn('警告', f'镜像删除失败，错误信息：{e}')
            return False

    def delete_flavor(self, flavor_id):
        """
        删除镜像类型
        :param flavor_id: 镜像类型ID
        :return: 删除成功返回True，否则返回False
        """
        try:
            requests.delete(f"{self.flavor_url}/{flavor_id}", headers=self.headers)
            return True
        except Exception as e:
            MessageBox().warn('警告', f'镜像删除失败，错误信息：{e}')
            return False

    def delete_server(self, server_id):
        """
        删除服务器
        :param server_id: 服务器ID
        :return: 删除成功返回True，否则返回False
        """
        try:
            requests.delete(f"{self.server_url}/{server_id}", headers=self.headers)
            return True
        except Exception as e:
            MessageBox().warn('警告', f'服务器删除失败，错误信息：{e}')
            return False

    def add_user(self, username, password, domain_id, project_id, desc):
        """
        添加用户

        Args:
            username (str): 用户名
            password (str): 密码
            domain_id (str): 区域 ID
            project_id (str): 项目 ID
            desc (str): 描述

        Returns:
            dict: 添加成功返回用户信息，添加失败返回 False
        """
        users = self.get_users()
        for user in users:
            if user['name'] == username:
                flag = MessageBox().warn("警告", f"用户{username}已存在，是否删除？")
                if flag:
                    requests.delete(f"{self.user_url}/{user['id']}", headers=self.headers)
                else:
                    return
        user_data = {
            "user": {
                "name": f"{username}",
                "password": f"{password}",
                "domain_id": f"{domain_id}",
                "default_project_id": f"{project_id}",
                "description": f"{desc}"
            }
        }
        try:
            res = requests.post(self.user_url, headers=self.headers, json=user_data).json()
            try:
                r = res['user']
                return r
            except Exception as e:
                MessageBox().warn('警告', f'用户添加失败，错误信息：{e}')
                return False
        except Exception as e:
            MessageBox().warn('警告', f'用户添加失败，错误信息：{e}')
            return False

    def add_network(self, name, admin_state_up, shared, network_projectid, networkdesc, network_type, external,
                    provider='', vlan_id=1):
        """
        添加网络

        Args:
            name (str): 网络名称
            admin_state_up (bool): 网络是否启用
            shared (bool): 网络是否共享
            network_projectid (str): 项目 ID
            networkdesc (str): 描述
            network_type (str): 网络类型
            external (bool): 是否为外部网络
            provider (str): 提供商信息
            vlan_id (int): VLAN ID

        Returns:
            dict: 添加成功返回网络信息，添加失败返回 False
        """
        try:
            network_data = {
                "network": {
                    "name": name,
                    "admin_state_up": admin_state_up,
                    "shared": shared,
                    "project_id": network_projectid,
                    "description": networkdesc,
                    "provider:network_type": network_type,
                    "router:external": external,
                    "provider:physical_network": provider
                }
            }
            if network_type == 'vlan':
                network_data['network']['provider:segmentation_id'] = vlan_id
            res = requests.post(self.network_url, headers=self.headers, json=network_data).json()
            try:
                r = res['network']
                return r
            except Exception as e:
                for k, v in res.items():
                    MessageBox().warn('警告', f'网络添加失败，错误信息：{k}: {v["message"]}')
                return False
        except Exception as e:
            MessageBox().warn('警告', f'网络添加失败，错误信息：{e}')
            return False

    def add_subnet(self, subnet_name, network_id, ip_version, cidr, dhcp, gateway_ip, ip_pools: list, dns_nameservers,
                   hosts_routes: list):
        """
        添加子网

        Args:
            subnet_name (str): 子网名称
            network_id (str): 网络 ID
            ip_version (int): IP 版本
            cidr (str): CIDR
            dhcp (bool): 是否开启 DHCP
            gateway_ip (str): 网关 IP
            ip_pools (list): IP 池
            dns_nameservers (list): DNS 服务器
            hosts_routes (list): 主机路由

        Returns:
            dict: 添加成功返回子网信息，添加失败返回 False
        """
        try:
            subnet_data = {
                'subnet': {
                    'name': subnet_name,
                    'network_id': network_id,
                    'ip_version': ip_version,
                    'cidr': cidr,
                    'enable_dhcp': dhcp,
                    'gateway_ip': gateway_ip,
                    'allocation_pools': ip_pools,
                    'dns_nameservers': dns_nameservers,
                    'host_routes': hosts_routes
                }
            }
            res = requests.post(self.subnet_url, headers=self.headers, json=subnet_data).json()
            try:
                r = res['subnet']
                return r
            except Exception as e:
                for k, v in res.items():
                    MessageBox().warn('警告', f'子网添加失败，错误信息：{k}: {v["message"]}')
                return False
        except Exception as e:
            MessageBox().warn('警告', f'子网添加失败，错误信息：{e}')

    def add_image(self, name, disk_format='qcow2', desc='', min_disk='', min_ram='', visibility='shared',
                  protected=False, file=None):
        """
        添加镜像

        Args:
            name (str): 镜像名称
            disk_format (str): 镜像磁盘格式，默认为 'qcow2'
            desc (str): 描述
            min_disk (str): 最小磁盘大小
            min_ram (str): 最小内存大小
            visibility (str): 可见性，默认为 'shared'
            protected (bool): 是否受保护，默认为 False
            file (str): 镜像文件路径

        Returns:
            bool: 添加成功返回 True，添加失败返回 False
        """
        container_format = 'bare'
        image_data = {
            "name": name,
            "disk_format": disk_format,
            "description": desc,
            "visibility": visibility,
            "protected": protected,
            "container_format": container_format
        }
        if min_disk:
            image_data['min_disk'] = int(min_disk)
        if min_ram:
            image_data['min_ram'] = int(min_ram)
        if file:
            try:
                res = requests.post(self.image_url, headers=self.headers, json=image_data).json()
                try:
                    self.headers['Content-Type'] = 'application/octet-stream'
                    requests.put(f"{self.image_url}/{res['id']}/file", headers=self.headers,
                                 data=open(file, 'rb'))
                    self.headers['Content-Type'] = 'application/json'
                    return True
                except Exception as e:
                    for k, v in res.items():
                        MessageBox().warn('警告', f'镜像添加失败，错误信息：{k}: {v["message"]}')
                    return False
            except Exception as e:
                MessageBox().warn('警告', f'镜像添加失败，错误信息：{e}')

    def add_flavor(self, name, ram, vcpus, disk, ephemeral, swap, rxtx, id=''):
        """
        添加镜像

        Args:
            name (str): 镜像名称
            ram (int): 内存大小
            vcpus (int): CPU 核心数
            disk (int): 磁盘大小
            ephemeral (int): 临时磁盘大小
            swap (int): 交换区大小
            rxtx (int): 网络带宽
            id (str): 云盘 ID

        Returns:
            dict: 添加成功返回镜像信息，添加失败返回 False
        """
        flavor_data = {
            "flavor": {
                "name": name,
                "ram": ram,
                "vcpus": vcpus,
                "disk": disk,
                "OS-FLV-EXT-DATA:ephemeral": ephemeral,
                "swap": swap,
                "rxtx_factor": rxtx,
                "id": id
            }
        }
        try:
            res = requests.post(self.flavor_url, headers=self.headers, json=flavor_data).json()
            try:
                r = res['flavor']
                return r
            except Exception as e:
                for k, v in res.items():
                    MessageBox().warn('警告', f'镜像添加失败，错误信息：{k}: {v["message"]}')
                return False
        except Exception as e:
            MessageBox().warn('警告', f'镜像添加失败，错误信息：{e}')

    def add_server(self, name, image_id, flavor_id, network_id, zone):
        """
        添加镜像

        Args:
            name (str): 镜像名称
            image_id (str): 镜像 ID
            flavor_id (str): 镜像 ID
            network_id (str): 网络 ID
            zone (str): 可用区

        Returns:
            dict: 添加成功返回镜像信息，添加失败返回 False
        """
        try:
            server_data = {
                "server": {
                    "name": name,
                    "imageRef": image_id,
                    "flavorRef": flavor_id,
                    "networks": [
                        {
                            "uuid": network_id
                        }
                    ],
                    "availability_zone": zone
                }
            }
            res = requests.post(self.server_url, headers=self.headers, json=server_data).json()
            try:
                r = res['server']
                return r
            except Exception as e:
                for k, v in res.items():
                    MessageBox().warn('警告', f'镜像添加失败，错误信息：{k}: {v["message"]}')
                return False
        except Exception as e:
            MessageBox().warn('警告', f'镜像添加失败，错误信息：{e}')
```

## 六、UI代码

ui代码在ui目录下，是用QtDesigner写的，所以就不进行解析了。
