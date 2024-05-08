from utils.enum import BaseEnum


class Result(BaseEnum):
    """
    继承baseenum,
    实现Result.Default.value=0,Result.Default.desc=处理中
    """
    Default = ('0', '处理中')
    Success = ('1', '成功')
    Fail = ('2', '失败')
