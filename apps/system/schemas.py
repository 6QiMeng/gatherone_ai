from pydantic import Field, BaseModel


class RegisterSchema(BaseModel):
    """
    注册
    """
    sms_code: str = Field(...)
    name: str = Field(..., min_length=1, max_length=20)
    mobile: str = Field(..., min_length=11, max_length=11, regex=r"^1[3-9]\d{9}$")
    password: str = Field(...)


class LoginSchema(BaseModel):
    """
    登录
    """

    mobile: str = Field(..., min_length=11, max_length=11, regex=r"^1[3-9]\d{9}$")
    password: str = Field(...)


class ResetPasswordSchema(BaseModel):
    """重置密码"""

    mobile: str = Field(..., min_length=11, max_length=11, regex=r"^1[3-9]\d{9}$")
    new_password: str = Field(...)
    new_password2: str = Field(...)
    sms_code: str = Field(...)


class SmsLoginSchema(BaseModel):
    """
    短信验证码登录
    """

    mobile: str = Field(...)
    sms_code: str = Field(...)
