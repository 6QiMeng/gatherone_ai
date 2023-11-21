from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.requests import Request
from apps import create_app
from utils.constant import RET
from utils.resp import MyResponse
import uvicorn

app = create_app()


# @app.exception_handler(HTTPException)
# async def invalid_token_exception_handler(request: Request, exc: HTTPException):
#     return MyResponse(code=RET.REQ_ERR, err=exc)
#
#
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     return MyResponse(code=RET.REQ_ERR, err=exc)
#
#
# @app.exception_handler(ValidationError)
# async def validation_exception_handler(request: Request, exc: ValidationError):
#     return MyResponse(code=RET.INVALID_DATA, err=exc)
#
#
# @app.exception_handler(Exception)
# async def generic_exception_handler(request: Request, exc: Exception):
#     return MyResponse(code=RET.SERVER_ERR, err=exc)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, env_file='.env', reload=True)
