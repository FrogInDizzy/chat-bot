import uuid

import arrow
import traceback
from constants.general_con import TIME_FORMAT
from public_library.utils.dotmap_cus import DotMap
from public_library.utils.json_util import bo_one
from public_library.utils.logger_wall import get_logger
from public_library.utils.wrapper_utils import check_class_attr
from setting import LOG_DIR, USER_CONFIG_JSON_DIR

_logger = get_logger(f'{__file__}', LOG_DIR)


class UpdateCardMsg:
    def __init__(self, config_info):
        self.c = DotMap(config_info)
        self.s = DotMap()
        self.is_continue = True

    @check_class_attr(check_item=['is_continue'])
    def search(self):
        user_config = bo_one.load_json(USER_CONFIG_JSON_DIR)
        find_result = user_config.get(self.c.open_chat_id, {}) # 获取user_config.json中的配置信息
        if not find_result: # 如果没有获取到配置信息
            example_config={
                "_id": str(uuid.uuid4()),
                "chat_id": self.c.open_chat_id,
                "model_name": "gpt35-common",  # gpt4
                "temperature": 0,  # gpt4
                "chat_mode": "qa",  # cc/ce(qa)
                "create_time": arrow.utcnow().format(TIME_FORMAT),
                "update_time": arrow.utcnow().format(TIME_FORMAT)
            }
        else:
            example_config=find_result # 如果获取到配置信息
        _logger.info(f"查看{self.c.open_chat_id}的卡片配置信息:\n {find_result}")
        latest_config = {
            "create_time": arrow.utcnow().format(TIME_FORMAT),
            self.s.config_name: self.s.config_value,  # gpt4
            "update_time": arrow.utcnow().format(TIME_FORMAT),
        } # 获取用户通过卡片回调的最新的配置信息
        example_config.update(latest_config) # 更新配置信息
        user_config[self.c.open_chat_id] = example_config # 更新user_config.json

        _logger.info(f"卡片配置更新为: {user_config}")

        bo_one.save_json(user_config, USER_CONFIG_JSON_DIR)

    def fetcher(self):
        self.s.config_name = self.c.action.value.config_name
        self.s.config_value = self.c.action.option
        self.s.action_value = self.c.action.value.config_name
        _logger.debug(f'config_name_value:{self.s.config_name}:{self.s.config_value}')
        _logger.debug(f'action_value:{self.s.action_value}')
        pass

    def main(self):
        try:
            self.fetcher()
            self.search()
        except Exception as e:
            sim_err = str(e)
            msg_error = traceback.format_exc()
            _logger.error(
                f' 简单报错:{sim_err} 复杂报错:{msg_error},')


if __name__ == '__main__':
    temp = {'app_id': 'cli_a5c9322fe03a900e', 'open_id': 'ou_bc024775e9db5a8002ee048d486c2313', 'user_id': '76e1bf88',
            'open_message_id': 'om_81b1a1ff5cf14a01f95cdf2df018d6a8',
            'open_chat_id': 'oc_16f8dafb092a9517dc6d0f34f079b9f0', 'tenant_key': '162604252d43575f',
            'token': 'c-733a1e2ae5348c03ad9dd2bed36c7f2233ed9069',
            'action': {
                'value': {'config_name': 'model_name'},
                'tag': 'select_static',
                'option': 'gpt35-common'}}
    # temp = {
    #     'operator': {'tenant_key': '162604252d43575f', 'open_id': 'ou_b8d4feffe34c79e9955c6ca363ae75dc',
    #                  'union_id': 'on_94508006d5f44b244e7ef03bd1144cd1'},
    #     'token': 'c-c67bf933c543ad7c1b9e18c4ae0ec96336e0e27f',
    #     'action': {'value': {'config_name': 'model_name'}, 'tag': 'select_static', 'option': 'gpt35-common'},
    #     'host': 'im_message', 'context': {'open_message_id': 'om_3c2e58063b90e0346bfeafbb3d0b5e42',
    #                                       'open_chat_id': 'oc_9b964cad54991eb0d0a0684e9d92b78c'}}
    UpdateCardMsg(temp).main()
    pass
