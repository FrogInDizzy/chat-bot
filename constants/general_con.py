DEBUG = True # 演示常量命名
PORT = 8000  # 演示常量命名
TIME_FORMAT = 'YYYY-MM-DD HH:mm:ss' # 记录数据的录入时间
TIME_FORMAT_PURE = 'YYYYMMDDHHmmss' #  记录数据的录入时间

CENTRAL_CONTROL_FILE_TYPE = ['csv', 'txt', 'xlsx']
GPT_CONFIG = {
    "gpt_4o": {
        "api_key": "sk-",
        "api_base": "https://",
        "model_name": "gpt-4o"
    },
    "gpt_35_turbo": {
        "api_key": "sk-",
        "api_base": "https://",
        "model_name": "gpt-3.5-turbo"
    }
}
CARD_GENERAL_URL = "https://open.feishu.cn/open-apis/im/v1/messages/{message_id}/reply?receive_id_type=chat_id"