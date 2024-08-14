import oss2
from utils.common import SingletonType
from settings.base import configs


class OssManage(metaclass=SingletonType):

    def __init__(self):
        self.AccessKeyId = configs.ACCESS_KEY_ID
        self.AccessKeySecret = configs.ACCESS_KEY_SECRET
        self.Endpoint = configs.END_POINT
        self.BucketName = configs.BUCKET_NAME
        try:
            self.auth = oss2.Auth(self.AccessKeyId, self.AccessKeySecret)
            self.bucket = oss2.Bucket(self.auth, self.Endpoint, self.BucketName)
            self.bucket.create_bucket(oss2.models.BUCKET_ACL_PUBLIC_READ)  # 设为公共读权限
        except Exception as e:
            raise e
        # bucket_info = self.bucket.get_bucket_info() # 获取bucket相关信息，如创建时间，访问Endpoint，Owner与ACL等

    def file_delete(self, key):
        """
        删除文件
        """
        try:
            result = self.bucket.delete_object(key)
            return result
        except Exception as e:
            raise e

    def file_upload(self, key, file):
        """
        上传文件
        """
        try:
            result = self.bucket.put_object(key, file)
            return result
        except Exception as e:
            raise e

    def get_obj_meta(self, key):
        """
        获取文件元信息
        """
        try:
            result = self.bucket.get_object_meta(key)
            return result
        except Exception as e:
            raise e

    def get_obj(self, key):
        """
        获取单个文件对象
        """
        try:
            result = self.bucket.get_object(key)
            return result
        except oss2.exceptions.NoSuchKey as e:
            raise e

    def get_all_obj(self):
        """
        获取bucket所有文件  返回文件对象生成器
        """
        try:
            return oss2.ObjectIterator(self.bucket)
        except Exception as e:
            raise e

    def exist_valid(self, key):
        """
        监测文件是否已存在
        """
        try:
            exist = self.bucket.object_exists(key)
            if exist:
                return True, 'File Existed'
            return False, 'File Not Existed'
        except Exception as e:
            raise e
