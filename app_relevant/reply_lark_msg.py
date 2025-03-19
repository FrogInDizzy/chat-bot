import json
import re
import traceback

from app_relevant.lark_msg_sender import LarkMsgSender
from app_relevant.one_api_answer import AnswerByOneAPI
from app_relevant.push_card_msg import PushCardMsg
from app_relevant.token_manager import TokenManager
from config.fetch_config_by_ip import gcpi
from public_library.utils.json_util import bo_one
from public_library.utils.logger_wall import get_logger
from setting import *

_logger = get_logger(f'{__file__}', LOG_DIR)


async def reply_message(input: dict):
    message_id = input["event"]["message"]["message_id"]
    chat_id = input["event"]["message"]["chat_id"]
    user_id = input['event']['sender']['sender_id']['user_id']
    _logger.info(f' 用户请求 : {input}')

    if input['header']['token'] != gcpi.verification_token:
        return
    reply = "default"
    final_img_key_str = ""
    # # 检查输入中是否包含文本消息
    if 'event' in input and 'message' in input['event'] and 'content' in input['event']['message']:
        try:
            content = json.loads(input['event']['message']['content'])

            user_text = content.get('text', None)  # 单文本存储体
            if user_text is None:
                user_text_list = content.get('content', [])  # 多种格式的文本信息存储体
                final_text = []
                for item in user_text_list:
                    item: list
                    each_line = [inn.get('text', '') for inn in item]
                    final_text.append(''.join(each_line))
                else:
                    user_text = '\n'.join(final_text)
                final_img_key = []
                for item in user_text_list:  # 目前只支持一张图片
                    item: list
                    each_line = [inn.get('image_key', '') for inn in item]
                    final_img_key.append(''.join(each_line))
                else:
                    final_img_key = list(filter(lambda x: x, final_img_key))
                    final_img_key = final_img_key[:1]  # 目前只支持一张图片
                    final_img_key_str = '\n'.join(final_img_key)

            _logger.info(f'收到用户的原始信息为:{user_text}')
            reply = f'收到用户的原始信息为:{user_text}'
            # todo user_text的信息去请求openai服务器,或者gpt的返回结果,文档: https://platform.openai.com/docs/api-reference
            # todo requests.post方式请求openai 的接口
            user_text = re.sub('@_user_\d+', '', user_text)
            qq = {
                "question": user_text,
                "model_name": "gpt_35_turbo",
                "temperature": 0,
                "chat_mode": "qa",
            }
            user_config = bo_one.load_json(USER_CONFIG_JSON_DIR)
            curr_user_config = user_config.get(chat_id, {})
            _logger.debug(f'读取到当前用户的配置信息为:{curr_user_config}')
            qq.update(curr_user_config)
            if user_text.lower().strip() == '/hp':
                temp = {
                    "template_id": gcpi.help_card_template_id,
                    "chat_id": chat_id,
                    "message_id": message_id,
                    "user_id": user_id,
                }
                _logger.info(f'help card config:{temp}')
                udm = PushCardMsg(temp)
                udm.main()
                return
            abo = AnswerByOneAPI(qq)
            abo.main()
            reply = abo.s.answer

        except Exception as e:
            sim_e = str(e)
            _logger.error(f"消息处理出错:简单原因:{sim_e}; 复杂原因:{traceback.format_exc()}")
            # reply = sim_e
            # reply = '后台服务出错，请联系开发小哥:>'
    token_manager = TokenManager(app_id=gcpi.app_id, app_secret=gcpi.app_secret)
    sender = LarkMsgSender(token_manager)

    await sender.send(reply, message_id)
