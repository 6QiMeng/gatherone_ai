from openai import OpenAI
from settings.base import configs
from utils.common import SingletonType


class SparkAi(metaclass=SingletonType):
    def __init__(self):
        self.api_key = f"{configs.SPARKAI_API_KEY}:{configs.SPARKAI_API_SECRET}"
        self.client = OpenAI(
            api_key=self.api_key,
            base_url='https://spark-api-open.xf-yun.com/v1'  # 指向讯飞星火的请求地址
        )

    def ask_question(self, user, question):
        """
        0:正常
        10007:用户流量受限：服务正在处理用户当前的问题，需等待处理完成后再发送新的请求。（必须要等大模型完全回复之后，才能发送下一个问题）
        10013:输入内容审核不通过，涉嫌违规，请重新调整输入内容
        10014:输出内容涉及敏感信息，审核不通过，后续结果无法展示给用户
        10019:表示本次会话内容有涉及违规信息的倾向；建议开发者收到此错误码后给用户一个输入涉及违规的提示
        10907:token数量超过上限。对话历史+问题的字数太多，需要精简输入
        11200:授权错误：该appId没有相关功能的授权 或者 业务量超过限制
        11201:授权错误：日流控超限。超过当日最大访问量的限制
        11202:授权错误：秒级流控超限。秒级并发超过授权路数限制
        11203:授权错误：并发流控超限。并发路数超过授权路数限制
        """
        completion = self.client.chat.completions.create(
            model=f'{configs.SPARKAI_DOMAIN}',  # 指定请求的版本
            messages=[
                {
                    "role": user,
                    "content": question
                }
            ],
            stream=True
        )
        return completion


OpenAI_obj = SparkAi()

if __name__ == '__main__':
    spark = SparkAi()
    ack = spark.ask_question('user', 'ok')
    for i in ack:
        print(i)
