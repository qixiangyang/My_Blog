文档创建时间：2019.09.25

版本 V 1.0

1. 调试 Archives，~~pynews~~PyHub 文章目录的样式

    1. 调整好文章列表的样式
    2. 数据测试最终的效果
    
    完成 时间 2019.10.9
    
2. 前后端交数据的交互
    
    1. 新建数据库, 使用migrate的方式进行数据库的管理
    2. 造假数据，从后端传数据 使用Faker生产假数据
    3. 写页面模板，包含目录页和文章页。
    
    填坑记录 
    1. 需要安装psycopg2 但是安装时报错，需安装psycopg2-binary
    链接：https://github.com/psycopg/psycopg2/issues/890
    
    2. markdown 渲染需要用到Flask-Markdown组件，网上的教程已过期，需要按照官方文档的要求来使用
    链接：https://pythonhosted.org/Flask-Markdown/
    注意：Flask-Markdown渲染的结果不尽如人意，后期通过其他组件在完善
    
    完成 时间 2019.10.10
    
3. 分页
    1. 分页需要与SQLAlchemy连用，因此先需要在数据库中插入相应的数据 完成 2019-10-11
    2. 后端数据库数据与前端数据交互 完成 2019-10-11
    3. 分页组件 完成 2019-10-11
    4. 从文章列表页进入文章详情 完成 2019-10-14
    5. 数据库迁移 完成 2019-10-14


4. ~~Home页开发~~
    1. ~~需要考虑首页展示的内容~~
    2. ~~考虑了一下，做一个首页内容只是现有功能的重复，其实没有必要，不如多花点时间完成其他重要的功能。~~

5. ~~后台的内容管理系统~~
    1. ~~新增文章~~
    2. ~~查看现有的文章，并修改~~
    3. ~~需要权限系统，用户认证通过后才可以新增和修改内容。~~
    4. ~~后台功能同理，现有的内容可以通过手动上传的方式实现，不是必须功能。~~

6. 爬虫
    1. 确定目标网站
    ~~~
    目标网站
    kawabangga
    laike9m
    ~~~

    2. 爬虫撰写 (正常日志与异常日志分开)
    ~~~
    完成两个网站，先进行了部署。
    完成 2019-10-20
    日志还未添加，后期再补充
    ~~~
    3. 内容分类（机器学习）
    4. 定时任务 


7. 测试
    未测试

8. 部署上线
   ~~~
   1. Docker 
   2. Docker + Kubernetes
   最终没有来得及用Docker or Kubernetes这一套。
   决定先行上线了，主要还是想先上线有一个成品，让自己的阶段性的目标完成，接下来再折腾Docker + Kubernetes这一套。
   目前部署的情况
   Nginx + Gunicorn + supervisor
   ~~~
   
  
9. 这个版本目前存在的问题：

    1. 版权问题 
    ~~~
    解决方式：
    网站标示 
    完成 2019-10-22
    发邮件问询
    laixintao 已获授权 2019-10-22
    laike9m 已获授权 2019-10-23
    ~~~
    
    2. 开发模式 CI
    
    ~~~
    需要解决的问题
    1. 读取环境变量配置
        - export FLASK_ENVIRONMENT=production
        - 如果使用虚拟环境，设置环境变量时注意要激活虚拟环境，同时不要给变量值加引号。
    2. 改善包引用的管理
        - 使用FLASK_ENVIRONMENT作为标示环境的环境变量
    完成 2019-10-22
    3. 环境变量失效问题
   
    vim ~/.bashrc
    添加 
    export FLASK_ENVIRONMENT=production
    export FLASK_ENV=production
   
    export FLASK_ENVIRONMENT=development
    export FLASK_ENV=development
    source ~/.bashrc
    unset 删除环境变量
   
    最后是直接vim ~/.bashrc
   
    针对于当前用户生效，具体哪个命令对那种情况生效，请见：
    https://blog.csdn.net/u011630575/article/details/49839893
    完成 2019-10-22
    ~~~
    
    3. 自己文章内容的上传
    ~~~
    完成 2019-10-22
    ~~~
    
    4. 爬虫与etl任务的界限
    ~~~
    对现有的数据流程进行部分修正，增加一层ETL
    爬虫直接入库，目前看数据还会存在一些问题，所以要对数据再次做一下处理
   
    爬虫的类设计，目前在爬虫类中写了大部分的数据格式处理的流程，
    但是随着爬取目标网站的增多，类势必会越来越长，变得难以维护。
    考虑使用在每个爬虫里面将方法重写，降低维护的难度
    
    这个可以先搁置，等到其他问题先解决，部署上线后再解决
    ~~~
    
    5. Pynews栏目的更名
    ~~~
    更改为PyHub
    完成 2019-10-22
    ~~~
    
    6. 给侧边栏添加相应的链接
    完成 2019-10-22
    
    7. 设置定时任务

    
10. 未来功能设想

   1. 搜索功能
   2. 内容评级
   3. 内容聚合

    





