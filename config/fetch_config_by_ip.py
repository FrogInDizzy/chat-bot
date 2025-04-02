import os

import toml
from loguru import logger

from public_library.utils.dotmap_cus import DotMap
from setting import CONFIG_DIR, GLOBAL_CONFIG_DIR


class Singleton(object):
    def __init__(self, cls):
        self._cls = cls
        self._instance = {}

    def __call__(self):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls()
        return self._instance[self._cls]


@Singleton
class FetchConfigByIp:
    def __init__(self):
        self.curr_config = {}
        self.ip = ""
        self.curr_env = ""
        self.whole_result = {}
        self.project_info = {}
        self.fetch_curr_config()
        pass

    def fetch_curr_config(self):
        """
        获取当前机器的配置文件
        Returns:

        """
        # self.curr_env="test"
        self.curr_env = toml.load(GLOBAL_CONFIG_DIR)['env']
        logger.info(f'curr env :{self.curr_env}')

        config_filepath = os.path.join(CONFIG_DIR, "{}.toml".format(self.curr_env))
        if not os.path.exists(config_filepath):
            logger.error(f'CURR ENV:{self.curr_env}-->{config_filepath} not exists')
            raise Exception("config file not exists: {}".format(config_filepath))

        curr_whole_result = toml.load(config_filepath)  # .toml的全部数据
        self.project_info = DotMap(curr_whole_result).project_info

    # def main(self):
    #     # self.fetch_curr_ip()
    #     self.fetch_curr_config()
    #     pass


gcpi = FetchConfigByIp().project_info
pass
# lgc = FetchConfigByIp().project_info.zmq
# lgc2 = FetchConfigByIp().project_info.zmq
# lgc3 = FetchConfigByIp().project_info
# print(id(lgc))
# print(id(lgc2))
# print(id(lgc2))
# print('-------')
# lgc.main()
# gc = DotMap(lgc.whole_result)
# gc2 = DotMap(lgc2.whole_result)
# gcpi = gc.project_info
# gcpi2 = DotMap(lgc.whole_result).project_info
# print(id(gc))
# print(id(gcp))