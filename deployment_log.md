1. python 版本 3.7.5
2. 数据库安装在data目录下


配置Python环境
1. 安装pyenv
https://www.jianshu.com/p/6d387f46cdc8

2. 下载Python，以v=3.7.5为例
v=3.7.5;wget http://npm.taobao.org/mirrors/python/$v/Python-$v.tar.xz -P ~/.pyenv/cache/;pyenv install $v

3. 配置Python环境
pyenv global 3.7.5 


挂载硬盘操作
sudo mkfs -t ext4 /dev/vdb
sudo mount /dev/vdb /data
https://www.cnblogs.com/lemon-flm/p/7597403.html