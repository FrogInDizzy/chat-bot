import requests
from tenacity import retry, stop_after_attempt, wait_fixed

from constants.general_con import GPT_CONFIG
from public_library.utils.dotmap_cus import DotMap
from public_library.utils.logger_wall import get_logger
from setting import LOG_DIR

_logger = get_logger(f'{__file__}', LOG_DIR)


class AnswerByOneAPI:
    def __init__(self, c):
        self.c = DotMap(c)
        self.s = DotMap()

    def prepare_one_api(self):
        self.s.one_api_headers = {
            'Authorization': f'Bearer {GPT_CONFIG[self.c.model_name]["api_key"]}',
            'Content-Type': 'application/json',
        }

        pass

    @retry(stop=stop_after_attempt(6), wait=wait_fixed(2))
    def call_one_api(self):
        json_data = {
            'model': GPT_CONFIG[self.c.model_name]['model_name'],
            "messages": [{"role": "user", "content": self.c.question}],
            'stream': False,
            "temperature": self.c.temperature
        }

        response = requests.post(f'{GPT_CONFIG[self.c.model_name]["api_base"]}/v1/chat/completions',
                                 headers=self.s.one_api_headers,
                                 json=json_data)
        resp_json = response.json()
        print(resp_json)
        self.s.answer = resp_json['choices'][0]['message']['content']
        _logger.debug(f'llm_answer: {self.s.answer}')

    def answer_one_api(self):
        self.prepare_one_api()
        self.call_one_api()
        pass

    def main(self):
        self.answer_one_api()
        pass


if __name__ == '__main__':
    qq = {
        "question": """Introduce yourself for a bit ;)""",
        "model_name": "gpt_35_turbo"

    }
    AnswerByOneAPI(qq).main()
    pass
