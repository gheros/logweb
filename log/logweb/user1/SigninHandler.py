class SigninHandler(BaseHandler):  # 引入BaseHandler
    import MySQLdb
    def post(self):  # HTTP的POST方法，是GET渲染的form中的post method所对应
        username = self.get_argument('username')  # 获取form中username的值
        password = self.get_argument('password')  # 获取form中password的值
        conn = MySQLdb.connect('localhost', user='root', passwd='', db='datacenter', charset='utf8',
                               cursorclass=MySQLdb.cursors.DictCursor)  # 连接数据库，指定cursorclass的目的是要让返回结果以字典的形式呈现，如果不写，是以元组形式返回
        cursor = conn.cursor()  # 定义数据库指针

        sql = 'SELECT * FROM dc_users WHERE username=%s AND password=password(%s)'  # 写sql，为何这样写后面再说
        cursor.execute(sql, (username, password,))  # 执行SQL
        row = cursor.fetchone()  # 获取一条，返回值为dict,因为前面连接数据库时定义了cursorclass = MySQLdb.cursors.DictCursor，当然，你需要import MySQLdb.cursors的包
        if row:  # 如果存在记录
            self.set_secure_cookie('id', str(row['id']).encode('unicode_escape'),
                                   expires_days=None)  # 设置安全cookie，防止xsrf跨域
            self.set_secure_cookie('username', row['username'].encode('unicode_escape'), expires_days=None)  # same
            self.set_secure_cookie('role', row['role'].encode('unicode_escape'), expires_days=None)  # same
            ip = self.request.remote_ip  # 获取来访者IP
            sql = 'UPDATE dc_users SET last_access = NOW(), last_ip=%s WHERE id = %s'  # 认证审计变更的SQL
            cursor.execute(sql, (ip, row['id'],))  # 执行SQL
            conn.commit()  # 提交执行
            cursor.close()  # 关闭指针
            conn.close()  # 关闭数据库连接
            self.redirect('/')  # 转入首页
            return  # 返回，按照官方文档的要求，在redirect之后需要写空的return，否则可能会有问题，实测确实会有问题
        else:  # 如果不存在记录
            self.redirect('/Signin')  # 跳转回登录页面
            return

    def get(self):  # HTTP GET方式
        self.render('users/login_form.html')  # 渲染登录框HTML