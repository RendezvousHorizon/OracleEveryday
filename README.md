# OracleEveryday
Course project of EE458 Software Engineering Spring 2021.

### 1. 服务端运行方式
```
git clone https://github.com/RendezvousHorizon/OracleEveryday.git
cd flask-server

将甲骨文图片压缩包解压到oracle-images文件夹中
<<cmd to do this>>

# 创建一个虚拟环境（可做可不做）
conda create -n web python=3.8
conda activate web

# 安装所需软件包
pip install -r requirements.txt

# 第一次运行时需要初始化一下数据库
flask init-db

# 运行
waitress-serve --port=5000 --call flaskr:create_app
```