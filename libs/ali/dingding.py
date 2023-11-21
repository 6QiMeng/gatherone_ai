# -*- coding: utf-8 -*-
import json
import hashlib
import base64
import hmac
import threading
import time
import requests
from urllib.parse import quote_plus
from settings.log import log_error
from settings.base import configs


class DingDing:
    def __init__(self):
        self.URL = "https://oapi.dingtalk.com/robot/send"
        self.headers = {'Content-Type': 'application/json'}

    def send_markdown(self, token, secret, title, content, at_mobiles):
        if not at_mobiles:
            at_mobiles = []
        timestamp = str(round(time.time() * 1000))
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = quote_plus(base64.b64encode(hmac_code))
        params = {'access_token': token, "sign": sign, 'timestamp': timestamp}
        data = {
            "msgtype": "markdown",
            "markdown": {"title": title, "text": content},
            "at": {"atMobiles": at_mobiles, "isAtAll": "false"}
        }
        try:
            requests.post(
                url=self.URL,
                data=json.dumps(data),
                params=params,
                headers=self.headers
            ).json()
        except Exception as e:
            log_error(e.__str__())

    def send_text(self, token, secret, content, at_mobiles):
        if not at_mobiles:
            at_mobiles = []
        timestamp = str(round(time.time() * 1000))
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = quote_plus(base64.b64encode(hmac_code))
        params = {'access_token': token, "sign": sign, 'timestamp': timestamp}
        data = {
            "msgtype": "text",
            "text": {"text": content},
            "at": {"atMobiles": at_mobiles, "isAtAll": "false"}
        }
        try:
            requests.post(
                url=self.URL,
                data=json.dumps(data),
                params=params,
                headers=self.headers
            ).json()
        except Exception as e:
            log_error(e.__str__())

    # 发送bug消息
    def send_err_message(self, token=configs.BUG_DD_TOKEN, secret=configs.BUG_DD_SECRET, title='', content='',
                         at_mobiles=None):
        t = threading.Thread(
            target=self.send_markdown,
            kwargs={'token': token, 'secret': secret, 'title': title, 'content': content, 'at_mobiles': at_mobiles})
        t.start()


dd = DingDing()
