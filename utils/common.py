import re
import string
import threading
from typing import Optional
from settings.db import Base, Row


def check_word(words):
    """检验字符串是否有特殊字符"""
    _strs = re.findall(f'[{string.punctuation}]+', words)
    _str = ''.join(_strs)
    if len(_str) != 1 and _str[-1] == '.':
        return False
    return True


def file_size_util(filee_size):
    """
    文件单位转换
    """
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    util = 'B'
    for u in units:
        if filee_size <= 1024:
            break
        filee_size /= 1024
        util = u
    return f"{filee_size}{util}"

class QueryResult:
    """
    将查询改为dict
    """
    @staticmethod
    def row_dict(query_result):
        if isinstance(query_result, Base):
            return query_result.to_dict()
        elif isinstance(query_result, Row):
            _map = dict(query_result._mapping)
            dic = {}
            for key, value in _map.items():
                if isinstance(value, Base):
                    dic.update(value.to_dict())
                else:
                    dic[key] = value
            return dic
        else:
            raise Exception("query_result should be a Row or Base~")

    # 将查询改为list
    @staticmethod
    def row_list(query_result):
        """
        查询单个使用，db.query().first()
        """
        _data = []
        for i in query_result:
            if isinstance(i, Row):
                _map = dict(i._mapping)
                dic = {}
                for key, j in _map.items():
                    if isinstance(j, Base):
                        dic.update(j.to_dict())
                    else:
                        dic[key] = j
                _data.append(dic)
            elif isinstance(i, Base):
                _data.append(i.to_dict())
            else:
                raise Exception("query_result should be a Row or Base~")
        return _data


class CommonQueryParams:
    """
    公共查询参数依赖
    """
    def __init__(self, q: Optional[str] = None, page: int = 1, page_size: int = 10, start_date: str = None,
                 end_date: str = None):
        self.q = q
        self.page = page
        self.page_size = page_size
        self.start_date = start_date
        self.end_date = end_date


class SingletonType(type):
    """
    使用单例模式时引用，metaclass=SingletonMeta
    """
    _instance_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with SingletonType._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instance
