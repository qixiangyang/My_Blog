文档创建时间：2019.11.05

V 2.1.2已经上线，基本功能已经完善，还有一些地方需要优化。

1. 页面的布局

   首页：显示完整文章。
   完成 2019.11.05
   
   archives：简化内容展示，改为列表。
   有两种方案：直接为简单的列表，第二种是增加一个预览的表单
   完成 2019.11.05
   
2. 增加博客点击的统计
   总访问量
   各个页面访问量
   记录时间
   记录 ip
   记录 cookie
   记录 user-agent
   完成 2019.11.07

3. 预警邮件
   完成 2019.11.07
    
4. Nginx静态文件配置

   - 配置JS文件目录
   完成：2019.11.11
   
   - 配置图片文件目录
   完成：2019.11.11
   
   遇到的网站访问请求时间过长的问题：
   - 图片请求时间过长
   带宽问题，暂无更好的优化方案
   
   - JS文件请求时间过长，尝试压缩JS
   配置Nginx Gzip设置，加载时间由原来的4s多降低到1s
   完成：2019.11.11

   - 下载CDN上的JS文件过慢，尝试使用下载为本地JS文件
   关闭editor.md的TeX公式支持，即不会再去请求CDN上的js文件
   完成：2019.11.12
    
5. Pyhub点赞按钮
   这个阶段先不做，加入idea池


6. 新增两个数据源
   https://manjusaka.itscoder.com/archives/
   https://www.dongwm.com/
   完成：2019.11.06
   
   
7. 解决的index页第一个markdown解析后面不解析的问题。
   原因：多个div访问一个id似乎只有第一个能拿到，剩下的无法获得这个id对应的js函数
   解决方案：为每一个数据遍历生成一个单独的JS函数
   
   
8. pyhub页内容超出容器范围，造成内容溢出
   通过定义CSS样式，增加了一个滚动条，暂时解决了这个问题，但是不美观，后续还需要继续调整
   完成：2019.11.12