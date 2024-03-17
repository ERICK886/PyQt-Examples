import requests
import json
from pathlib import Path
from .threads import *
from .messagebox import *


class Session(object):
    def __init__(self):
        self.session_path = Path(__file__).parent / "session.json"

    def read(self):
        try:
            with open(self.session_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
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
        with open(self.session_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


session = Session()


class Openstack(object):
    def __init__(self, ip, username, password, project_name, domain_name):
        self.ip = ip
        self.username = username
        self.password = password
        self.project_name = project_name
        self.domain_name = domain_name
        self.auth_url = f"http://{self.ip}:5000/v3/auth/tokens"  # 认证地址
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
        token = requests.post(self.auth_url, headers=self.headers, json=self.auth_data).headers['X-Subject-Token']
        return token

    def login(self):
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
        self.session = Session().read()
        self.ip = self.session['ip']
        self.headers = self.session['headers']
        self.auth_url = f"http://{self.ip}:5000/v3/auth/tokens"  # 认证地址
        self.user_url = f"http://{self.ip}:5000/v3/users"  # 用户创建地址
        self.network_url = f"http://{self.ip}:9696/v2.0/networks"  # 创建网络的url
        self.subnet_url = f"http://{self.ip}:9696/v2.0/subnets"
        self.domain_url = f"http://{self.ip}:5000/v3/domains"
        self.project_url = f"http://{self.ip}:5000/v3/projects"
        self.image_url = f"http://{self.ip}:9292/v2/images"
        self.flavor_url = f"http://{self.ip}:8774/v2/flavors"
        self.server_url = f"http://{self.ip}:8774/v2/servers"

    def get_users(self):
        users = requests.get(self.user_url, headers=self.headers).json()['users']
        return users

    def get_domains(self):
        domains = requests.get(self.domain_url, headers=self.headers).json()['domains']
        return domains

    def get_projects(self):
        projects = requests.get(self.project_url, headers=self.headers).json()['projects']
        return projects

    def get_networks(self):
        networks = requests.get(self.network_url, headers=self.headers).json()['networks']
        return networks

    def get_subnets(self):
        subnets = requests.get(self.subnet_url, headers=self.headers).json()['subnets']
        return subnets

    def get_images(self):
        images = requests.get(self.image_url, headers=self.headers).json()['images']
        return images

    def get_flavors(self):
        flavors = requests.get(self.flavor_url, headers=self.headers).json()['flavors']
        n_flavors = []
        for flavor in flavors:
            n_flavors.append(requests.get(f"{self.flavor_url}/{flavor['id']}", headers=self.headers).json()['flavor'])
        return n_flavors

    def get_servers(self):
        servers = requests.get(self.server_url, headers=self.headers).json()['servers']
        n_servers = []
        for server in servers:
            n_servers.append(requests.get(f"{self.server_url}/{server['id']}", headers=self.headers).json()['server'])
        return n_servers

    def delete_user(self, user_id):
        try:
            requests.delete(f"{self.user_url}/{user_id}", headers=self.headers)
            return True
        except Exception as e:
            MessageBox().warn('警告', f'用户删除失败，错误信息：{e}')
            return False

    def delete_network(self, network_id):
        try:
            requests.delete(f"{self.network_url}/{network_id}", headers=self.headers)
            return True
        except Exception as e:
            MessageBox().warn('警告', f'网络删除失败，错误信息：{e}')
            return False

    def delete_image(self, image_id):
        try:
            requests.delete(f"{self.image_url}/{image_id}", headers=self.headers)
            return True
        except Exception as e:
            MessageBox().warn('警告', f'镜像删除失败，错误信息：{e}')
            return False

    def delete_flavor(self, flavor_id):
        try:
            requests.delete(f"{self.flavor_url}/{flavor_id}", headers=self.headers)
            return True
        except Exception as e:
            MessageBox().warn('警告', f'镜像删除失败，错误信息：{e}')
            return False
    def delete_server(self, server_id):
        try:
            requests.delete(f"{self.server_url}/{server_id}", headers=self.headers)
            return True
        except Exception as e:
            MessageBox().warn('警告', f'服务器删除失败，错误信息：{e}')
            return False
    def add_user(self, username, password, domain_id, project_id, desc):
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
