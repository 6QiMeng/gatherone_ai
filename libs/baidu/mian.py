import base64
import json
from urllib.parse import quote_plus
from settings.base import configs
from utils.common import SingletonType
from libs import session


class BaiDuAPI(metaclass=SingletonType):
    def __init__(self):
        self.api_key = configs.BAI_DU_API_KEY
        self.secret_key = configs.BAI_DU_SECRET_KEY

    def __get_access_token(self):
        """
        获取百度token
        """
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": self.api_key, "client_secret": self.secret_key}
        return str(session.post(url, params=params).json().get("access_token"))

    def __get_file_content_as_base64(self, path, urlencoded=False):
        """
        获取文件base64编码
        :param path: 文件路径
        :param urlencoded: 是否对结果进行urlencoded
        :return: base64编码信息
        """
        with open(path, "rb") as f:
            content = base64.b64encode(f.read()).decode("utf8")
            if urlencoded:
                content = quote_plus(content)
        return content

    def voice_to_text(self, voice, file_type):
        """
        调用语音转文本
        """
        url = "https://vop.baidu.com/server_api"
        payload = json.dumps({
            "format": file_type,
            "rate": 16000,
            "channel": 1,
            "cuid": "4YYPXJt6CADXioaSP9H9pRugOpIYi8u4",
            "token": self.__get_access_token(),
            "speech": base64.b64encode(voice).decode('utf-8'),
            "len": 17982
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        response = session.post(url, headers=headers, data=payload)
        return response.json()
