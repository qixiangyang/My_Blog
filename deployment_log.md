1. python 版本 3.7.5
2. 数据库安装在data目录下

### 数据库情况
服务器：腾讯云
配置：2核4G 50+50g硬盘
系统Centos 7.6


### 配置Python环境
1. 安装pyenv
https://www.jianshu.com/p/6d387f46cdc8

2. 下载Python，以v=3.7.5为例
v=3.7.5;wget http://npm.taobao.org/mirrors/python/$v/Python-$v.tar.xz -P ~/.pyenv/cache/;pyenv install $v
v=3.7.2;wget http://npm.taobao.org/mirrors/python/$v/Python-$v.tar.xz -P ~/.pyenv/cache/;pyenv install $v

3. 配置Python环境
pyenv global 3.7.5 


### 挂载硬盘
sudo mkfs -t ext4 /dev/vdb
sudo mount /dev/vdb /data


https://www.cnblogs.com/lemon-flm/p/7597403.html


### 数据库安装

#### Redis
按照官方教程即可

#### PostgreSQL

##### 安装
按照按照官方教程
https://www.postgresql.org/download/linux/redhat/

##### 配置

<br>链接配置
配置需要注意，由于要远程连接，所以需要额外改配置
修改配置前务必注意，需要提前备份配置文件

vi /var/lib/pgsql/12/data/pg_hba.conf
vi /var/lib/pgsql/12/data/postgresql.conf

systemctl enable postgresql-12
systemctl start postgresql-12  # 重启
systemctl restart postgresql-12

<br>权限配置
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




