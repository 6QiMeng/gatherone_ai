import base64
import json
import urllib
from settings.base import configs
from utils.common import SingletonType
from libs import session


class BaiDuAPI(metaclass=SingletonType):
    def __init__(self):
        self.api_key = configs.BAI_DU_API_KEY
        self.secret_key = configs.BAI_DU_SECRET_KEY

    def get_access_token(self):
        """
        获取百度token
        """
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": self.api_key, "client_secret": self.secret_key}
        return str(session.post(url, params=params).json().get("access_token"))

    def get_file_content_as_base64(path, urlencoded=False):
        """
        获取文件base64编码
        :param path: 文件路径
        :param urlencoded: 是否对结果进行urlencoded
        :return: base64编码信息
        """
        with open('./北京.m4a', "rb") as f:
            content = base64.b64encode(f.read()).decode("utf8")
            if urlencoded:
                content = urllib.parse.quote_plus(content)
        return content

    def voice_to_text(self, voice):
        """
        调用语音转文本
        """
        url = "https://vop.baidu.com/server_api"
        payload = json.dumps({
            "format": "m4a",
            "rate": 16000,
            "channel": 1,
            "cuid": "4YYPXJt6CADXioaSP9H9pRugOpIYi8u4",
            "token": self.get_access_token(),
            "speech": voice,
            "len": 17982
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        response = session.post(url, headers=headers, data=payload)
        print(response.json())



if __name__ == '__main__':
    """
    支持m4a格式文件语音转文字。
    采样率16000
    """
    with open('./北京.m4a', 'rb') as f:
        content = base64.b64encode(f.read()).decode('utf-8')
    baidu = BaiDuAPI().voice_to_text(content)
