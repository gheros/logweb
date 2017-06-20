import sys

sys.setdefaultencoding('utf-8')
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.autoreload


class BaseHandler(tornado.web.RequestHandler):  # BaseHandler
    def get_current_user(self):
        user = self.get_secure_cookie('username')
        return user


class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        if not self.current_user:
            self.redirect('/Signin')  # 如未登录，则跳转Signin，Signin的GET方法调用的就是login_form.html页面
            return
        self.render('welcome.html')  # 否则渲染welcome.html


settings = \
    {
        "cookie_secret": "HeavyMetalWillNeverDie",  # Cookie secret
        "xsrf_cookies": True,  # 开启跨域安全
        "gzip": False,  # 关闭gzip输出
        "debug": False,  # 关闭调试模式，其实调试模式是很纠结的一事，我喜欢打开。
        "template_path": os.path.join(os.path.dirname(__file__), "./templates"),
    # 定义模板，也就是login_form.html或header.html相对于本程序所在的位置
        "static_path": os.path.join(os.path.dirname(__file__), "./static"),  # 定义JS, CSS等文件相对于本程序所在的位置
        "login_url": "/Signin",  # 登录URL为/Signin
    }

application = tornado.web.Application([
    (r"/", IndexHandler),  # 路由设置/ 使用IndexHandler
    (r"/signin", SigninHandler)  # Signin使用SigninHandler
], **settings)

if __name__ == "__main__":  # 启动tornado，配置里如果打开debug，则可以使用autoload，属于development模式，如果关闭debug，则不可以使用autoload，属于production模式。autoload的含义是当tornado监测到有任何文件发生变化，不需要重启server即可看到相应的页面变化，否则是修改了东西看不到变化。
    server = tornado.httpserver.HTTPServer(application)
    server.bind(10002)  # 绑定到10002端口
    server.start(0)  # 自动以多进程方式启动Tornado，否则需要手工启动多个进程
    tornado.ioloop.IOLoop.instance().start()