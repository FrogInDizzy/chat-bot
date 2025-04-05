
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from views.msg_process_view import router as vsb_router2


# from starlette.staticfiles import StaticFiles
# from starlette.templating import Jinja2Templates


def create_app():
    app = FastAPI()
    app.include_router(router=vsb_router2)  # 将路由注册到app中

    # app_relevant.mount("/static", StaticFiles(directory="static"), name="static")  # 设置静态文件目录
    # templates = Jinja2Templates(directory="templates")  # 设置JinJa模板文件位置
    origins = [  # 允许跨域访问的域名或者主机的列表，注意这里不允许使用通配符
        "*",  # 末尾不要带/
    ]
    app.add_middleware(
        CORSMiddleware,  # 跨域的中间件
        allow_origins=origins,  # 允许跨域的网址列表
        allow_credentials=True,  # 允许跨域的 https
        allow_methods=["*", ],  # 允许跨域的方法
        allow_headers=["*"],  # 允许跨域的请求头信息
    )
    return app
