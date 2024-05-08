from settings.base import configs
from micro_server.http.base import BaseRequest
from utils.common import SingletonType

# 继承BaseRequest例子
# class CRMClient(BaseRequest, metaclass=SingletonType):
#     """
#     CRM服务
#     """
#
#     def __init__(self):
#         super().__init__()
#         self.server_name = "crm_api服务"
#         self.api_key = configs.CRM_API_KEY
#         self.request_url = configs.CRM_SERVER
#
#     def customer_id_name(self, params=None):
#         """
#         获取结算名称和对应id,
#         """
#         url = f'{self.request_url}/advertisers/customer_id_name'
#         res = self.get_request(url=url, params=params)
#         return res

