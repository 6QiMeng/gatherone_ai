# -*- coding: utf-8 -*-
import requests
from libs.open import session
from settings.base import configs
from utils.common import SingletonType


class TianAPIRequest(metaclass=SingletonType):
    def __init__(self):
        self.base_url = 'https://apis.tianapi.com'
        self.key = configs.TIANAPI_KEY

    # 地址解析
    def address_parse(self, address_text):
        url = f'{self.base_url}/addressparse/index'
        params = {'key': self.key, 'text': address_text}
        try:
            json_res = session.get(url, params=params, timeout=5).json()
        except requests.exceptions.RequestException as e:
            return {}
        if json_res.get('code') == 200:
            result = json_res.get('result')
            return {'name': result.get('name'), 'mobile': result.get('mobile'), 'address': result.get('detail')}
        return {}
