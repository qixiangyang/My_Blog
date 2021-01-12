from gunicorn import glogging
glogging.Logger.error_fmt = "%(asctime)s [%(filename)s:%(lineno)d] [%(funcName)s] " \
                            "[%(levelname)s] [pid: %(process)d thread_id:%(thread)d] - %(message)s"
workers = 3  # 并行工作进程数
threads = 2  # 指定每个工作者的线程数
bind = ['0.0.0.0:5000']  # 监听内网端口5000
worker_connections = 1000  # 设置最大并发量
proc_name = 'my_blog'  # 进程名称
pidfile = '/tmp/blog.pid'  # 设置进程文件目录
timeout = 60  # 超时
max_requests = 6000  # 最大请求数
loglevel = 'info'  # 日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'  # 设置gunicorn访问日志格式，错误日志无法设置
accesslog = "./log/accesslog.log"  # 访问日志文件
errorlog = "./log/errorlog.log"  # 错误日志文件
reload = True
autorestart = True
# preload = True


"""
其每个选项的含义如下：
h          remote address
l          '-'
u          currently '-', may be user name in future releases
t          date of the request
r          status line (e.g. ``GET / HTTP/1.1``)
s          status
b          response length or '-'
f          referer
a          user agent
T          request time in seconds
D          request time in microseconds
L          request time in decimal seconds
p          process ID
"""