from loguru import logger
from pydantic import BaseModel, model_validator, Field


class LarkMsgType(BaseModel):
    encrypt: str = Field("", description="加密信息")

    @model_validator(mode="before")
    def check_mv(cls, v):
        logger.info(f"event 收到的请求: {v}")
        return v


class LarkCardType(BaseModel):
    challenge: str = Field("", description="加密信息")
    token: str = Field("", description="token信息")
    type: str = Field("", description="验证类型")
    app_id: str = Field("", description="app_id")
    open_id: str = Field("", description="open_id")
    user_id: str = Field("", description="open_id")
    open_message_id: str = Field("", description="open_id")
    open_chat_id: str = Field("", description="open_id")
    action: dict = Field("", description="open_id")
    encrypt: str = Field("", description="加密信息")

    @model_validator(mode="before")
    def check_mv(cls, v):
        logger.info(f"card 收到的原始请求: {v}")
        return v


if __name__ == '__main__':
    a = {'app_id': 'cli_a5c9322fe03a900e', 'open_id': 'ou_bc024775e9db5a8002ee048d486c2313',
         'user_id': '76e1bf88',
         'open_message_id': 'om_5e435a68e1d7e94c6b839b90c12a535d',
         'open_chat_id': 'oc_16f8dafb092a9517dc6d0f34f079b9f0',
         'tenant_key': '162604252d43575f', 'token': 'c-be5a493e5d55f8db7e14dad99281d19e37162114',
         'action': {'value': {'config_name': 'model_name'}, 'tag': 'select_static', 'option': 'gpt35-common'}}