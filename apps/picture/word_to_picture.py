import requests
import hashlib
import base64
import hmac
import json
import uuid
from time import mktime
from PIL import Image
from io import BytesIO
from urllib.parse import urlencode
from datetime import datetime
from wsgiref.handlers import format_date_time
from settings.db import configs
from utils.constant import RET
from settings.log import log_error
from libs.ali.oss import OssManage

OSS_PREFIX = configs.OSS_PREFIX


class AssembleHeaderException(Exception):
    def __init__(self, msg):
        self.message = msg


class Url:
    def __init__(this, host, path, schema):
        this.host = host
        this.path = path
        this.schema = schema


# calculate sha256 and encode to base64
def sha256base64(data):
    sha256 = hashlib.sha256()
    sha256.update(data)
    digest = base64.b64encode(sha256.digest()).decode(encoding='utf-8')
    return digest


def parse_url(requset_url):
    stidx = requset_url.index("://")
    host = requset_url[stidx + 3:]
    schema = requset_url[:stidx + 3]
    edidx = host.index("/")
    if edidx <= 0:
        raise AssembleHeaderException("invalid request url:" + requset_url)
    path = host[edidx:]
    host = host[:edidx]
    u = Url(host, path, schema)
    return u


# 生成鉴权url
def assemble_ws_auth_url(requset_url, method="GET", api_key="", api_secret=""):
    u = parse_url(requset_url)
    host = u.host
    path = u.path
    now = datetime.now()
    date = format_date_time(mktime(now.timetuple()))
    # date = "Wed, 14 Aug 2024 09:57:10 GMT"
    signature_origin = "host: {}\ndate: {}\n{} {} HTTP/1.1".format(host, date, method, path)
    signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                             digestmod=hashlib.sha256).digest()
    signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
    authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
        api_key, "hmac-sha256", "host date request-line", signature_sha)
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
    values = {
        "host": host,
        "date": date,
        "authorization": authorization
    }
    return requset_url + "?" + urlencode(values)


# 生成请求body体
def getBody(appid, text):
    body = {
        "header": {
            "app_id": appid,  # 应用的app_id
            "uid": "123456789"  # 每个用户的id，非必传字段
        },
        "parameter": {
            "chat": {
                # 默认分辨率512*512
                "domain": "general",  # 需要使用的领域
                "temperature": 0.5,  # 核采样阈值,向上调整可以增加结果的随机程度，取值范围 (0，1] ，默认值0.5
                "max_tokens": 4096  # 回答的tokens的最大长度 ，最小值是1, 最大值是8192，默认值2048
            }
        },
        "payload": {
            "message": {
                "text": [
                    {
                        "role": "user",  # user表示是用户的问题，assistant表示AI的回复
                        "content": text  # 文本内容，该角色的对话内容，不得超过1000个字符，受Token限制，有效内容不能超过8192Token
                    }
                ]
            }
        }
    }
    return body


# 发起请求并返回结果
def main(text, appid, apikey, apisecret):
    host = 'http://spark-api.cn-huabei-1.xf-yun.com/v2.1/tti'
    url = assemble_ws_auth_url(host, method='POST', api_key=apikey, api_secret=apisecret)
    content = getBody(appid, text)
    response = requests.post(url, json=content, headers={'content-type': "application/json"}).text
    return response


# 将base64 的图片数据上传到阿里云
def base64_to_image(base64_data):
    # 解码base64数据
    img_data = base64.b64decode(base64_data)
    # 将图片上传到阿里云
    uuid_hex = uuid.uuid4().hex
    new_filename = f"{uuid_hex[:6]}.jpg"
    oss_file_key = f"{OSS_PREFIX}/{new_filename}"
    OssManage().file_upload(key=oss_file_key, file=img_data)
    img_url = f"https://{configs.BUCKET_NAME}.{configs.END_POINT}/{oss_file_key}"
    return img_url


# 解析并保存到指定位置
def parser_Message(message):
    data = json.loads(message)
    code = data['header']['code']
    if code != 0:
        log_error(f'请求错误码: {code}, 请求错误原因：{data}')
        return RET.THIRD_ERR, data
    else:
        text = data["payload"]["choices"]["text"]
        imageContent = text[0]
        imageBase = imageContent["content"]
        img_url = base64_to_image(imageBase)
        return RET.OK, img_url


if __name__ == '__main__':
    desc = '''生成一张图：远处有着高山，山上覆盖着冰雪，近处有着一片湛蓝的湖泊'''
    res = main(desc, appid=configs.SPARKAI_APP_ID, apikey=configs.SPARKAI_API_KEY, apisecret=configs.SPARKAI_API_SECRET)
    # 保存到指定位置
    print(parser_Message(res))
