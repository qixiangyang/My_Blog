文档创建时间：2019.11.08

1. 搜索栏目施工
   挪到下一期

2. 搜索结果页面
   挪到下一期

3. 定时任务
   定时任务不执行原因，crontab不能正确读取当前账号的环境变量，参见：
   https://blog.csdn.net/weixin_36343850/article/details/79217611
   https://stackoverflow.com/questions/2229825/where-can-i-set-environment-variables-that-crontab-will-use
   完成 2019.11.15

4. 订阅邮件 一周更新一次

5. 登陆过期
   现在内容页编辑登陆后，无过期自动注销，有一定的安全风险。
   https://stackoverflow.com/questions/2229825/where-can-i-set-environment-variables-that-crontab-will-use
   完成：2019.11.15

6. BUG：在内容页跳转到文章页时，跳转到带端口号的网址上
   Nginx没有对redirect进行限制，导致直接跳转到gunicorn服务上
   解决方案：google 关键词：flask nginx 重定向：
   https://www.jianshu.com/p/390f8946120a
   完成： 2019.11.14

7. 更新两个数据源
   完成： 2019.11.13
   
8. 调整Pyhub内容预览展示的样式
   现在格式还有很大问题。直接带标签的内容导致显示的格式非常混乱，需要再优化。
   frostming
   完成： 2019.11.14
   重写了所有的preview字段
   完成： 2019.11.15


10 jinja2代码格式混乱
   https://stackoverflow.com/questions/21991479/jinja2-correctly-indent-included-block
   可以设置代码缩进
   
  
全部完成 2019.11.26