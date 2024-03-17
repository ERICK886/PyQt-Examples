import sys
import webbrowser
from utils import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ui import *


class Login(QWidget, Ui_Login):
    def __init__(self, openstack: QStackedWidget, parent):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.openstack = openstack
        self.reader = Session()
        self.pushButton_link.clicked.connect(self.login)
        self.pushButton_exit.clicked.connect(self.parent.close)

    def login(self):
        # 获取输入的IP地址、用户名、密码、用户域、用户项目
        ip = self.lineEdit_ip.text()
        username = self.lineEdit_username.text()
        password = self.lineEdit_password.text()
        domain = self.lineEdit_userdomain.text()
        project = self.lineEdit_userproject.text()
        # 如果用户名和密码都存在
        if username and password:
            # 创建Openstack连接
            conn = Openstack(ip, username, password, project, domain)
            # 登录并获取状态和令牌
            status, token = conn.login()
            # 如果登录成功
            if status:
                try:
                    # 设置窗口标题为"OpenStack - IP地址"
                    self.parent.setWindowTitle("OpenStack - " + ip)
                    # 创建Index对象
                    self.Index = Index(self.openstack)
                    # 将Index对象添加到openstack的widget列表中
                    self.openstack.addWidget(self.Index)
                    # 设置openstack的当前索引为1
                    self.openstack.setCurrentIndex(1)
                except Exception as e:
                    # 弹出警告框，显示"登录失败！f{e}"
                    MessageBox().warn("警告", f"登录失败！f{e}")
            else:
                # 弹出警告框，显示"登录失败！{token}"
                MessageBox().warn("警告", f"登录失败！{token}")
        else:
            # 弹出警告框，显示"用户名和密码不能为空！"
            MessageBox().warn("警告", "用户名和密码不能为空！")


class Index(QWidget, Ui_Index):
    def __init__(self, openstack):
        super().__init__()
        self.setupUi(self)
        self.reader = Session()
        self.request = Request()
        self.openstack = openstack
        self.adduserdialog = None
        self.label_logo.setPixmap(QPixmap("resources/img/logo.png").scaled(200, 100, Qt.KeepAspectRatio))
        data = self.reader.read()
        self.label_link.setText(f"""连接IP: {data['ip']}\n用户名: {data['username']}\n域: {data['domain']}""")
        self.pushButton_user.clicked.connect(self.user)
        self.pushButton_network.clicked.connect(self.network)
        self.pushButton_image.clicked.connect(self.image)
        self.pushButton_server.clicked.connect(self.server)
        self.pushButton_flavor.clicked.connect(self.flavor)
        self.pushButton_api.clicked.connect(self.api)
        self.tree_users.setColumnWidth(0, 160)
        self.tree_users.setColumnWidth(1, 600)
        self.tree_users.setColumnWidth(2, 400)
        self.tree_users.setColumnWidth(3, 600)
        self.tree_users.setColumnWidth(4, 160)
        self.tree_users.setColumnWidth(5, 300)
        self.tree_users.setColumnWidth(6, 160)
        self.tree_users.setColumnWidth(7, 400)

        self.tree_networks.setColumnWidth(0, 260)
        self.tree_networks.setColumnWidth(1, 400)
        self.tree_networks.setColumnWidth(2, 400)
        self.tree_networks.setColumnWidth(3, 400)
        self.tree_networks.setColumnWidth(4, 160)
        self.tree_networks.setColumnWidth(5, 160)
        self.tree_networks.setColumnWidth(6, 160)
        self.tree_networks.setColumnWidth(7, 300)

        self.tree_images.setColumnWidth(0, 160)
        self.tree_images.setColumnWidth(1, 500)
        self.tree_images.setColumnWidth(2, 400)
        self.tree_images.setColumnWidth(3, 160)
        self.tree_images.setColumnWidth(4, 160)
        self.tree_images.setColumnWidth(5, 160)
        self.tree_images.setColumnWidth(6, 160)
        self.tree_images.setColumnWidth(7, 200)

        self.tree_flavors.setColumnWidth(0, 180)
        self.tree_flavors.setColumnWidth(1, 400)

        self.tree_servers.setColumnWidth(0, 160)
        self.tree_servers.setColumnWidth(1, 500)
        self.tree_servers.setColumnWidth(2, 500)
        self.tree_servers.setColumnWidth(3, 160)
        self.tree_servers.setColumnWidth(8, 160)

        self.tableWidget.setColumnWidth(0, 250)
        self.tableWidget.setColumnWidth(1, 670)

        self.show_user_tree_thread()
        self.show_network_tree_thread()
        self.show_image_tree_thread()
        self.show_flavor_tree_thread()
        self.show_server_tree_thread()
        self.pushButton_deluser.clicked.connect(self.user_del)
        self.push_addneuser_time = QDateTime.currentDateTime()
        self.pushButton_adduser.clicked.connect(self.user_add)
        self.pushButton_addsubnet.clicked.connect(self.subnet_add)
        self.pushButton_delnetwork.clicked.connect(self.network_del)
        self.push_addnetwork_time = QDateTime.currentDateTime()
        self.pushButton_addnetwork.clicked.connect(self.network_add)
        self.pushButton_addimage.clicked.connect(self.image_add)
        self.pushButton_delimage.clicked.connect(self.image_del)
        self.pushButton_addflavors.clicked.connect(self.flavor_add)
        self.pushButton_delflavors.clicked.connect(self.flavor_del)
        self.pushButton_addservers.clicked.connect(self.server_add)
        self.pushButton_delservers.clicked.connect(self.server_del)
        self.pushButton_refresh.clicked.connect(self.refresh)
        self.push_refresh_time = QDateTime.currentDateTime()

    def refresh(self):
        current_time = QDateTime.currentDateTime()
        if self.push_refresh_time.secsTo(current_time) > 5:
            self.push_refresh_time = current_time
            self.show_server_tree_thread()
        else:
            MessageBox().warn("警告", "刷新间隔不能小于5秒！")

    def show_user_tree_thread(self):
        self.userthread = ShowUserTrees(self)
        self.userthread.start()

        def finished(flag):
            if flag:
                self.userthread.quit()
                self.userthread = None

        self.userthread.signal.connect(finished)

    def show_network_tree_thread(self):
        self.nethread = ShowNetworkTrees(self)
        self.nethread.start()

        def finished(flag):
            if flag:
                self.nethread.quit()
                self.nethread = None

        self.nethread.signal.connect(finished)

    def show_image_tree_thread(self):
        self.imgthread = ShowImageTrees(self)
        self.imgthread.start()

        def finished(flag):
            if flag:
                self.imgthread.quit()
                self.imgthread = None

        self.imgthread.signal.connect(finished)

    def show_flavor_tree_thread(self):
        self.flathread = ShowFlavorTrees(self)
        self.flathread.start()

        def finished(flag):
            if flag:
                self.flathread.quit()
                self.flathread = None

        self.flathread.signal.connect(finished)

    def show_server_tree_thread(self):
        self.serthread = ShowServerTrees(self)
        self.serthread.start()
        self.pushButton_refresh.setDisabled(True)

        def finished(flag):
            if flag:
                self.pushButton_refresh.setEnabled(True)
                self.serthread.quit()
                self.serthread = None

        self.serthread.signal.connect(finished)

    def server_add(self):
        dialog = AddServer(self)
        dialog.exec_()

    def server_del(self):
        item = self.tree_servers.currentItem()
        if item:
            if item.text(0).isdigit():
                flag = MessageBox().quest("提示", "确定删除该云主机吗？")
                if flag:
                    try:
                        server_id = item.text(2)
                        res = self.request.delete_server(server_id)
                        if res:
                            self.show_server_tree_thread()
                            MessageBox().info("提示", "云主机删除成功！")
                    except Exception as e:
                        MessageBox().warn("警告", f"云主机删除失败！{e}")

    def flavor_add(self):
        dialog = AddFlavor(self)
        dialog.exec_()

    def flavor_del(self):
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
        item = self.tree_images.currentItem()
        if item:
            if item.text(0).isdigit():
                flag = MessageBox().quest("提示", "确定删除该镜像吗？")
                if flag:
                    try:
                        image_id = item.text(2)
                        res = self.request.delete_image(image_id)
                        if res:
                            self.show_image_tree_thread()
                            MessageBox().info("提示", "镜像删除成功！")
                        else:
                            MessageBox().warn("警告", "镜像删除失败！")
                    except Exception as e:
                        MessageBox().warn("警告", f"镜像删除失败！{e}")

    def network_del(self):
        item = self.tree_networks.currentItem()
        if item:
            if item.text(0).isdigit():
                flag = MessageBox().quest("提示", "确定删除该网络吗？")
                if flag:
                    try:
                        network_id = item.text(2)
                        res = self.request.delete_network(network_id)
                        if res:
                            self.show_network_tree_thread()
                            MessageBox().info("提示", "网络删除成功！")
                        else:
                            MessageBox().warn("警告", "网络删除失败！")
                    except Exception as e:
                        MessageBox().warn("警告", f"网络删除失败！{e}")

    def subnet_add(self):
        item = self.tree_networks.currentItem()
        if item:
            if item.text(0).isdigit():
                network_id = item.text(2)
                try:
                    dialog = AddSubnet(network_id)
                    if not dialog.exec():
                        self.show_network_tree_thread()
                        return
                except Exception as e:
                    MessageBox().warn("警告", f"添加子网失败！{e}")

    def user_del(self):
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
        current_time = QDateTime.currentDateTime()
        if self.push_addneuser_time.secsTo(current_time) < 4:
            MessageBox().warn('警告', '请勿频繁添加用户')
            return
        self.adduserdialog = None
        self.adduserdialog = AddUser(self)
        self.adduserdialog.show()
        self.push_addneuser_time = QDateTime.currentDateTime()

    def network_add(self):
        current_time = QDateTime.currentDateTime()
        if self.push_addnetwork_time.secsTo(current_time) < 4:
            MessageBox().warn('警告', '请勿频繁添加网络')
            return
        self.addnetworkdialog = None
        self.addnetworkdialog = AddNetwork(self)
        self.addnetworkdialog.show()
        self.push_addnetwork_time = QDateTime.currentDateTime()

    def api(self):
        self.stackedWidget.setCurrentIndex(0)

    def user(self):
        self.stackedWidget.setCurrentIndex(1)

    def network(self):
        self.stackedWidget.setCurrentIndex(2)

    def image(self):
        self.stackedWidget.setCurrentIndex(3)

    def server(self):
        self.stackedWidget.setCurrentIndex(4)

    def flavor(self):
        self.stackedWidget.setCurrentIndex(5)


class AddServer(QDialog, Ui_AddServer):
    def __init__(self, parent: Index):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('logo.ico'))
        self.setWindowTitle('添加云主机')
        self.parent = parent
        self.request = Request()
        self.server_name = ''
        self.image_id = ''
        self.flavor_id = ''
        self.network_id = ''
        self.show_add_server()
        self.zone_view = QListView()
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
        self.comboBox_add_serverzone.setView(self.zone_view)

        self.image_view = QListView()
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
        self.comboBox_add_serverimage.setView(self.image_view)

        self.flavor_view = QListView()
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
        self.comboBox_add_serverflavor.setView(self.flavor_view)
        self.network_view = QListView()
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
        self.comboBox_add_servernetwork.setView(self.network_view)
        self.comboBox_add_serverzone.addItem('nova')
        self.pushButton_add_addserver.clicked.connect(self.add_server)

    def show_add_server(self):
        try:
            images = self.request.get_images()
            flavors = self.request.get_flavors()
            networks = self.request.get_networks()
            if images and flavors and networks:
                for image in images:
                    self.comboBox_add_serverimage.addItem(image['name'])
                for flavor in flavors:
                    self.comboBox_add_serverflavor.addItem(flavor['name'])
                self.comboBoxList = []
            for network in networks:
                self.comboBox_add_servernetwork.addItem(network['name'])
        except Exception as e:
            MessageBox().warn('警告', f'系统错误：{e}')

    def add_server(self):
        try:
            self.server_name = self.lineEdit_add_servername.text()
            if self.server_name == '':
                MessageBox().warn('警告', '请输入云主机名称')
                return
            for image in self.request.get_images():
                if image['name'] == self.comboBox_add_serverimage.currentText():
                    self.image_id = image['id']
                    break
            for flavor in self.request.get_flavors():
                if flavor['name'] == self.comboBox_add_serverflavor.currentText():
                    self.flavor_id = flavor['id']
                    break
            for network in self.request.get_networks():
                if network['name'] == self.comboBox_add_servernetwork.currentText():
                    self.network_id = network['id']
                    break
            self.zone = self.comboBox_add_serverzone.currentText()
            res = self.request.add_server(self.server_name, self.image_id, self.flavor_id, self.network_id, self.zone)
            if res:
                MessageBox().info('提示', '添加云主机成功')
                self.parent.show_server_tree_thread()
                self.close()
        except Exception as e:
            MessageBox().warn('警告', f'系统错误：{e}')


class AddFlavor(QDialog, Ui_AddFlavor):
    def __init__(self, parent: Index):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('logo.ico'))
        self.setWindowTitle('添加云主机类型')
        self.parent = parent
        self.request = Request()
        self.flavor_name = ''
        self.flavor_id = ''
        self.vcpus = 0
        self.ram = 0
        self.disk = 0
        self.ephemeral = 0
        self.rxtx = 1
        self.swap = 0
        self.pushButton_add_addflavor.clicked.connect(self.add_flavor)

    def add_flavor(self):
        try:
            self.flavor_name = self.lineEdit_add_flavorname.text()
            if self.flavor_name == '':
                MessageBox().warn('警告', '请输入云主机类型名称')
                return
            self.vcpus = int(self.spinBox_add_flavorvcpu.text())
            if self.vcpus == 0:
                MessageBox().warn('警告', '请输入云主机类型CPU数量')
                return
            elif self.vcpus < 1:
                MessageBox().warn('警告', '云主机类型CPU数量不能小于1')
                return
            self.ram = int(self.spinBox_add_flavorram.text())
            if self.ram == 0:
                MessageBox().warn('警告', '请输入云主机类型内存大小')
                return
            elif self.ram < 1:
                MessageBox().warn('警告', '云主机类型内存大小不能小于1')
                return
            self.disk = int(self.spinBox_add_flavordisk.text())
            if self.disk == 0:
                MessageBox().warn('警告', '请输入云主机类型磁盘大小')
                return
            elif self.disk < 1:
                MessageBox().warn('警告', '云主机类型磁盘大小不能小于1')
                return
            self.flavor_id = self.lineEdit_add_flavorid.text()
            if self.flavor_id != '':
                for flavor in self.request.get_flavors():
                    if flavor['id'] == self.flavor_id:
                        MessageBox().warn('警告', '云主机类型ID已存在')
                        return
            self.swap = self.spinBox_add_flavorswap.text()
            self.ephemeral = self.spinBox_add_flavorephemeral.text()
            self.rxtx = self.spinBox_add_flavorrxtx.text()
            res = self.request.add_flavor(self.flavor_name, self.ram, self.vcpus, self.disk, self.ephemeral, self.swap,
                                          self.rxtx, self.flavor_id)
            if res:
                MessageBox().info('提示', '添加云主机类型成功')
                self.parent.show_flavor_tree_thread()
                self.close()
        except Exception as e:
            MessageBox().warn('警告', f'系统错误：{e}')


class AddImage(QDialog, Ui_AddImage):
    def __init__(self, parent: Index):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('logo.ico'))
        self.setWindowTitle('添加镜像')
        self.parent = parent
        self.request = Request()
        self.file = None
        self.visibility = 'shared'
        self.prtected = False
        self.disk_format_listview = QListView()
        self.disk_format_listview.setStyleSheet("""QListView {
                                                    background-color: white;
                                                }
                                                
                                                QListView::item {
                                                    background-color: white;
                                                }
                                                
                                                QListView::item:selected {
                                                    background-color: #C32E24;
                                                    color: white;
                                                }""")
        self.comboBox_add_disk_format.setView(self.disk_format_listview)
        self.comboBox_add_disk_format.addItems(
            ['iso-光盘镜像', 'ova-开放式虚拟设备', 'ploop-并行回环磁盘', 'qcow2-QEMU模拟器', 'vdi-虚拟磁盘镜像',
             'vhd-虚拟硬盘', 'vmdk-虚拟机磁盘', 'aki-Amazon 内核镜像', 'ami-Amazon 机器镜像', 'ari-Amazon Ramdisk镜像',
             'docker-Docker镜像'])
        self.lineEdit_add_imagefile.setReadOnly(True)
        self.pushButton_add_addimage.clicked.connect(self.add_image)
        self.pushButton_add_imagefile.clicked.connect(self.select_file)
        self.checkBox_add_add_ifprotected.toggled.connect(self.check_add_ifprotected)
        self.radioButton_add_public.clicked.connect(self.radio_visibility)
        self.radioButton_add_private.clicked.connect(self.radio_visibility)
        self.radioButton_add_shared.clicked.connect(self.radio_visibility)
        self.radioButton_add_social.clicked.connect(self.radio_visibility)

    def radio_visibility(self):
        if self.radioButton_add_public.isChecked():
            self.visibility = 'public'
        elif self.radioButton_add_private.isChecked():
            self.visibility = 'private'
        elif self.radioButton_add_shared.isChecked():
            self.visibility = 'shared'
        elif self.radioButton_add_social.isChecked():
            self.visibility = 'community'
        else:
            self.visibility = 'shared'

    def check_add_ifprotected(self):
        if self.checkBox_add_add_ifprotected.isChecked():
            self.prtected = True
        else:
            self.prtected = False

    def select_file(self):
        self.file, _ = QFileDialog.getOpenFileName(self, '选择镜像文件', 'D:/', 'All Files (*.*)')
        if self.file:
            self.lineEdit_add_imagefile.setText(self.file)
        else:
            self.lineEdit_add_imagefile.setText('')

    def add_image(self):
        try:
            self.imagename = self.lineEdit_add_imagename.text()
            if self.imagename == '':
                MessageBox().warn('警告', '镜像名称不能为空')
                return
            self.imagedesc = self.lineEdit_add_imagedesc.text()
            self.disk_format = self.comboBox_add_disk_format.currentText().split('-')[0]
            self.min_disk = self.spinBox_add_min_disk.text()
            self.min_ram = self.spinBox_add_min_ram.text()
            if self.file is None:
                MessageBox().warn('警告', '请选择镜像文件')
                return
            self.uploadimgthread = UploadImageFileThread(self)
            self.uploadimgthread.signal.connect(self.finished)
            self.uploadimgthread.start()

        except Exception as e:
            MessageBox().warn('警告', f'系统错误：{e}')

    def finished(self):
        MessageBox().info('提示', '添加镜像成功')
        self.parent.show_image_tree_thread()
        self.uploadimgthread.quit()
        self.uploadimgthread = None
        self.close()


class AddSubnet(QDialog, Ui_AddSubnet):
    def __init__(self, network_id):
        super().__init__()
        self.setupUi(self)
        self.request = Request()
        self.network_id = network_id
        self.setWindowIcon(QIcon('logo.ico'))
        self.setWindowTitle('添加子网')
        self.show_version()
        self.subnet_name = ''
        self.ip_version = 4
        self.cidr = ''
        self.gateway_ip = ''
        self.bangateway = True
        self.dhcp = False
        self.ip_pools = []
        self.dns_nameservers = []
        self.hosts_routes = []
        self.add_subnetipversion = QListView()
        self.add_subnetipversion.setStyleSheet("""QListView{background-color: white;}QListView::item{background-color: white
                                                        ;}QListView::item:selected {background-color: #C32E24;color: white;}""")
        self.comboBox_add_subnetipversion.setView(self.add_subnetipversion)
        self.pushButton_add_addsubnet.clicked.connect(self.add_subnet)
        self.checkBox_add_subnetifgateway.clicked.connect(self.ifgateway)

    def show_version(self):
        ip_versions = ['IPv4', 'IPv6']
        for i in range(0, 2):
            self.comboBox_add_subnetipversion.addItem(ip_versions[i])

    def ifgateway(self):
        if self.checkBox_add_subnetifgateway.isChecked():
            self.lineEdit_add_subnetgatewayip.setText('')
            self.lineEdit_add_subnetgatewayip.setEnabled(False)
        else:
            self.lineEdit_add_subnetgatewayip.setEnabled(True)

    def add_subnet(self):
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
            self.ip_version = self.comboBox_add_subnetipversion.currentText()
            self.ip_version = int(str(self.ip_version)[-1])
            self.cidr = self.lineEdit_add_subnetcidr.text()
            if self.checkBox_add_subnetifgateway.isChecked():
                self.bangateway = True
                self.gateway_ip = ''
            else:
                self.gateway_ip = self.lineEdit_add_subnetgatewayip.text()
                self.bangateway = False

            self.dhcp = self.checkBox_add_subnetifdhcp.isChecked()
            try:
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
        self.setupUi(self)
        self.request = Request()
        self.parent = parent
        self.setWindowIcon(QIcon('logo.ico'))
        self.setWindowTitle('添加用户')
        self.show_domain_project()
        self.domain_listview = QListView()
        self.domain_listview.setStyleSheet("""QListView{background-color: white;}QListView::item{background-color: white
                                                        ;}QListView::item:selected {background-color: #C32E24;color: white;}""")
        self.comboBox_add_domain.setView(self.domain_listview)

        self.project_listview = QListView()
        self.project_listview.setStyleSheet("""QListView{background-color: white;}QListView::item{background-color: white
                                                        ;}QListView::item:selected {background-color: #C32E24;color: white;}""")
        self.comboBox_add_project.setView(self.project_listview)
        self.pushButton_add_adduer.clicked.connect(self.add_user)
        self.pushButton_add_cancel.clicked.connect(self.close)

    def show_domain_project(self):
        try:
            self.combox_domain = {}
            self.combox_project = {}
            domains = self.request.get_domains()
            for domain in domains:
                self.combox_domain[domain['id']] = domain['name']
                self.comboBox_add_domain.addItem(domain['name'])

            projects = self.request.get_projects()
            for project in projects:
                self.combox_project[project['id']] = project['name']
                self.comboBox_add_project.addItem(project['name'])
        except Exception as e:
            MessageBox().warn('警告', f'系统错误：{e}')

    def add_user(self):
        if self.lineEdit_add_username.text() == '':
            MessageBox().warn('警告', '用户名不能为空')
        elif self.lineEdit_add_password.text() == '':
            MessageBox().warn('警告', '密码不能为空')
        else:
            try:
                username = self.lineEdit_add_username.text()
                password = self.lineEdit_add_password.text()
                domain_id = ''
                project_id = ''
                for k, v in self.combox_domain.items():
                    if v == self.comboBox_add_domain.currentText():
                        domain_id = k

                for k, v in self.combox_project.items():
                    if v == self.comboBox_add_project.currentText():
                        project_id = k
                desc = self.lineEdit_add_desc.text()
                res = self.request.add_user(username, password, domain_id, project_id, desc)
                if res:
                    MessageBox().info('提示', '添加用户成功')
                    self.parent.show_user_tree_thread()
                    self.close()
                else:
                    MessageBox().warn('警告', '添加用户失败')
            except Exception as e:
                MessageBox().warn('警告', f'系统错误：{e}')


class AddNetwork(QDialog, Ui_AddNetwork):
    def __init__(self, parent: Index):
        super().__init__()
        self.parent = parent
        self.provider = ''
        self.zone = ''
        self.networktype = ''
        self.network_projectid = ''
        self.networkname = ''
        self.networkdesc = ''
        self.admin_state_up = False
        self.shared = False
        self.outnetwork = False
        self.ifsubnet = False
        self.setupUi(self)
        self.request = Request()
        self.setWindowIcon(QIcon('logo.ico'))
        self.setWindowTitle('创建网络')
        self.show_add_network()
        self.add_networkproject_listview = QListView()
        self.add_networkproject_listview.setStyleSheet("""QListView{background-color: white;}QListView::item{background-color: white
                                                        ;}QListView::item:selected {background-color: #C32E24;color: white;}""")
        self.comboBox_add_networkproject.setView(self.add_networkproject_listview)

        self.add_networktype_listview = QListView()
        self.add_networktype_listview.setStyleSheet("""QListView{background-color: white;}QListView::item{background-color: white
                                                        ;}QListView::item:selected {background-color: #C32E24;color: white;}""")
        self.comboBox_add_networktype.setView(self.add_networktype_listview)

        self.add_networkzone_listview = QListView()
        self.add_networkzone_listview.setStyleSheet("""QListView{background-color: white;}QListView::item{background-color: white
                                                        ;}QListView::item:selected {background-color: #C32E24;color: white;}""")
        self.comboBox_add_networkzone.setView(self.add_networkzone_listview)
        self.pushButton_add_addnetwork.clicked.connect(self.create_network)
        self.pushButton_add_cancelnetwork.clicked.connect(self.close)

    def show_add_network(self):
        try:
            projects = self.request.get_projects()
            for project in projects:
                self.comboBox_add_networkproject.addItem(project['name'])
            network_type_items = ['vlan', 'vxlan', 'geneve', 'gre', 'flat', 'local']
            for network_type in network_type_items:
                self.comboBox_add_networktype.addItem(network_type)
            zones = ['nova']
            for zone in zones:
                self.comboBox_add_networkzone.addItem(zone)
        except Exception as e:
            MessageBox().warn('警告', f'系统错误：{e}')

    def create_network(self):
        try:
            projects = self.request.get_projects()
            networks = self.request.get_networks()
            if self.lineEdit_add_networkname.text() == '':
                MessageBox().warn('警告', '网络名称不能为空')
                return
            self.networkname = self.lineEdit_add_networkname.text()
            for network in networks:
                if network['name'] == self.networkname:
                    MessageBox().warn('警告', '网络名称已存在')
                    return
            projectname = self.comboBox_add_networkproject.currentText()
            for project in projects:
                if project['name'] == projectname:
                    self.network_projectid = project['id']
            self.networktype = self.comboBox_add_networktype.currentText()
            self.zone = self.comboBox_add_networkzone.currentText()

            self.networkdesc = self.lineEdit_add_networkdesc.text()
            self.admin_state_up = self.checkBox_add_networkadmin.isChecked()
            self.shared = self.checkBox_add_networkshared.isChecked()
            self.outnetwork = self.checkBox_add_networkout.isChecked()
            self.ifsubnet = self.checkBox_add_networkifsubnet.isChecked()
            if self.networktype in ['vlan', 'vxlan']:
                self.dialog_networktypevlan()
            elif self.networktype == 'local':
                res = self.request.add_network(self.networkname, self.admin_state_up, self.shared,
                                               self.network_projectid,
                                               self.networkdesc, self.networktype, self.outnetwork)
                if res:
                    self.network_id = res['id']
                    if self.ifsubnet:
                        subnet_dialog = AddSubnet(self.network_id)
                        if not subnet_dialog.exec_():
                            self.parent.show_network_tree_thread()
                            self.close()
            else:
                self.dialog_networktype()
        except Exception as e:
            MessageBox().warn('警告', f'系统错误：{e}')
            return

    def dialog_networktype(self):
        dialog = NetworkType(self)
        if not dialog.exec_():
            self.provider = dialog.provider
            res = self.request.add_network(self.networkname, self.admin_state_up, self.shared, self.network_projectid,
                                           self.networkdesc, self.networktype, self.outnetwork,
                                           self.provider)
            if res:
                self.network_id = res['id']
                if self.ifsubnet:
                    subnet_dialog = AddSubnet(self.network_id)
                    if not subnet_dialog.exec_():
                        self.parent.show_network_tree_thread()
                        self.close()

    def dialog_networktypevlan(self):
        dialog = NetworkTypeVlan(self)
        if not dialog.exec_():
            self.provider = dialog.provider
            self.vlan_id = dialog.vlan_id
            res = self.request.add_network(self.networkname, self.admin_state_up, self.shared, self.network_projectid,
                                           self.networkdesc, self.networktype, self.outnetwork,
                                           self.provider, self.vlan_id)
            if res:
                self.network_id = res['id']
                if self.ifsubnet:
                    subnet_dialog = AddSubnet(self.network_id)
                    if not subnet_dialog.exec_():
                        self.parent.show_network_tree_thread()
                        self.close()


class NetworkTypeVlan(QDialog, Ui_NetworkTypeVlan):
    def __init__(self, master: AddNetwork):
        super().__init__()
        self.master = master
        self.provider = ''
        self.vlan_id = ''
        self.setupUi(self)
        self.request = Request()
        self.setWindowIcon(QIcon('logo.ico'))
        self.setWindowTitle('Vlan网络类型')
        self.label_addnetworktypetitle.setText('Vlan网络类型')
        self.pushButton_add_addunetworktype.clicked.connect(self.add_networkvlan)

    def add_networkvlan(self):
        try:
            provider = self.lineEdit_add_networktype.text()
            vlan_id = self.lineEdit_add_networkvlanid.text()
            if vlan_id == '':
                MessageBox().warn('警告', 'Vlan ID不能为空')
                return
            else:
                self.provider = provider
                self.vlan_id = vlan_id
                self.close()
        except Exception as e:
            MessageBox().warn('警告', f'系统错误：{e}')


class NetworkType(QDialog, Ui_NetworkType):
    def __init__(self, master: AddNetwork):
        super().__init__()
        self.setupUi(self)
        self.master = master
        self.provider = None
        self.request = Request()
        self.setWindowIcon(QIcon('logo.ico'))
        self.setWindowTitle(self.master.networktype)
        self.label_addnetworktypetitle.setText(f"{self.master.networktype}网络类型")
        self.pushButton_add_addunetworktype.clicked.connect(self.add_networkprovider)

    def add_networkprovider(self):
        try:
            if self.lineEdit_add_networktype.text() == '':
                MessageBox().warn('警告', '物理网络不能为空')
                return
            self.provider = self.lineEdit_add_networktype.text()
            self.close()
        except Exception as e:
            MessageBox().warn('警告', f'系统错误：{e}')


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("logo.ico"))
        self.setWindowTitle("OpenStack")
        self.setFixedSize(1120, 800)
        self.session = Session()
        self.action_OpenStack.triggered.connect(self.get_openstack_url)
        self.action_OpenStackDocs.triggered.connect(self.get_docs_openstack_url)
        self.action_CSDN.triggered.connect(self.get_csdn_url)

        self.openstack = QStackedWidget()
        self.Login = Login(self.openstack, self)
        self.openstack.addWidget(self.Login)

        self.setCentralWidget(self.openstack)

    def get_openstack_url(self):
        url = "https://www.openstack.org/"
        webbrowser.open(url)

    def get_docs_openstack_url(self):
        url = "https://docs.openstack.org/zh_CN/"
        webbrowser.open(url)

    def get_csdn_url(self):
        url = "https://blog.csdn.net/lj2023103338"
        webbrowser.open(url)

    def closeEvent(self, event):
        flag = MessageBox().quest('退出', '是否退出？')
        if flag:
            self.session.write({
                "ip": "",
                "username": "",
                "password": "",
                "domain": "",
                "project": "",
                "token": "",
                "headers": ""
            })
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont("resources/fonts/HarmonyOS_Sans_SC_Medium.ttf")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
