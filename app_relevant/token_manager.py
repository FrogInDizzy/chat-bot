import aiohttp
import json

from public_library.utils.logger_wall import get_logger
from setting import *

_logger = get_logger(f'{__file__}', LOG_DIR)


class TokenManager():
    def __init__(self, app_id, app_secret) -> None:
        """
        初始化token管理器
        Args:
            app_id:
            app_secret:
        """
        self.token = 'an_invalid_token'
        self.url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        self.req = {
            "app_id": app_id,
            "app_secret": app_secret
        }

    async def update(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, headers={
                'Content-Type': 'application/json; charset=utf-8'
            }, data=json.dumps(self.req), timeout=5) as response:
                data = await response.json()
                if (data["code"] == 0):
                    self.token = data["tenant_access_token"]

    def get_token(self):
        return self.token
