import requests
from requests.adapters import HTTPAdapter, Retry

session = requests.Session()
retries = Retry(total=3, backoff_factor=1)
session.mount('http://', HTTPAdapter(max_retries=retries))
session.mount('https://', HTTPAdapter(max_retries=retries))


import socket
import re
from libs import session


class BaseRequest:
    def __init__(self):
        self.server_name = None
        self.request_url = None
        self.api_key = None
        self.access_token = None

    def check_server(self):
        host_ip = re.findall(
            r'(http|https)://([\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}:[\d]{1,5})/api/',
            self.request_url
        )
        if host_ip:
            host_ip = host_ip[0][1]
        else:
            try:
                domain = self.request_url.split('/')[2]
                socket.gethostbyname(domain)
            except socket.gaierror:
                return False, '域名解析失败'
            else:
                return True, '域名解析成功'
        try:
            host, port = host_ip.split(':')[0], int(host_ip.split(':')[1])
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect((host, port))
        except ConnectionRefusedError as e:
            return False, f'{self.server_name}未开启错误{e}'
        except Exception as e:
            return False, f'{self.server_name}未知错误{e}'
        return True, f'{self.server_name}开启'

    def get_request(self, url, params=None, headers=None):
        """
        get请求
        """
        status, msg = self.check_server()
        if status is False:
            raise Exception(msg)
        if params is None:
            params = dict()
        if self.api_key:
            params.update({"api_key": self.api_key})
        if headers is None:
            headers = dict()
        try:
            resp = session.get(url=url, params=params, headers=headers).json()
        except ValueError as e:
            raise Exception(f'{self.server_name}连接服务超时{e}')
        except Exception as e:
            raise Exception(f'错误{self.server_name}:{e}')
        else:
            if resp.get('code') != 0:
                raise Exception(f'{self.server_name}数据返回错误：{resp}')
        return resp

    def post_request(self, url, data, params=None, headers=None, alone_flag=False):
        """
        post：请求
        """
        status, msg = self.check_server()
        if status is False:
            raise Exception(msg)
        if params is None:
            params = dict()
        if self.api_key:
            params.update({"api_key": self.api_key})
        if self.access_token:
            params.update({"access_token": self.access_token})
        if headers is None:
            headers = dict()
        try:
            resp = session.post(url=url, json=data, params=params, headers=headers).json()
        except ValueError as e:
            raise Exception(f'{self.server_name}连接服务超时{e}')
        except Exception as e:
            raise Exception(f'错误{self.server_name}:{e}')
        else:
            if resp.get('code') != 0 and not alone_flag:
                raise Exception(f'{self.server_name}数据返回错误：{resp}')
        return resp

    def post_request_stream(self, url, data, params=None, headers=None):
        """
        返回文件流
        """
        status, msg = self.check_server()
        if status is False:
            raise Exception(msg)
        if params is None:
            params = dict()
        if self.api_key:
            params.update({"api_key": self.api_key})
        if headers is None:
            headers = dict()
        try:
            resp = session.post(url=url, json=data, params=params, headers=headers)
        except ValueError as e:
            raise Exception(f'crm连接服务超时{e}')
        except Exception as e:
            raise e
        return resp.text
