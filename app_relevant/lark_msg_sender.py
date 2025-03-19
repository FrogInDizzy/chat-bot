import json

import aiohttp

from app_relevant.token_manager import TokenManager


class LarkMsgSender():
    def __init__(self, token_manager: TokenManager) -> None:
        """
        feishu message sender
        Args:
            token_manager: token manager
        """
        self.prefix = "https://open.feishu.cn/open-apis/im/v1/messages/"
        self.suffix = "/reply"
        self.token_manager = token_manager

    async def send(self, msg, msg_id):
        """
        send message to feishu
        Args:
            msg: message
            msg_id:  message_id

        Returns:

        """
        url = self.prefix + msg_id + self.suffix
        headers = {
            'Authorization': 'Bearer ' + self.token_manager.get_token(),  # your access token
            'Content-Type': 'application/json'
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=json.dumps({
                "msg_type": "text",
                "content": json.dumps({
                    "text": msg,
                })
            })) as response:
                data = await response.json()
        if (data["code"] == 99991668 or data["code"] == 99991663):  # token expired
            await self.token_manager.update()
            await self.send(msg, msg_id)
        elif (data["code"] == 0):
            return
        else:
            print("unreachable")
            print(data)
            pass