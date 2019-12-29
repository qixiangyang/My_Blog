
### 数据库情况
服务器：腾讯云
配置：2核4G 50+50g硬盘
系统Centos 7.6


### 配置Python环境

Python版本：3.7.2  

本来想选择最新的Python 3.8 但是考虑到刚出来，不太稳定，所以选择了的最新的3.7.5，后来又选择了3.7.2，具体原因，见下文。

1. 安装pyenv
https://www.jianshu.com/p/6d387f46cdc8

2. 下载Python，以v=3.7.5为例
~~~
v=3.7.5;wget http://npm.taobao.org/mirrors/python/$v/Python-$v.tar.xz -P ~/.pyenv/cache/;pyenv install $v  
v=3.7.2;wget http://npm.taobao.org/mirrors/python/$v/Python-$v.tar.xz -P ~/.pyenv/cache/;pyenv install $v  
~~~

3. 配置Python环境
pyenv global 3.7.5 


### 挂载硬盘
sudo mkfs -t ext4 /dev/vdb  
sudo mount /dev/vdb /data  

详细请参考
https://www.cnblogs.com/lemon-flm/p/7597403.html


### 数据库安装  

#### Redis  
按照官方教程即可

#### PostgreSQL  

数据库版本
PostgreSQL 12  

##### 安装
按照按照官方教程  
https://www.postgresql.org/download/linux/redhat/

##### 配置  

数据库链接配置
配置需要注意，由于要远程连接数据库，所以需要额外改配置
修改配置前务必注意，需要提前备份配置文件

vi /var/lib/pgsql/12/data/pg_hba.conf
vi /var/lib/pgsql/12/data/postgresql.conf

具体参数请参考：
https://cloud.tencent.com/developer/article/1005191  
https://segmentfault.com/a/1190000018812714

postgresql常用命令  
systemctl enable postgresql-12  
systemctl start postgresql-12  # 重启  
systemctl restart postgresql-12  

修改数据库密码  
ALTER USER postgres WITH PASSWORD '12345678';  

遇到一个坑，Navicats中看不到PostgreSQL的表信息  
Navicat的坑，似乎是一个bug，升级到最新版，正常  


##### mysql

### virtualenv 部署
最开始部署的python 版本是3.7.5，在创建virtualenv环境时，报错  
~~~
setuptools pip wheel failed with error code 1
~~~
经查询，无好的解决方案，遂选择给Python降级，选择自己开发常用的3.7.2  
然后再创建虚拟环境，报错  
~~~
ModuleNotFoundError: No module named '_ctypes'
~~~
执行：yum install libffi-devel -y  
再次创建虚拟环境，成功  

### nginx 配置

https://qizhanming.com/blog/2018/08/06/how-to-install-nginx-on-centos-7  

设置开机启动  
sudo systemctl enable nginx  
启动服务  
sudo systemctl start nginx  
关闭服务  
sudo systemctl stop nginx  
停止服务  
sudo systemctl restart nginx  
重新加载，因为一般重新配置之后，不希望重启服务，这时可以使用重新加载。  
sudo systemctl reload nginx  
检查服务状态  
systemctl status nginx.service
查看 Nginx配置位置
locate nginx.conf



### gunicorn 配置

gunicorn -w2 -b0.0.0.0:5000 blog_start:app
gunicorn 无法正确获取环境变量，需要在启动时为其设置环境变量，如下：
gunicorn -w4 -b 0.0.0.0:5000 --env FLASK_ENV=production blog_start:app
在supervisor也要这样设置
参见：http://docs.gunicorn.org/en/stable/settings.html

### supervisor 配置

~~~
[program:blog_start]
https://www.jianshu.com/p/be9dd421fb8d

command=/data/Blog_App/app_venv/bin/gunicorn -w4 -b 0.0.0.0:5000 --env FLASK_ENV=production blog_start:app    ; supervisor启动命令
directory=/data/Blog_App                                                 ; 项目的文件夹路径
startsecs=0                                                                             ; 启动时间
stopwaitsecs=0                                                                          ; 终止等待时间
autostart=false                                                                         ; 是否自动启动
autorestart=false                                                                      ; 是否自动重启
stdout_logfile=/data/Blog_App/log/gunicorn.log                           ; log 日志
stderr_logfile=/data/Blog_App/log/gunicorn.err
~~~

supervisor常用命令
supervisord -c supervisor.conf                             通过配置文件启动supervisor
supervisorctl -c supervisor.conf status                    察看supervisor的状态
supervisorctl -c supervisor.conf reload                    重新载入 配置文件
supervisorctl -c supervisor.conf start [all]|[appname]     启动指定/所有 supervisor管理的程序进程
supervisorctl -c supervisor.conf stop [all]|[appname]      关闭指定/所有 supervisor管理的程序进程


### GitHub拉取最新代码  

git init  
git remote add origin https://github.com/qixiangyang/My_Blog.git  
git pull origin master # 拿到全部源码  
pip install -r requirements.txt
