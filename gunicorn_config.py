from gunicorn import glogging

# 日志格式说明
"""
asctime	%(asctime)s	日志事件发生的时间--人类可读时间，如：2003-07-08 16:49:45,896
created	%(created)f	日志事件发生的时间--时间戳，就是当时调用time.time()函数返回的值
relativeCreated	%(relativeCreated)d	日志事件发生的时间相对于logging模块加载时间的相对毫秒数（目前还不知道干嘛用的）
msecs	%(msecs)d	日志事件发生事件的毫秒部分
levelname	%(levelname)s	该日志记录的文字形式的日志级别（'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'）
levelno	%(levelno)s	该日志记录的数字形式的日志级别（10, 20, 30, 40, 50）
name	%(name)s	所使用的日志器名称，默认是'root'，因为默认使用的是 rootLogger
message	%(message)s	日志记录的文本内容，通过 msg % args计算得到的
pathname	%(pathname)s	调用日志记录函数的源码文件的全路径
filename	%(filename)s	pathname的文件名部分，包含文件后缀
module	%(module)s	filename的名称部分，不包含后缀
lineno	%(lineno)d	调用日志记录函数的源代码所在的行号
funcName	%(funcName)s	调用日志记录函数的函数名
process	%(process)d	进程ID
processName	%(processName)s	进程名称，Python 3.1新增
thread	%(thread)d	线程ID
threadName	%(thread)s	线程名称
"""
glogging.Logger.error_fmt = '{' \
                            '"time": "%(asctime)s", ' \
                            '"log_level": "%(levelname)s", ' \
                            '"pathname": "%(pathname)s", ' \
                            '"filename": "%(filename)s", ' \
                            '"lineno": "%(lineno)s", ' \
                            '"module_name":"%(module)s",  ' \
                            '"method": "%(funcName)s",  ' \
                            '"process_id":%(process)d,  ' \
                            '"thread_id":%(thread)d,  ' \
                            '"message": "%(message)s"' \
                            '}'
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