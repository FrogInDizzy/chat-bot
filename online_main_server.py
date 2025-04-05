import os
import sys

import uvicorn

from public_library.utils.pc_op import fetch_computer_name_address

P_PATH = os.path.dirname(os.path.realpath(__file__))
if P_PATH not in sys.path:
    sys.path.append(P_PATH)
import setting
from config.fetch_config_by_ip import gcpi

from views.app_start_view import create_app

port = gcpi.port
# workers = 2
workers = gcpi.workers
DEBUG = True

app = create_app()  # 创建fastapi 服务

if __name__ == '__main__':
    if DEBUG:
        import colorama

        color = colorama.Fore.CYAN
        print(color + "PRINT ALL ROUTERS")
        for x in app.routes:
            print(color + getattr(x, "path"))
        print(color + "END PRINT ALL ROUTERS")

    pc_name, pc_ip = fetch_computer_name_address()
    api_doc_url = f'http://{pc_ip}:{port}/docs'
    print(f'接口文档位于:\n {api_doc_url}')
    # 启动fastapi 服务
    uvicorn.run(app="online_main_server:app", port=port,
                host="0.0.0.0",
                workers=workers,
                reload=False,
                # reload=True,
                log_level="info")
