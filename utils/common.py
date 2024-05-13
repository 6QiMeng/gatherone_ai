# -*- coding: utf-8 -*-
import asyncio
import concurrent.futures
import smtplib
from concurrent.futures import ThreadPoolExecutor
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from typing import Optional
import aiomysql
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry
from settings.base import configs
from settings.db import Base, Row
import os
import threading
from settings.log import log_error

retry = Retry(total=3, connect=3, read=3, status=3, backoff_factor=0.5, raise_on_redirect=False)
session = requests.Session()
session.mount('http://', HTTPAdapter(max_retries=retry))
session.mount('https://', HTTPAdapter(max_retries=retry))


# 将查询改为dict
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
def row_list(query_result):
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


# 公共查询参数依赖
class CommonQueryParams:
    def __init__(self, q: Optional[str] = None, page: int = 1, page_size: int = 10):
        self.q = q
        self.page = page
        self.page_size = page_size


def Num2MoneyFormat(change_number):
    """
    .转换数字为大写货币格式( format_word.__len__() - 3 + 2位小数 )
    change_number 支持 float, int, long, string
    """
    format_word = ["分", "角", "元",
                   "拾", "百", "千", "万",
                   "拾", "百", "千", "亿",
                   "拾", "百", "千", "万",
                   "拾", "百", "千", "兆"]

    format_num = ["零", "壹", "贰", "叁", "肆", "伍", "陆", "柒", "捌", "玖"]
    if type(change_number) == str:
        # - 如果是字符串,先尝试转换成float或int.
        if '.' in change_number:
            try:
                change_number = float(change_number)
            except:
                raise ValueError('%s   can\'t change' % change_number)
        else:
            try:
                change_number = int(change_number)
            except:
                raise ValueError('%s   can\'t change' % change_number)
    if isinstance(change_number, int):
        change_number = float(change_number)
    if type(change_number) == float:
        real_numbers = []
        for i in range(len(format_word) - 3, -3, -1):
            if change_number >= 10 ** i or i < 1:
                real_numbers.append(int(round(change_number / (10 ** i), 2) % 10))

    else:
        raise ValueError('%s   can\'t change' % change_number)

    zflag = 0  # 标记连续0次数，以删除万字，或适时插入零字
    start = len(real_numbers) - 3
    change_words = []
    for i in range(start, -3, -1):  # 使i对应实际位数，负数为角分
        if 0 != real_numbers[start - i] or len(change_words) == 0:
            if zflag:
                change_words.append(format_num[0])
                zflag = 0
            change_words.append(format_num[real_numbers[start - i]])
            change_words.append(format_word[i + 2])

        elif 0 == i or (0 == i % 4 and zflag < 3):  # 控制 万/元
            change_words.append(format_word[i + 2])
            zflag = 0
        else:
            zflag += 1

    if change_words[-1] not in (format_word[0], format_word[1]):
        # - 最后两位非"角,分"则补"整"
        change_words.append("整")

    return ''.join(change_words)


# Word转PDF
class DocxToPdf:
    def __init__(self, file_paths):
        self.file_paths = file_paths

    def upload_file(self):
        """
        return
        [{'file': 'upload_1c626dce57f02b264d34450fe3769c40.docx', 'size': 12914, 'name': '退款申请单.docx', 'ctime': '2023-08-14 05:56:00', 'host': 'filetools28.pdf24.org'}]
        """
        upload_url = 'https://filetools28.pdf24.org/client.php?action=upload'
        upload_results = []
        for file_path in self.file_paths:
            upload_data = {'file': open(file_path, 'rb')}
            resp = requests.post(url=upload_url, files=upload_data).json()
            upload_results.extend([
                {
                    'file': f.get('file'),  # 上传名
                    'size': f.get('size'),  # 尺寸大小
                    'name': f.get('name'),  # 文件名
                    'host': f.get('host')  # 服务器
                } for f in resp])
        return upload_results

    @staticmethod
    def convert_file(files):
        """
        convert_data = {
            "files": [
                {
                    'file': 'upload_2f00dc54a3fd48e5565e202214105675.docx',
                    'size': 14016,
                    'name': '退款申请单.docx',
                    'host': 'filetools28.pdf24.org'
                }
            ]
        }
        return
        {'jobId': 'convertToPdf_d1c88e796ccbe2f3654fe585775acdba'}
        """
        convert_url = 'https://filetools28.pdf24.org/client.php?action=convertToPdf'
        convert_data = {"files": files, 'language': 'zh-CN'}
        response = session.post(convert_url, json=convert_data).json()
        jobId = response.get('jobId')
        return jobId

    @staticmethod
    def get_status(jobId):
        status_url = f'https://filetools28.pdf24.org/client.php?action=getStatus&jobId={jobId}'
        response = requests.get(status_url).json()
        return response

    @staticmethod
    def get_download_link(jobId):
        download_url = f"https://filetools28.pdf24.org/client.php?mode=download&action=downloadJobResult&jobId={jobId}"
        # response = requests.get(download_url)
        # with open('res.pdf', 'wb') as f:
        #     f.write(response.content)
        return download_url

    def run(self):
        files = self.upload_file()
        jobId = self.convert_file(files)
        return self.get_download_link(jobId)


class SendEmail:
    def __init__(self, subject='', body='', body_type='plain', file=None, file_name=None, from_email=configs.SENDER,
                 to: list = [], cc: list = [],
                 attachments=None):
        self.subject = subject  # 邮件主题
        self.body = body  # 邮件正文
        self.body_type = body_type  # 邮件正文格式（plain/html）;默认纯文本plain
        self.from_email = from_email  # 发件邮箱
        self.file = file  # 二进制流
        self.file_name = file_name  # 文件名字
        self.to = to if to else list()  # 接收邮箱(List); 示例['13579@qq.com', '24681@qq.com']
        self.cc = cc if cc else list()
        self.attachments = attachments

    def send(self):
        try:
            msg = MIMEMultipart()
            msg['subject'] = self.subject
            # 邮件正文
            if self.body_type == "html":
                msg.attach(MIMEText(self.body, _subtype='html', _charset='utf-8'))
                # 邮件发/收件人显示中文
                msg['From'] = formataddr(pair=(configs.EMAIL_FROM_NAME, configs.SENDER))
                msg['To'] = ','.join(self.to)
                msg['Cc'] = ','.join(self.cc)
                server = None
                try:
                    server = smtplib.SMTP_SSL(configs.EMAIL_HOST, configs.EMAIL_PORT)
                    server.ehlo()
                    server.login(configs.SENDER, configs.PASSWORD)
                    server.sendmail(self.from_email, self.to + self.cc, msg.as_string())
                    server.quit()
                    return True
                except Exception as e:
                    log_error('邮件发送失败 Error:%s' % e)
                    return False
                finally:
                    if server is not None:
                        # server.close()
                        server.quit()
            else:
                txt = MIMEText(self.body, 'plain', 'utf-8')
                msg.attach(txt)
                # 添加附件
                if self.attachments:
                    if isinstance(self.attachments, list):
                        for attachment in self.attachments:
                            file_path = attachment
                            file_name = os.path.basename(file_path)
                            part = MIMEApplication(open(file_path, 'rb').read())
                            part.add_header('Content-Disposition', 'attachment',
                                            filename=file_name)  # filename给附件重命名,默认与原文件名一样
                            msg.attach(part)
                    else:
                        file_path = self.attachments
                        file_name = os.path.basename(file_path)
                        part = MIMEApplication(open(file_path, 'rb').read())
                        part.add_header('Content-Disposition', 'attachment', filename=file_name)
                        msg.attach(part)
                else:
                    part = MIMEApplication(self.file)
                    part.add_header('Content-Disposition', 'attachment', filename=self.file_name)
                    msg.attach(part)
                # 邮件发/收件人显示中文
                msg['From'] = formataddr(pair=(configs.EMAIL_FROM_NAME, configs.SENDER))
                if self.to is not None:
                    msg['To'] = ','.join(self.to)
                if self.cc is not None:
                    msg['Cc'] = ','.join(self.cc)
                server = None
                try:
                    server = smtplib.SMTP_SSL(configs.EMAIL_HOST, configs.EMAIL_PORT)
                    server.ehlo()
                    server.login(configs.SENDER, configs.PASSWORD)
                    server.sendmail(self.from_email, self.to + self.cc, msg.as_string())
                    return True  # 发送成功
                except Exception as e:
                    log_error('邮件发送失败 Error:%s' % e)
                    return False
                finally:
                    server.quit()
        except Exception as e:
            log_error('邮件发送失败 Error:%s' % e)
            return False


class SingletonType(type):
    _instance_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with SingletonType._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instance


class ChunkReadSQL:
    """
    调用
    res_df = await ChunkReadSQL.main('account', 'tb_meta_accounts')
    bio = BytesIO()
    csv_string = res_df.to_csv(bio, index=False, encoding='utf-8-sig')
    response = Response(content=csv_string, media_type='text/csv')
    response.headers['Content-Disposition'] = 'attachment;filename={}.xlsx'.format('data')
    """

    @staticmethod
    async def create_pool():
        pool = await aiomysql.create_pool(host=configs.MYSQL_SERVER, user=configs.MYSQL_USER,
                                          password=configs.MYSQL_PASSWORD, db=configs.MYSQL_DB_NAME, charset='utf8mb4')
        return pool

    @staticmethod
    async def get_total(pool, count_sql):
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(count_sql)
                count = cursor._rows[0][0]
                return count

    @staticmethod
    async def execute_query(conn, sql):
        async with conn.cursor() as cursor:
            await cursor.execute(sql)
            fields = [field[0] for field in cursor.description]
            result = await cursor.fetchall()
            return result, fields

    @staticmethod
    async def process_data(sql_type, pool, start, end, where_str="") -> pd.DataFrame:
        '''
        根据不同的操作（sql_type）选择对应的sql，得到DataFrame。
        '''
        async with pool.acquire() as conn:
            sql_dict = {
                "recharge": f"""
                    充值sql语句。
                """,
                "reset": f"""
                    清零sql语句。
                """,
                "meta_account": f"""
                SELECT
                    a.account_id AS 广告账户ID,
                    a.account_name AS 广告账户名称,
                    b.`name` AS 客户简称,
                    e.real_name AS 销售负责人,
                    c.`name` AS 开户主体名称,
                    d.`name` AS 投放方式,
                    a.open_date AS 开户时间,
                    a.inner_subject_name AS 内部开户主体名称,
                    a.product_link AS 产品链接,
                    a.account_type AS 账户类型,
                    a.description AS 描述,
                    'Meta' AS 投放媒介
                FROM
                (SELECT * FROM `tb_meta_accounts`) a
                LEFT JOIN tb_customers b ON a.customer_id = b.id
                LEFT JOIN tb_open_subjects c ON a.open_subject_id = c.id
                LEFT JOIN tb_put_ways d ON a.put_way = d.id
                LEFT JOIN tb_users e ON b.sell_id = e.id
                 WHERE a.is_delete = FALSE {where_str} LIMIT {start}, {end - start}
                """,
                "tiktok_account": f"""
                SELECT
                    a.account_id AS 广告账户ID,
                    a.account_name AS 广告账户名称,
                    b.`name` AS 客户简称,
                    c.real_name AS 销售负责人,
                    e.`name` AS 开户主体名称,
                    a.bc_id AS BC,
                    d.`name` AS 投放方式,
                    a.open_date AS 开户时间,
                    a.product_link AS 产品链接,
                    a.description AS 描述,
                    a.position AS 版位,
                    a.country AS 投放国家,
                    'Tiktok' AS 投放媒介
                FROM
                    (SELECT * FROM `tb_tiktok_accounts`) a
                LEFT JOIN tb_customers b ON a.customer_id = b.id
                LEFT JOIN tb_put_ways d ON a.put_way = d.id
                LEFT JOIN tb_open_subjects e ON e.id = a. open_subject_id
                LEFT JOIN tb_users c ON b.sell_id = c.id
                WHERE a.is_delete = FALSE {where_str}  LIMIT {start}, {end - start}
                    """,
                "google_account": f"""
                SELECT
                    a.account_id AS 广告账户ID,
                    a.account_name AS 广告账户名称,
                    b.`name` AS 客户简称,
                    c.real_name AS 销售负责人,
                    d.`name` AS 投放方式,
                    a.open_date AS 开户时间,
                    a.product_link AS 产品链接,
                    a.description AS 描述,
                    a.remark AS 备注,
                    'Google' AS 投放媒介
                FROM
                    (SELECT * FROM `tb_google_accounts`) a
                LEFT JOIN tb_customers b ON a.customer_id = b.id
                LEFT JOIN tb_put_ways d ON a.put_way = d.id
                LEFT JOIN tb_users c ON b.sell_id = c.id
                WHERE a.is_delete = FALSE {where_str}  LIMIT {start}, {end - start}
                                """,
                "kwai_account": f"""
                SELECT
                    a.account_id AS 广告账户ID,
                    a.account_name AS 广告账户名称,
                    b.`name` AS 客户简称,
                    c.real_name AS 销售负责人,
                    e.`name` AS 开户主体名称,
                    d.`name` AS 投放方式,
                    a.open_date AS 开户时间,
                    a.product_link AS 产品链接,
                    a.description AS 描述,
                    a.time_zone AS 账户时区,
                    a.product_type AS 产品类型,
                    'Kwai' AS 投放媒介
                FROM
                    (SELECT * FROM `tb_kwai_accounts`) a
                LEFT JOIN tb_customers b ON a.customer_id = b.id
                LEFT JOIN tb_put_ways d ON a.put_way = d.id
                LEFT JOIN tb_open_subjects e ON e.id = a. open_subject_id
                LEFT JOIN tb_users c ON b.sell_id = c.id
                WHERE a.is_delete = FALSE {where_str}  LIMIT {start}, {end - start}
                                            """,
                "twitter_account": f"""
                SELECT
                   a.account_id AS 广告账户ID,
                   a.account_name AS 广告账户名称,
                   b.`name` AS 客户简称,
                   c.real_name AS 销售负责人,
                   e.`name` AS 开户主体名称,
                   d.`name` AS 投放方式,
                   a.open_date AS 开户时间,
                   a.description AS 描述,
                   'Twitter' AS 投放媒介
               FROM
                    (SELECT * FROM  `tb_twitter_accounts`) a
               LEFT JOIN tb_customers b ON a.customer_id = b.id
               LEFT JOIN tb_put_ways d ON a.put_way = d.id
               LEFT JOIN tb_open_subjects e ON e.id = a. open_subject_id
               LEFT JOIN tb_users c ON b.sell_id = c.id
                WHERE a.is_delete = FALSE {where_str}  LIMIT {start}, {end - start}
                    """,
                "apple_account": f"""
                SELECT
                    a.account_id AS 广告账户ID,
                    a.account_name AS 广告账户名称,
                    b.`name` AS 客户简称,
                    c.real_name AS 销售负责人,
                    e.`name` AS 开户主体名称,
                    d.`name` AS 投放方式,
                    a.open_date AS 开户时间,
                    a.product_name AS 产品名称,
                    a.ad_group_plain_id AS 广告组计划ID,
                    a.product_link AS 产品链接,
                    a.description AS 描述,
                    'Apple' AS 投放媒介
                FROM
                    (SELECT * FROM  `tb_apple_accounts`) a
                LEFT JOIN tb_customers b ON a.customer_id = b.id
                LEFT JOIN tb_put_ways d ON a.put_way = d.id
                LEFT JOIN tb_open_subjects e ON e.id = a. open_subject_id
                LEFT JOIN tb_users c ON b.sell_id = c.id
                WHERE a.is_delete = FALSE {where_str}  LIMIT {start}, {end - start}
                """,
                "petal_account": f"""
                SELECT
                    a.account_id AS 广告账户ID,
                    a.account_name AS 广告账户名称,
                    b.`name` AS 客户简称,
                    c.real_name AS 销售负责人,
                    e.`name` AS 开户主体名称,
                    d.`name` AS 投放方式,
                    a.open_date AS 开户时间,
                    a.petal_account AS 华为账户,
                    a.password AS 密码,
                    'Petal' AS 投放媒介
                FROM
                        (SELECT * FROM  `tb_petal_accounts`) a
                LEFT JOIN tb_customers b ON a.customer_id = b.id
                LEFT JOIN tb_put_ways d ON a.put_way = d.id
                LEFT JOIN tb_open_subjects e ON e.id = a. open_subject_id
                LEFT JOIN tb_users c ON b.sell_id = c.id
                WHERE a.is_delete = FALSE {where_str}  LIMIT {start}, {end - start}
               """,
                "spend": f"""
                SELECT 
                    c.`name` 客户简称,
                    a.account_id 账户ID,
                    a.account_name 广告账户名称,
                    a.put_way 投放方式,
                    a.medium 投放媒介,
                    CONCAT(YEAR(a.date_end), '年', MONTH(a.date_end), '月') 消耗月份,
                    a.spend 消耗金额,
                    a.service_charge 服务费
                FROM 
                    (SELECT * FROM  `tb_spends`) a
                INNER JOIN tb_bills b on a.bill_id = b.id
                INNER JOIN tb_customers c on b.customer_id = c.id
                WHERE a.is_delete = FALSE {where_str}  LIMIT {start}, {end - start}
                """
            }
            # 执行查询操作
            result, fields = await ChunkReadSQL.execute_query(conn, sql_dict[sql_type])
            # 处理查询结果
            df = pd.DataFrame(result, columns=fields)
            return df

    @staticmethod
    async def main(sql_type, count_sql, where_str):
        # 创建数据库连接池
        pool = await ChunkReadSQL.create_pool()
        # 查询数据总量
        total = await ChunkReadSQL.get_total(pool, count_sql)
        # print('总数量:', total)
        # 定义分片大小
        if total < 10000:
            chunk_size = 500
        elif total < 50000:
            chunk_size = 2500
        elif total < 100000:
            chunk_size = 3500
        elif total < 200000:
            chunk_size = 5000
        else:
            chunk_size = 6000
        total_data = total
        # 计算分片数量
        num_chunks = total_data // chunk_size
        if total % chunk_size != 0:
            num_chunks += 1
        # print('总页', num_chunks)
        # 创建进程池
        with ThreadPoolExecutor(max_workers=50) as executor:
            # 创建事件循环
            loop = asyncio.get_event_loop()
            # 将进程池设置为协程的默认执行器
            loop.set_default_executor(executor)
            # 创建协程任务列表
            tasks = []
            for i in range(num_chunks):
                # 计算每个分片的起始和结束位置
                start = i * chunk_size
                end = (i + 1) * chunk_size
                # 创建协程任务
                task = loop.create_task(ChunkReadSQL.process_data(sql_type, pool, start, end, where_str))
                tasks.append(task)
            res_df = pd.DataFrame()
            # 等待所有协程任务完成
            if tasks:
                result = await asyncio.gather(*tasks)
                pool.close()
                # await pool.wait_closed()
                res_df = pd.concat(result)
            return res_df
