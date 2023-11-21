# -*- coding: utf-8 -*-
class RET:
    OK = 0

    DB_ERR = 4001
    NO_DATA = 4002
    DATA_EXIST = 4003
    DATA_ERR = 4004
    INVALID_DATA = 4005

    SESSION_ERR = 4101
    LOGIN_ERR = 4102
    PARAM_ERR = 4103
    USER_ERR = 4104
    ROLE_ERR = 4105
    PWD_ERR = 4106
    CODE_ERR = 4107
    BIND_ERR = 4108
    PER_ERR = 4109
    PHONE_EXISTED = 4110
    INVITATION_CODE_ERR = 4111
    EMAIL_EXISTED = 4112
    CHANGE_FAILED = 4113
    QR_EXPIRED = 4114
    NO_SCAN = 4115
    WS_DISCONNECTED = 4116

    REQ_ERR = 4201
    IP_ERR = 4202
    THIRD_ERR = 4301
    IO_ERR = 4302

    SERVER_ERR = 4500
    UNKNOW_ERR = 4501
    EXPORT_ERR = 4502
    NO_SYSTEM_PERMISSION = 4503


error_map = {
    RET.OK: u"成功",

    RET.DB_ERR: u"数据库查询错误",
    RET.NO_DATA: u"无数据",
    RET.INVALID_DATA: u"无效数据",
    RET.DATA_EXIST: u"数据已存在",
    RET.DATA_ERR: u"数据错误",

    RET.SESSION_ERR: u"用户未登录",
    RET.LOGIN_ERR: u"用户登录失败",
    RET.PARAM_ERR: u"参数错误",
    RET.USER_ERR: u"用户不存在或未激活",
    RET.ROLE_ERR: u"用户身份错误",
    RET.PWD_ERR: u"密码错误",
    RET.CODE_ERR: U'验证码错误',
    RET.BIND_ERR: u"未绑定系统用户",
    RET.PER_ERR: u"权限错误",
    RET.PHONE_EXISTED: u"手机号已被注册",
    RET.INVITATION_CODE_ERR: u"邀请码错误",
    RET.EMAIL_EXISTED: u"邮箱已被注册",
    RET.CHANGE_FAILED: u"修改失败",
    RET.QR_EXPIRED: u"二维码失效",
    RET.NO_SCAN: u"未扫码",
    RET.WS_DISCONNECTED: u"WebSocket断开连接",

    RET.REQ_ERR: u"非法请求或请求次数受限",
    RET.IP_ERR: u"IP受限",
    RET.THIRD_ERR: u"第三方系统错误",
    RET.IO_ERR: u"文件读写错误",

    RET.SERVER_ERR: u"内部错误",
    RET.UNKNOW_ERR: u"未知错误",
    RET.EXPORT_ERR: u"导出错误",
    RET.NO_SYSTEM_PERMISSION: u"无系统权限",
}


class CodeType:
    FORGET_PWD = 'forget_pwd'
    BIND_WX = 'bind_wx'
    REGISTER = 'register'
