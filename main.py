import asyncio
import logging
import os
import sys

from tornado.web import Application, RequestHandler, StaticFileHandler

from common.config import getConfig
from controller import systemController, jobController, notifyController
from service.system import onStart


class MainIndex(RequestHandler):
    def get(self):
        self.render(os.path.join(frontendPath, "front/index.html"))


def make_app():
    # 以/svr/noAuth开头的请求无需鉴权，例如登录等
    return Application([
        (r"/svr/noAuth/login", systemController.Login),
        (r"/svr/user", systemController.User),
        (r"/svr/language", systemController.Language),
        (r"/svr/alist", jobController.Alist),
        (r"/svr/job", jobController.Job),
        (r"/svr/notify", notifyController.Notify),
        (r"/", MainIndex),
        (r"/(.*)", StaticFileHandler,
         {"path": os.path.join(frontendPath, "front")})
    ], cookie_secret=server['passwdStr'])


async def main():
    app = make_app()
    logger = logging.getLogger()
    app.listen(server['port'])
    successMsg = f"启动成功_/_Running at http://127.0.0.1:{server['port']}/"
    logger.critical(successMsg)
    await asyncio.Event().wait()


if __name__ == "__main__":
    # 切换到脚本所在目录
    scriptDir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(scriptDir)

    onStart.init()
    cfg = getConfig()
    frontendPath = sys._MEIPASS if getattr(sys, 'frozen', False) else scriptDir
    # 后端配置
    server = cfg['server']
    asyncio.run(main())
