import random
import string
import time
from fastapi import APIRouter, Request, Path, Query, Depends
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from settings.base import configs
from settings.db import RedisClient,get_db
from utils.constant import RET
from utils.resp import MyResponse
from apps.system.models import UserModel
from apps.system.schemas import UserRegeisterSchema

SystemRouter = APIRouter()


@cbv(SystemRouter)
class UserView:
    request: Request

    @CustomerRouter.get("/sms_codes", description="发送短信验证码")
    async def send_sms_code(
            self,
            code_type: str = Query(...),
            mobile: str = Query(...),
            db: Session = Depends(get_db),
    ):
        area_mobile = mobile
        area_code = mobile.split(' ')[0]
        user_mobile = mobile.replace("+", "").replace(" ", "")
        if len(area_mobile) > 20:
            return MyResponse(code=RET.DATA_ERR, msg="手机号格式不正确，请重新输入")
        if area_code == '+86':
            user_mobile = re.sub(r"86", "", user_mobile, 1)
            if not re.match(r'^1[3-9]\d{9}$', user_mobile):
                return MyResponse(code=RET.DATA_ERR, msg="手机号格式不正确，请重新输入")
        register_ins = (
            db.query(AdvertiserRegister)
            .filter(
                AdvertiserRegister.mobile == area_mobile,
                AdvertiserRegister.status != RegisterStatus.REFUSE.value,
                AdvertiserRegister.is_delete == False,
            )
            .first()
        )
        user_ins = (
            db.query(AdvertiserUser)
            .filter(AdvertiserUser.mobile == area_mobile, AdvertiserUser.is_delete == False)
            .first()
        )
        # 当验证码类型为自助系统注册时
        if code_type == CodeType.ADVERTISER_REGISTER:
            # 如果注册用户存在并且状态不是已拒绝则返回手机号已存在
            if register_ins:
                return MyResponse(
                    code=RET.PHONE_EXISTED, msg=error_map[RET.PHONE_EXISTED]
                )
            # 如果用户已存在并且是激活状态则返回手机号已存在
            if user_ins:
                return MyResponse(
                    code=RET.PHONE_EXISTED, msg=error_map[RET.PHONE_EXISTED]
                )
        # 当验证码类型为授权子账号时
        if code_type == CodeType.AUTHORIZED_ACCOUNT:
            # 如果是子账号或者用户的状态不是已拒绝
            if register_ins:
                return MyResponse(
                    code=RET.PHONE_EXISTED, msg="该手机号不能被授权为子账号"
                )
            if user_ins:
                return MyResponse(code=RET.PHONE_EXISTED, msg="该手机号已被授权")
        # 当验证码类型为忘记密码或者自助系统登录时
        if code_type in [CodeType.ADVERTISER_FORGET_PWD, CodeType.ADVERTISER_LOGIN]:
            # 如果用户不存在
            if not user_ins:
                return MyResponse(code=RET.USER_ERR, msg=error_map[RET.USER_ERR])
            # 如果用户之前是子账号并且被现在是被取消状态
            if user_ins.p_id and user_ins.is_active == False:
                return MyResponse(code=RET.USER_ERR, msg=error_map[RET.USER_ERR])
            code_type = CodeType.ADVERTISER_FORGET_PWD if code_type == CodeType.ADVERTISER_FORGET_PWD else CodeType.ADVERTISER_LOGIN
        # 调用发送验证码的推送服务
        push_code, push_res = PushService().send_verification_code(code_type, user_mobile, area_code)
        return MyResponse(code=push_code, msg=push_res)

    @CustomerRouter.post("/registrations", description="注册")
    async def register(self, data: RegisterSchema, db: Session = Depends(get_db)):
        area_mobile = data.mobile
        area_code = data.mobile.split(' ')[0]
        user_mobile = data.mobile.replace("+", "").replace(" ", "")
        if len(area_mobile) > 20:
            return MyResponse(code=RET.DATA_ERR, msg="手机号格式不正确，请重新输入")
        if area_code == '+86':
            user_mobile = re.sub(r"86", "", user_mobile, 1)
            if not re.match(r'^1[3-9]\d{9}$', user_mobile):
                return MyResponse(code=RET.DATA_ERR, msg="手机号格式不正确，请重新输入")
        register_ins = (
            db.query(AdvertiserRegister)
            .filter(
                AdvertiserRegister.mobile == area_mobile,
                AdvertiserRegister.status != RegisterStatus.REFUSE.value,
                AdvertiserRegister.is_delete == False,
            )
            .first()
        )
        # 如果注册用户存在并且注册用户的状态不是已拒绝
        if register_ins:
            return MyResponse(code=RET.PHONE_EXISTED, msg=error_map[RET.PHONE_EXISTED])
        verify_code, verify_msg = verify_sms_code(data.code_type, user_mobile, data.sms_code, delete=True)
        # 校验验证码
        if verify_code != RET.OK:
            return MyResponse(code=verify_code, msg=verify_msg)
        # 添加到用户注册表
        new_user = AdvertiserRegister(
            company_name=data.company_name,
            contact=data.contact,
            mobile=area_mobile,
            email=data.email,
        )
        db.add(new_user)
        db.commit()
        return MyResponse(code=RET.OK, msg="注册成功")

    @CustomerRouter.post("/login", description="密码登录")
    async def login(self, data: LoginSchema, req_dev=Depends(get_device), db: Session = Depends(get_db)):
        area_mobile = data.mobile
        area_code = data.mobile.split(' ')[0]
        user_mobile = data.mobile.replace("+", "").replace(" ", "")
        if len(area_mobile) > 20:
            return MyResponse(code=RET.DATA_ERR, msg="手机号格式不正确，请重新输入")
        if area_code == '+86':
            user_mobile = re.sub(r"86", "", user_mobile, 1)
            if not re.match(r'^1[3-9]\d{9}$', user_mobile):
                return MyResponse(code=RET.DATA_ERR, msg="手机号格式不正确，请重新输入")
        register_ins = (
            db.query(AdvertiserRegister)
            .filter(
                AdvertiserRegister.mobile == area_mobile,
                AdvertiserRegister.is_delete == False,
            )
            .first()
        )
        register_info = (
            db.query(AdvertiserRegister)
            .filter(
                AdvertiserRegister.mobile == area_mobile,
                AdvertiserRegister.is_delete == True,
            )
            .first()
        )
        user_ins = (
            db.query(AdvertiserUser)
            .filter(
                AdvertiserUser.mobile == area_mobile, AdvertiserUser.is_delete == False
            )
            .first()
        )
        # 判断用户是否存在
        if not user_ins:
            # 不存在注册表
            if not register_ins:
                t = threading.Thread(target=add_login_record,
                                     args=(None, area_mobile, LoginStatus.ERROR, LoginDesc.USERNOTEXIST, *req_dev))
                t.start()
                return MyResponse(code=RET.USER_ERR, msg="该账号未注册")
            if register_info:
                t = threading.Thread(target=add_login_record,
                                     args=(
                                         register_info.user_id, area_mobile, LoginStatus.ERROR, LoginDesc.USERNOTEXIST,
                                         *req_dev))
                t.start()
                return MyResponse(code=RET.DATA_ERR, msg="该账号已注销")
            t = threading.Thread(target=add_login_record,
                                 args=(
                                     register_ins.user_id, area_mobile, LoginStatus.ERROR, LoginDesc.NOTACTIVE,
                                     *req_dev))
            t.start()
            return MyResponse(code=RET.DATA_ERR, msg="该账号注册申请未通过")
        # 判断用户状态是否是禁用
        if user_ins.is_active == False:
            t = threading.Thread(target=add_login_record,
                                 args=(user_ins.id, area_mobile, LoginStatus.ERROR, LoginDesc.NOTACTIVE, *req_dev))
            t.start()
            return MyResponse(code=RET.USER_ERR, msg="该账号已被禁用")
        # 判断密码是否一致
        if not check_password_hash(user_ins.password, data.password):
            t = threading.Thread(target=add_login_record,
                                 args=(user_ins.id, area_mobile, LoginStatus.ERROR, LoginDesc.PASSWORDERROR, *req_dev))
            t.start()
            return MyResponse(code=RET.DATA_ERR, msg="密码不正确")
        payload = {"user_id": user_ins.id}
        token = JwtTokenUtil.generate_jwt(payload)
        t = threading.Thread(target=add_login_record,
                             args=(user_ins.id, area_mobile, LoginStatus.SUCCESS, LoginDesc.LOGINSUCCESS, *req_dev))
        t.start()
        return MyResponse(code=RET.OK, msg="登录成功", data={"token": token})

    @CustomerRouter.post("/forget_password", description="忘记密码")
    async def forget_password(
            self, data: ResetPasswordSchema, db: Session = Depends(get_db)
    ):
        area_mobile = data.mobile
        area_code = data.mobile.split(' ')[0]
        user_mobile = data.mobile.replace("+", "").replace(" ", "")
        if len(area_mobile) > 20:
            return MyResponse(code=RET.DATA_ERR, msg="手机号格式不正确，请重新输入")
        if area_code == '+86':
            user_mobile = re.sub(r"86", "", user_mobile, 1)
            if not re.match(r'^1[3-9]\d{9}$', user_mobile):
                return MyResponse(code=RET.DATA_ERR, msg="手机号格式不正确，请重新输入")
        register_ins = (
            db.query(AdvertiserRegister)
            .filter(
                AdvertiserRegister.mobile == area_mobile,
                AdvertiserRegister.status == RegisterStatus.AGREE.value,
                AdvertiserRegister.is_delete == False,
            )
            .first()
        )
        user_ins = (
            db.query(AdvertiserUser)
            .filter(
                AdvertiserUser.mobile == area_mobile, AdvertiserUser.is_delete == False
            )
            .first()
        )
        # 如果用户不存在或者用户是禁用状态
        if not user_ins or user_ins.is_active != True:
            return MyResponse(code=RET.USER_ERR, msg="用户不存在或已禁用")
        # res = verify_sms_code(data.code_type, data.mobile, data.sms_code)
        # if res.code != RET.OK:
        #     return MyResponse(code=res.code, msg=error_map[res.code])
        verify_code, verify_msg = verify_sms_code(data.code_type, user_mobile, data.sms_code, delete=True)
        # 校验验证码
        if verify_code != RET.OK:
            return MyResponse(code=verify_code, msg=verify_msg)
        if register_ins:
            register_ins.password = data.password1
        user_ins.password = generate_password_hash(data.password1)
        db.commit()
        return MyResponse(code=RET.OK, msg="重置密码成功")

    @CustomerRouter.post("/sms_login", description="验证码登录")
    async def sms_login(self, data: SmsLoginSchema, req_dev=Depends(get_device), db: Session = Depends(get_db)):
        area_mobile = data.mobile
        area_code = data.mobile.split(' ')[0]
        user_mobile = data.mobile.replace("+", "").replace(" ", "")
        if len(area_mobile) > 20:
            return MyResponse(code=RET.DATA_ERR, msg="手机号格式不正确，请重新输入")
        if area_code == '+86':
            user_mobile = re.sub(r"86", "", user_mobile, 1)
            if not re.match(r'^1[3-9]\d{9}$', user_mobile):
                return MyResponse(code=RET.DATA_ERR, msg="手机号格式不正确，请重新输入")
        verify_code, verify_msg = verify_sms_code(data.code_type, user_mobile, data.sms_code, delete=True)
        # 校验验证码
        if verify_code != RET.OK:
            return MyResponse(code=verify_code, msg=verify_msg)
        register_ins = (
            db.query(AdvertiserRegister)
            .filter(
                AdvertiserRegister.mobile == area_mobile,
                AdvertiserRegister.is_delete == False,
            )
            .first()
        )
        register_info = (
            db.query(AdvertiserRegister)
            .filter(
                AdvertiserRegister.mobile == area_mobile,
                AdvertiserRegister.is_delete == True,
            )
            .first()
        )
        user_ins = (
            db.query(AdvertiserUser)
            .filter(
                AdvertiserUser.mobile == area_mobile, AdvertiserUser.is_delete == False
            )
            .first()
        )
        # 如果用户不存在
        if not user_ins:
            # 不存在注册表
            if not register_ins:
                t = threading.Thread(target=add_login_record,
                                     args=(None, area_mobile, LoginStatus.ERROR, LoginDesc.USERNOTEXIST, *req_dev))
                t.start()
                return MyResponse(code=RET.DATA_ERR, msg="该账号未注册")
            if register_info:
                t = threading.Thread(target=add_login_record,
                                     args=(register_info.user_id, area_mobile, LoginDesc.USERNOTEXIST, *req_dev))
                t.start()
                return MyResponse(code=RET.DATA_ERR, msg="该账号已注销")
            t = threading.Thread(target=add_login_record,
                                 args=(
                                     register_info.user_id, area_mobile, LoginStatus.ERROR, LoginDesc.NOTACTIVE,
                                     *req_dev))
            t.start()
            return MyResponse(code=RET.DATA_ERR, msg="该账号注册申请未通过或已被禁用")
        # 如果用户状态是禁用状态
        if user_ins.is_active == False:
            t = threading.Thread(target=add_login_record,
                                 args=(user_ins.id, area_mobile, LoginStatus.ERROR, LoginDesc.NOTACTIVE, *req_dev))
            t.start()
            return MyResponse(code=RET.USER_ERR, msg="该账号已被禁用")
        header = {"alg": "HS256", "typ": "JWT"}
        exp = time.time() + configs.ACCESS_TOKEN_EXPIRE  # 过期时间为8小时后
        secret = configs.SECRET_KEY  # 用于签名和验证的密钥
        payload = {"user_id": user_ins.id, "exp": exp}  # 要包含在JWT中的负载数据
        token = jwt.encode(payload, secret, algorithm="HS256", headers=header)
        t = threading.Thread(target=add_login_record,
                             args=(user_ins.id, area_mobile, LoginStatus.SUCCESS, LoginDesc.LOGINSUCCESS, *req_dev))
        t.start()
        return MyResponse(code=RET.OK, msg="登录成功", data={"token": token})
