import requests
from requests.adapters import HTTPAdapter, Retry

session = requests.Session()
retries = Retry(total=3, backoff_factor=1)
session.mount('http://', HTTPAdapter(max_retries=retries))
session.mount('https://', HTTPAdapter(max_retries=retries))


class BaseRequest:
    def __init__(self):
        self.server_name = None
        self.request_url = None
        self.api_key = None
        self.access_token = None

    def get_request(self, url, params=None, headers=None, timeout=3,**kwargs):
        """
        get请求
        """
        if params is None:
            params = dict()
        if self.api_key:
            params.update({"api_key": self.api_key})
        if headers is None:
            headers = dict()
        try:
            resp = session.get(url=url, params=params, headers=headers, timeout=timeout)
            resp.json()
        except ValueError as e:
            raise Exception(f'{self.server_name}连接服务超时{e}')
        except Exception as e:
            raise Exception(f'错误{self.server_name}:{e}')
        else:
            if resp.get('code') != 0:
                raise Exception(f'{self.server_name}数据返回错误：{resp}')
        return resp

    def post_request(self, url, data, params=None, headers=None, timeout=3, **kwargs):
        """
        post：请求
        """
        if params is None:
            params = dict()
        if self.api_key:
            params.update({"api_key": self.api_key})
        if self.access_token:
            params.update({"access_token": self.access_token})
        if headers is None:
            headers = dict()
        try:
            resp = session.post(url=url, json=data, params=params, headers=headers, timeout=timeout)
            resp.json()
        except ValueError as e:
            raise Exception(f'{self.server_name}连接服务超时{e}')
        except Exception as e:
            raise Exception(f'错误{self.server_name}:{e}')
        else:
            if resp.get('code') != 0:
                raise Exception(f'{self.server_name}数据返回错误：{resp}')
        return resp

    def post_request_stream(self, url, data, params=None, headers=None, timeout=3,**kwargs):
        """
        返回文件流
        """
        if params is None:
            params = dict()
        if self.api_key:
            params.update({"api_key": self.api_key})
        if headers is None:
            headers = dict()
        try:
            resp = session.post(url=url, json=data, params=params, headers=headers, timeout=timeout)
        except ValueError as e:
            raise Exception(f'连接服务超时{e}')
        except Exception as e:
            raise e
        return resp.text
