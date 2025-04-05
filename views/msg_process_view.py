import json

from fastapi import Request, BackgroundTasks, APIRouter

from app_relevant.reply_lark_msg import reply_message
from app_relevant.update_card_msg import UpdateCardMsg
from config.fetch_config_by_ip import gcpi
from models.msg_process_model import LarkMsgType, LarkCardType
from public_library.utils.aes_cipher import AESCipher
from public_library.utils.logger_wall import get_logger
from setting import LOG_DIR

_logger = get_logger(f'{__file__}', LOG_DIR)

processed_message_ids = set()  # 存储已经处理过的消息id

router = APIRouter()


@router.post("/event")  # 接收事件的请求
async def process(message: LarkMsgType, request: Request, background_tasks: BackgroundTasks):
    cipher = AESCipher(gcpi.encryption_key)

    plaintext = json.loads(cipher.decrypt_string(message.encrypt))
    if 'challenge' in plaintext:  # url verification
        return {'challenge': plaintext['challenge']}
    _logger.info(f'plaintext: {plaintext["event"]}')
    message = plaintext['event'].get('message')

    if message is None:
        return {'message': 'ok'}  # 接受到消息后，立即返回ok，避免客户端重试

    message_id = plaintext['event']['message']['message_id']
    if message_id not in processed_message_ids:
        # 将message_id加入到已处理列表，避免下次重复处理
        processed_message_ids.add(message_id)
        background_tasks.add_task(
            reply_message, plaintext)  # reply in background

    return {'message': 'ok'}  # 接受到消息后，立即返回ok，避免客户端重试


@router.post("/card")
async def process_card(message: LarkCardType, request: Request, background_tasks: BackgroundTasks):
    if gcpi.first_card_auth:
        cipher = AESCipher(gcpi.encryption_key)

        plaintext = json.loads(cipher.decrypt_string(message.encrypt))
        if 'challenge' in plaintext:  # url verification
            return {'challenge': plaintext['challenge']}
    model_dict = message.model_dump()
    # _logger.info(f'card 收到请求: {model_dict}')
    challenge = model_dict.get('challenge', '')
    if challenge:  # url verification
        return {'challenge': message.challenge}
    UpdateCardMsg(model_dict).main()
    return {'message': 'ok'}  # 接受到消息后，立即返回ok，避免客户端重试

if __name__ == '__main__':
    cipher = AESCipher(gcpi.encryption_key)

    en = {
        'encrypt': 'GVT0AkKrKcFIquTMnpRqSAKARBMglUmc73h/GiOWBPvuXrsprlYWjIDob6E0NWUfd26wG3+Gl1p5AJqRM+3s8SLgHvB7Qtz72nIbwi0OilTW/hgt2JExs/pCfVJzCjCdsoI9ZD/MFkV4AENMf+G6q15r0jB9dvkFw60L9YYU2XyNt3EptT5kANJAWtOeAc5nbT/z+GHfT8bwdT9BtxIoodDG5Fv/T7/BZj8Gsttu8VxgOAxD0NLwI+9upBX8Ou5nabpFq7lk6k/0/41jzvL766uztETz8P0pH7M2X3IElkmeFcmwhnHAuxZ0HpI/WDJqggVH0fqtEnNSM0F+A/fZcduAAHf5oxRfbwJ0rT91flXVwFNMCY1PQt5bBu46SzoYnerG822zP6N6CUTec7mh7Py/rjdXd/vlNRTV83jVq/ibgxOcerLpwQCVGkPbm5kPT6lFzyXc8sAFpoCpWsgaDdaIuOdooCPG4dSyD3zOGStip3rDCjr5571YwA2CNwg0GNb3aFxrm7MG6Tbs7TynQ6rXCkLN2LwHco+ltHabCDN7ee2zIZAHhyzIrSHv8wDH5pRSk7ttZhneVV8HiRxBRwNmrdjrfD6qBqMsGBhdqamG0D+LMSVLykUwiHB93eDgGFejCQE2qNOV0aeDCTFO2UDHpyCLla++es8mC05hxnOkdAQ4/fbML0y9rTWf89MlcC1uDDd3WeznKupk9TCbNQ=='}
    plaintext = json.loads(cipher.decrypt_string(en['encrypt']))
    print(plaintext)
