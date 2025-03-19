import json
import uuid

import requests

from config.fetch_config_by_ip import gcpi
from constants.general_con import CARD_GENERAL_URL
from public_library.utils.dotmap_cus import DotMap
from public_library.utils.logger_wall import get_logger
from setting import LOG_DIR

_logger = get_logger(f'{__file__}', LOG_DIR)


class PushCardMsg:
    def __init__(self, config_info):
        self.c = DotMap(config_info)
        self.s = DotMap()

    def form_header(self):
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": gcpi.app_id,
            "app_secret": gcpi.app_secret,
        }

        response = requests.post(url, json=payload)
        resp_json = response.json()
        # _logger.info(f"request tenant_access_token respond result: {response.json()}")

        self.s.tenant_access_token = resp_json["tenant_access_token"]
        self.s.headers = {
            'Authorization': f'Bearer {self.s.tenant_access_token}',
        }

    def fetch_user_config(self):
        self.s.template_variable = {
            "chat_mode": "Choose conversation mode",
            "temperature": "Choose degree of innovation",
            "model_name": "Choose model",
            "total_cost": "0.0",

        }

    def form_msg_dict(self):
        msg_content = {
            "type": "template",
            "data": {
                "template_id": self.c.template_id,
                "template_variable": {
                    **self.s.template_variable,
                }
            }
        }
        _logger.debug(f"Card message content: {msg_content}")
        self.s.msg_dict = {
            "content": json.dumps(msg_content),
            "msg_type": "interactive",
            'receive_id': self.c.chat_id,
            "uuid": str(uuid.uuid4())
        }
        _logger.debug(f"Card Message Dictionary: {self.s.msg_dict}")

    def send_card(self):
        headers = {
            'Authorization': f'Bearer {self.s.tenant_access_token}',
        }
        card_url = CARD_GENERAL_URL.format(message_id=self.c.message_id)
        response = requests.post(card_url, headers=headers, json=self.s.msg_dict)
        _logger.info(f"sending card message: {response.json()}")

    def main(self):
        self.fetch_user_config()
        self.form_header()
        self.form_msg_dict()
        self.send_card()
        pass


if __name__ == '__main__':
    temp = {'template_id': 'AAqCWuc4CbG6f',
            'chat_id': 'oc_9b964cad54991eb0d0a0684e9d92b78c',
            'message_id': 'om_b4b9b0ee621fd532622f23b603d86fc7',
            'user_id': '76e1bf88'}
    PushCardMsg(temp).main()
