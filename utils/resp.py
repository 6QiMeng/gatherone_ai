# -*- coding:utf-8 -*-
import sys
import traceback
from typing import Optional, Union, List, Dict
from utils.constant import RET, error_map
from starlette.responses import JSONResponse


class MyResponse(JSONResponse):
    def __init__(self, code: int = RET.OK, msg: str = error_map[RET.OK], total: Optional[int] = None,
                 data: Union[List, Dict] = None, err=None, **kwargs):
        """
        统一接口返回数据格式，json格式。
        """
        response_data = {
            'code': code,
            'msg': msg
        }
        if total is not None:
            response_data['total'] = total
        if data is not None:
            response_data['data'] = data
        if err:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            tb_info = traceback.extract_tb(exc_traceback)
            filename, line, func, text = tb_info[-1]
            module = filename.split('gatherone_crm/')[-1]
            response_data['msg'] = f'Error Occur IN:{module},Line NO:{line},Error Msg: {exc_value}'
        super().__init__(content=response_data, **kwargs)
