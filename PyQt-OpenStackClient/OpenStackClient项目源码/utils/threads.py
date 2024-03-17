from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QTreeWidgetItem
from utils.messagebox import MessageBox


class ShowUserTrees(QThread):
    signal = pyqtSignal(bool)

    def __init__(self, parent: QWidget):
        super().__init__()
        self.parent = parent

    def run(self):
        try:
            self.parent.tree_users.clear()
            users = self.parent.request.get_users()
            domains = self.parent.request.get_domains()
            projects = self.parent.request.get_projects()
            roots = {}
            children = {}
            for i in range(len(users)):
                roots[i] = QTreeWidgetItem(self.parent.tree_users)
                roots[i].setText(0, str(i + 1))
                roots[i].setText(1, users[i]['name'])
                roots[i].setText(2, users[i]['id'])
                roots[i].setText(3, users[i]['links']['self'])
                for domain in domains:
                    if domain['id'] == users[i]['domain_id']:
                        roots[i].setText(4, domain['name'])
                        break
                roots[i].setText(5, users[i]['domain_id'])
                try:
                    for project in projects:
                        if project['id'] == users[i]['default_project_id']:
                            roots[i].setText(6, project['name'])
                            break
                    roots[i].setText(7, users[i]['default_project_id'])
                except KeyError:
                    roots[i].setText(6, '无')
                    roots[i].setText(7, '无')
                children[i] = {}
                children[i]["name"] = QTreeWidgetItem(roots[i])
                children[i]["name"].setText(0, "用户名：")
                children[i]["name"].setText(1, users[i]['name'])
                children[i]["id"] = QTreeWidgetItem(roots[i])
                children[i]["id"].setText(0, "用户ID：")
                children[i]["id"].setText(1, users[i]['id'])
                children[i]["links"] = QTreeWidgetItem(roots[i])
                children[i]["links"].setText(0, "用户链接：")
                children[i]["links"].setText(1, users[i]['links']['self'])
                children[i]["domain"] = QTreeWidgetItem(roots[i])
                children[i]["domain"].setText(0, "域ID：")
                children[i]["domain"].setText(1, users[i]['domain_id'])
                children[i]["default_project"] = QTreeWidgetItem(roots[i])
                try:
                    children[i]["default_project"].setText(0, "项目ID：")
                    children[i]["default_project"].setText(1, users[i]['default_project_id'])
                except KeyError:
                    children[i]["default_project"].setText(0, "项目：")
                    children[i]["default_project"].setText(1, '无')
        except Exception as e:
            MessageBox().warn("错误", str(e))

        self.signal.emit(True)


class ShowNetworkTrees(QThread):
    signal = pyqtSignal(bool)

    def __init__(self, parent: QWidget):
        super().__init__()
        self.parent = parent

    def run(self):
        try:
            self.parent.tree_networks.clear()
            networks = self.parent.request.get_networks()
            subnets = self.parent.request.get_subnets()
            roots = {}
            children = {}
            for i in range(len(networks)):
                roots[i] = QTreeWidgetItem(self.parent.tree_networks)
                roots[i].setText(0, str(i + 1))
                roots[i].setText(1, networks[i]['name'])
                roots[i].setText(2, networks[i]['id'])
                roots[i].setText(3, networks[i]['project_id'])
                roots[i].setText(4, networks[i]['provider:network_type'])
                if networks[i]['shared'] == 'True':
                    roots[i].setText(5, "共享网络")
                else:
                    roots[i].setText(5, "私有网络")
                roots[i].setText(6, networks[i]['status'])
                roots[i].setText(7, networks[i]['created_at'])

                children[i] = {}
                children[i]["name"] = QTreeWidgetItem(roots[i])
                children[i]["name"].setText(0, "网络名称：")
                children[i]["name"].setText(1, networks[i]['name'])

                children[i]["id"] = QTreeWidgetItem(roots[i])
                children[i]["id"].setText(0, "网络ID：")
                children[i]["id"].setText(1, networks[i]['id'])

                children[i]["project_id"] = QTreeWidgetItem(roots[i])
                children[i]["project_id"].setText(0, "项目ID：")
                children[i]["project_id"].setText(1, networks[i]['project_id'])

                children[i]["provider:physical_network"] = QTreeWidgetItem(roots[i])
                if networks[i]['provider:physical_network'] == 'None':
                    children[i]["provider:physical_network"].setText(0, "物理网络：")
                    children[i]["provider:physical_network"].setText(1, "无")
                else:
                    children[i]["provider:physical_network"].setText(0, "物理网络：")
                    children[i]["provider:physical_network"].setText(1, networks[i]['provider:physical_network'])

                children[i]["provider:network_type"] = QTreeWidgetItem(roots[i])
                children[i]["provider:network_type"].setText(0, "网络类型：")
                children[i]["provider:network_type"].setText(1, networks[i]['provider:network_type'])

                children[i]["provider:segmentation_id"] = QTreeWidgetItem(roots[i])
                if networks[i]['provider:segmentation_id'] == 'None':
                    children[i]["provider:segmentation_id"].setText(0, "网络段：")
                    children[i]["provider:segmentation_id"].setText(1, "无")
                else:
                    children[i]["provider:segmentation_id"].setText(0, "网络段：")
                    children[i]["provider:segmentation_id"].setText(1, str(networks[i]['provider:segmentation_id']))

                children[i]["shared"] = QTreeWidgetItem(roots[i])
                children[i]["shared"].setText(0, "共享：")
                if networks[i]['shared'] == 'True':
                    children[i]["shared"].setText(1, '是')
                else:
                    children[i]["shared"].setText(1, '否')

                children[i]["status"] = QTreeWidgetItem(roots[i])
                children[i]["status"].setText(0, "状态：")
                if networks[i]['status'] == 'ACTIVE':
                    children[i]["status"].setText(1, '活跃')
                elif networks[i]['status'] == 'BUILD':
                    children[i]["status"].setText(1, '创建中')

                children[i]["created_at"] = QTreeWidgetItem(roots[i])
                children[i]["created_at"].setText(0, "创建时间：")
                children[i]["created_at"].setText(1, networks[i]['created_at'])

                children[i]["subnets"] = {}
                children[i]["subnets"]["item"] = QTreeWidgetItem(roots[i])
                children[i]["subnets"]["item"].setText(0, "子网：")
                children[i]["subnets"]["item"].setText(1, "子网信息")
                for nsubnet in networks[i]['subnets']:
                    children[i]["subnets"][nsubnet] = {}
                    children[i]["subnets"][nsubnet]["item"] = QTreeWidgetItem(children[i]["subnets"]["item"])
                    for subnet in subnets:
                        if subnet['network_id'] == networks[i]['id'] and subnet['id'] == nsubnet:
                            children[i]["subnets"][nsubnet]['item'].setText(0, "子网名称")
                            children[i]["subnets"][nsubnet]['item'].setText(1, subnet['name'])
                            children[i]["subnets"][nsubnet]['info'] = {}
                            for key, value in subnet.items():
                                if key == 'id':
                                    children[i]["subnets"][nsubnet]['info'][key] = QTreeWidgetItem(
                                        children[i]["subnets"][nsubnet]['item'])
                                    children[i]["subnets"][nsubnet]['info'][key].setText(0, "子网ID")
                                    children[i]["subnets"][nsubnet]['info'][key].setText(1, subnet[key])
                                elif key == 'cidr':
                                    children[i]["subnets"][nsubnet]['info'][key] = QTreeWidgetItem(
                                        children[i]["subnets"][nsubnet]['item'])
                                    children[i]["subnets"][nsubnet]['info'][key].setText(0, "CIDR")
                                    children[i]["subnets"][nsubnet]['info'][key].setText(1, subnet[key])
                                elif key == 'gateway_ip':
                                    children[i]["subnets"][nsubnet]['info'][key] = QTreeWidgetItem(
                                        children[i]["subnets"][nsubnet]['item'])
                                    children[i]["subnets"][nsubnet]['info'][key].setText(0, "网关IP")
                                    children[i]["subnets"][nsubnet]['info'][key].setText(1, subnet[key])
                                elif key == 'ip_version':
                                    children[i]["subnets"][nsubnet]['info'][key] = QTreeWidgetItem(
                                        children[i]["subnets"][nsubnet]['item'])
                                    children[i]["subnets"][nsubnet]['info'][key].setText(0, "IP版本")
                                    children[i]["subnets"][nsubnet]['info'][key].setText(1, str(subnet[key]))
                                elif key == 'dns_nameservers':
                                    children[i]["subnets"][nsubnet]['info'][key] = QTreeWidgetItem(
                                        children[i]["subnets"][nsubnet]['item'])
                                    if subnet[key] == []:
                                        children[i]["subnets"][nsubnet]['info'][key].setText(0, "DNS服务器")
                                        children[i]["subnets"][nsubnet]['info'][key].setText(1, '无')
                                    else:
                                        children[i]["subnets"][nsubnet]['info'][key].setText(0, "DNS服务器")
                                        for dns in subnet[key]:
                                            children[i]["subnets"][nsubnet]['info'][key].addChild(QTreeWidgetItem(
                                                children[i]["subnets"][nsubnet]['info'][key]))
                                            children[i]["subnets"][nsubnet]['info'][key].child(
                                                children[i]["subnets"][nsubnet]['info'][key].childCount() - 1).setText(
                                                0, dns)
                                elif key == 'enable_dhcp':
                                    children[i]["subnets"][nsubnet]['info'][key] = QTreeWidgetItem(
                                        children[i]["subnets"][nsubnet]['item'])
                                    if subnet[key] == 'True':
                                        children[i]["subnets"][nsubnet]['info'][key].setText(0, "DHCP")
                                        children[i]["subnets"][nsubnet]['info'][key].setText(1, '是')
                                    else:
                                        children[i]["subnets"][nsubnet]['info'][key].setText(0, "DHCP")
                                        children[i]["subnets"][nsubnet]['info'][key].setText(1, '否')
                                elif key == 'allocation_pools':
                                    children[i]["subnets"][nsubnet]['info'][key] = QTreeWidgetItem(
                                        children[i]["subnets"][nsubnet]['item'])
                                    if not subnet[key]:
                                        children[i]["subnets"][nsubnet]['info'][key].setText(0, "IP池")
                                        children[i]["subnets"][nsubnet]['info'][key].setText(1, '无')
                                    else:
                                        children[i]["subnets"][nsubnet]['info'][key].setText(0, "IP池")
                                        for pool in subnet['allocation_pools']:
                                            children[i]["subnets"][nsubnet]['info'][key].addChild(QTreeWidgetItem(
                                                children[i]["subnets"][nsubnet]['info'][key]))
                                            children[i]["subnets"][nsubnet]['info'][key].child(
                                                children[i]["subnets"][nsubnet]['info'][
                                                    key].childCount() - 1).setText(
                                                0, "起始IP")

                                            children[i]["subnets"][nsubnet]['info'][key].addChild(QTreeWidgetItem(
                                                children[i]["subnets"][nsubnet]['info'][key]))
                                            children[i]["subnets"][nsubnet]['info'][key].child(
                                                children[i]["subnets"][nsubnet]['info'][
                                                    key].childCount() - 1).setText(
                                                0, "结束IP")

                                            children[i]["subnets"][nsubnet]['info'][key].child(
                                                children[i]["subnets"][nsubnet]['info'][
                                                    key].childCount() - 2).setText(
                                                1, pool['start'])
                                            children[i]["subnets"][nsubnet]['info'][key].child(
                                                children[i]["subnets"][nsubnet]['info'][
                                                    key].childCount() - 1).setText(
                                                1, pool['end'])
                                elif key == 'tenant_id':
                                    if subnet[key]:
                                        children[i]["subnets"][nsubnet]['info'][key] = QTreeWidgetItem(
                                            children[i]["subnets"][nsubnet]['item'])
                                        children[i]["subnets"][nsubnet]['info'][key].setText(0, "租户ID")
                                        children[i]["subnets"][nsubnet]['info'][key].setText(1, str(subnet[key]))
                                    else:
                                        children[i]["subnets"][nsubnet]['info'][key] = QTreeWidgetItem(
                                            children[i]["subnets"][nsubnet]['item'])
                                        children[i]["subnets"][nsubnet]['info'][key].setText(0, "租户ID")
                                        children[i]["subnets"][nsubnet]['info'][key].setText(1, '无')

                                elif key == 'project_id':

                                    if subnet[key]:
                                        children[i]["subnets"][nsubnet]['info'][key] = QTreeWidgetItem(
                                            children[i]["subnets"][nsubnet]['item'])
                                        children[i]["subnets"][nsubnet]['info'][key].setText(0, "项目ID")
                                        children[i]["subnets"][nsubnet]['info'][key].setText(1, str(subnet[key]))
                                    else:
                                        children[i]["subnets"][nsubnet]['info'][key] = QTreeWidgetItem(
                                            children[i]["subnets"][nsubnet]['item'])
                                        children[i]["subnets"][nsubnet]['info'][key].setText(0, "项目ID")
                                        children[i]["subnets"][nsubnet]['info'][key].setText(1, '无')

                                elif key == 'description':

                                    if subnet[key]:
                                        children[i]["subnets"][nsubnet]['info'][key] = QTreeWidgetItem(
                                            children[i]["subnets"][nsubnet]['item'])
                                        children[i]["subnets"][nsubnet]['info'][key].setText(0, "描述")
                                        children[i]["subnets"][nsubnet]['info'][key].setText(1, str(subnet[key]))
                                    else:
                                        children[i]["subnets"][nsubnet]['info'][key] = QTreeWidgetItem(
                                            children[i]["subnets"][nsubnet]['item'])
                                        children[i]["subnets"][nsubnet]['info'][key].setText(0, "描述")
                                        children[i]["subnets"][nsubnet]['info'][key].setText(1, '无')
                                elif key == 'created_at':

                                    if subnet[key]:
                                        children[i]["subnets"][nsubnet]['info'][key] = QTreeWidgetItem(
                                            children[i]["subnets"][nsubnet]['item'])
                                        children[i]["subnets"][nsubnet]['info'][key].setText(0, "创建时间")
                                        children[i]["subnets"][nsubnet]['info'][key].setText(1, str(subnet[key]))
                                    else:
                                        children[i]["subnets"][nsubnet]['info'][key] = QTreeWidgetItem(
                                            children[i]["subnets"][nsubnet]['item'])
                                        children[i]["subnets"][nsubnet]['info'][key].setText(0, "创建时间")
                                        children[i]["subnets"][nsubnet]['info'][key].setText(1, '无')

                children[i]["availability_zones"] = QTreeWidgetItem(roots[i])
                children[i]["availability_zones"].setText(0, "可用域：")
                children[i]["availability_zones"].setText(1,
                                                          ", ".join(zone for zone in networks[i]['availability_zones']))

                children[i]["router:external"] = QTreeWidgetItem(roots[i])
                if networks[i]['router:external'] == 'True':
                    children[i]["router:external"].setText(0, "外部路由器：")
                    children[i]["router:external"].setText(1, '是')
                else:
                    children[i]["router:external"].setText(0, "外部路由器：")
                    children[i]["router:external"].setText(1, '否')

                children[i]["admin_state_up"] = QTreeWidgetItem(roots[i])
                if networks[i]['admin_state_up'] == 'True':
                    children[i]["admin_state_up"].setText(0, " 管理状态：")
                    children[i]["admin_state_up"].setText(1, '开启')
                else:
                    children[i]["admin_state_up"].setText(0, "管理状态状态：")
                    children[i]["admin_state_up"].setText(1, '关闭')

                children[i]["ipv6_address_scope"] = QTreeWidgetItem(roots[i])
                if networks[i]['ipv6_address_scope'] == 'None':
                    children[i]["ipv6_address_scope"].setText(0, "IPv6地址范围：")
                    children[i]["ipv6_address_scope"].setText(1, "无")
                else:
                    children[i]["ipv6_address_scope"].setText(0, "IPv6地址范围：")
                    children[i]["ipv6_address_scope"].setText(1, networks[i]['ipv6_address_scope'])
                children[i]["ipv4_address_scope"] = QTreeWidgetItem(roots[i])
                if networks[i]['ipv4_address_scope'] == 'None':
                    children[i]["ipv4_address_scope"].setText(0, "IPv4地址范围：")
                    children[i]["ipv4_address_scope"].setText(1, "无")
                else:
                    children[i]["ipv4_address_scope"].setText(0, "IPv4地址范围：")
                    children[i]["ipv4_address_scope"].setText(1, networks[i]['ipv4_address_scope'])

                children[i]["mtu"] = QTreeWidgetItem(roots[i])
                if networks[i]['mtu'] == 'None':
                    children[i]["mtu"].setText(0, "MTU：")
                    children[i]["mtu"].setText(1, "无")
                else:
                    children[i]["mtu"].setText(0, "MTU：")
                    children[i]["mtu"].setText(1, str(networks[i]['mtu']))

                children[i]["revision_number"] = QTreeWidgetItem(roots[i])
                children[i]["revision_number"].setText(0, "修订号：")
                children[i]["revision_number"].setText(1, str(networks[i]['revision_number']))

                children[i]["description"] = QTreeWidgetItem(roots[i])
                if networks[i]['description'] == 'None':
                    children[i]["description"].setText(0, "描述：")
                    children[i]["description"].setText(1, "无")
                else:
                    children[i]["description"].setText(0, "描述：")
                    children[i]["description"].setText(1, networks[i]['description'])
        except Exception as e:
            MessageBox().warn("错误", str(e))
        self.signal.emit(True)


class ShowImageTrees(QThread):
    signal = pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def run(self):
        try:
            self.parent.tree_images.clear()
            images = self.parent.request.get_images()
            roots = {}
            children = {}
            for i in range(len(images)):
                roots[i] = QTreeWidgetItem(self.parent.tree_images)
                roots[i].setText(0, str(i + 1))
                roots[i].setText(1, images[i]['name'])
                roots[i].setText(2, images[i]['id'])
                roots[i].setText(3, f"{images[i]['size'] / 1024 / 1024 / 8:.2f}MB")
                roots[i].setText(4, images[i]['container_format'])
                roots[i].setText(5, images[i]['disk_format'])
                if images[i]['status'] == 'active':
                    roots[i].setText(6, "运行中")
                else:
                    roots[i].setText(6, "已停止")
                roots[i].setText(7, images[i]['created_at'])
                children[i] = {}
                for k, v in images[i].items():
                    if k == 'id':
                        if v:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '镜像ID')
                            children[i][k].setText(1, v)
                        else:
                            pass
                    elif k == 'container_format':
                        if v:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '容器格式')
                            children[i][k].setText(1, v)
                        else:
                            pass
                    elif k == 'disk_format':
                        if v:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '镜像格式')
                            children[i][k].setText(1, v)
                        else:
                            pass
                    elif k == 'status':
                        if v == 'active':
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '状态')
                            children[i][k].setText(1, '运行中')
                        else:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '状态')
                            children[i][k].setText(1, '已停止')
                    elif k == 'created_at':
                        if v:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '创建时间')
                            children[i][k].setText(1, v)
                        else:
                            pass
                    elif k == 'updated_at':
                        if v:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '更新时间')
                            children[i][k].setText(1, v)
                        else:
                            pass
                    elif k == 'name':
                        if v:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '名称')
                            children[i][k].setText(1, v)
                        else:
                            pass
                    elif k == 'size':
                        if v:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '大小')
                            children[i][k].setText(1, f"{v / 1024 / 1024 / 8:.2f}MB")
                        else:
                            pass
                    elif k == 'description':
                        if v:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '描述')
                            children[i][k].setText(1, v)
                        else:
                            pass
                    elif k == 'min_ram':
                        if v:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '最小内存')
                            children[i][k].setText(1, str(v))
                        else:
                            pass
                    elif k == 'min_disk':
                        if v:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '最小磁盘')
                            children[i][k].setText(1, str(v))
                        else:
                            pass
                    elif k == 'file':
                        if v:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '文件')
                            children[i][k].setText(1, v)
                        else:
                            pass
                    elif k == 'owner':
                        if v:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '所有者')
                            children[i][k].setText(1, v)
                        else:
                            pass
                    elif k == 'visibility':
                        if v:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '可见性')
                            children[i][k].setText(1, v)
                        else:
                            pass
                    elif k == 'protected':
                        children[i][k] = QTreeWidgetItem(roots[i])
                        children[i][k].setText(0, '是否保护')
                        if v:
                            children[i][k].setText(1, '受保护的')
                        else:
                            children[i][k].setText(1, '未受保护的')
                    elif k == 'tags':
                        if v:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '标签')
                            children[i][k].setText(1, v)
                        else:
                            pass
                    elif k == 'self':
                        if v:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, 'self')
                            children[i][k].setText(1, v)
                        else:
                            pass
                    elif k == 'schema':
                        if v:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, 'schema')
                            children[i][k].setText(1, v)
                        else:
                            pass
                    elif k == 'os_hash_algo':
                        if v:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, 'hash算法')
                            children[i][k].setText(1, v)
                        else:
                            pass
                    elif k == 'virtual_size':
                        if v:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, '虚拟大小')
                            children[i][k].setText(1, f"{v / 1024 / 1024 / 8:.2f}MB")
                        else:
                            pass
                    elif k == 'checksum':
                        if v:
                            children[i][k] = QTreeWidgetItem(roots[i])
                            children[i][k].setText(0, 'checksum')
                            children[i][k].setText(1, v)
                        else:
                            pass
                    elif k == 'os_hash_value':
                        if v:
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
    signal = pyqtSignal(bool)

    def __init__(self, parent):
        super(ShowFlavorTrees, self).__init__()
        self.parent = parent

    def run(self):
        try:
            self.parent.tree_flavors.clear()
            flavors = self.parent.request.get_flavors()
            roots = {}
            children = {}
            for i in range(len(flavors)):
                roots[i] = QTreeWidgetItem(self.parent.tree_flavors)
                roots[i].setText(0, str(i + 1))
                roots[i].setText(1, flavors[i]['name'])
                roots[i].setText(2, flavors[i]['id'])
                roots[i].setText(3, str(flavors[i]['vcpus']))
                roots[i].setText(4, f"{flavors[i]['ram']}MB")
                roots[i].setText(5, f"{flavors[i]['disk']}GB")
                roots[i].setText(6, f"{flavors[i]['OS-FLV-EXT-DATA:ephemeral']}GB")
                if flavors[i]['swap']:
                    roots[i].setText(7, f"{flavors[i]['swap']}MB")
                else:
                    roots[i].setText(7, "0MB")
                roots[i].setText(8, f"{flavors[i]['rxtx_factor']}")
                children[i] = {}
                for key, value in flavors[i].items():
                    if key == 'links':
                        children[i]['links'] = {}
                        children[i]['links']['item'] = QTreeWidgetItem(roots[i])
                        children[i]['links']['item'].setText(0, '链接')
                        children[i]['links']['info'] = {}
                        for link in value:
                            children[i]['links']['info'][link['rel']] = QTreeWidgetItem(children[i]['links']['item'])
                            children[i]['links']['info'][link['rel']].setText(0, link['rel'])
                            children[i]['links']['info'][link['rel']].setText(1, link['href'])
                    elif key == 'ram':
                        children[i]['ram'] = QTreeWidgetItem(roots[i])
                        children[i]['ram'].setText(0, '内存大小')
                        children[i]['ram'].setText(1, str(value) + "MB")
                    elif key == 'disk':
                        children[i]['disk'] = QTreeWidgetItem(roots[i])
                        children[i]['disk'].setText(0, '磁盘大小')
                        children[i]['disk'].setText(1, str(value) + "GB")
                    elif key == 'OS-FLV-EXT-DATA:ephemeral':
                        children[i]['ephemeral'] = QTreeWidgetItem(roots[i])
                        children[i]['ephemeral'].setText(0, '临时磁盘大小')
                        children[i]['ephemeral'].setText(1, str(value) + "GB")
                    elif key == 'swap':
                        children[i]['swap'] = QTreeWidgetItem(roots[i])
                        children[i]['swap'].setText(0, 'Swap磁盘大小')
                        if value:
                            children[i]['swap'].setText(1, str(value) + "MB")
                        else:
                            children[i]['swap'].setText(1, "0MB")
                    elif key == 'rxtx_factor':
                        children[i]['rxtx_factor'] = QTreeWidgetItem(roots[i])
                        children[i]['rxtx_factor'].setText(0, 'RX/TX因子')
                        children[i]['rxtx_factor'].setText(1, str(value))
                    elif key == 'OS-FLV-DISABLED:disabled':
                        children[i]['disabled'] = QTreeWidgetItem(roots[i])
                        children[i]['disabled'].setText(0, '是否禁用')
                        if value:
                            children[i]['disabled'].setText(1, '是')
                        else:
                            children[i]['disabled'].setText(1, '否')
                    elif key == 'os-flavor-access:is_public':
                        children[i]['is_public'] = QTreeWidgetItem(roots[i])
                        children[i]['is_public'].setText(0, '是否公开')
                        if value:
                            children[i]['is_public'].setText(1, '是')
                        else:
                            children[i]['is_public'].setText(1, '否')
                    elif key == 'id':
                        children[i]['id'] = QTreeWidgetItem(roots[i])
                        children[i]['id'].setText(0, '云主机类型ID')
                        children[i]['id'].setText(1, str(value))
                    elif key == 'name':
                        children[i]['name'] = QTreeWidgetItem(roots[i])
                        children[i]['name'].setText(0, '云主机类型名称')
                        children[i]['name'].setText(1, str(value))
        except Exception as e:
            MessageBox().warn("警告", f"系统错误！{e}")
        self.signal.emit(True)


class ShowServerTrees(QThread):
    signal = pyqtSignal(bool)

    def __init__(self, parent):
        super(ShowServerTrees, self).__init__()
        self.parent = parent

    def run(self):
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
                            children[i][k].setText(0, '密钥对')
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
    signal = pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def run(self):
        self.parent.request.add_image(self.parent.imagename, self.parent.disk_format, self.parent.imagedesc,
                                      self.parent.min_disk, self.parent.min_ram,
                                      self.parent.visibility, self.parent.prtected, self.parent.file)
        self.signal.emit(True)
