## UTC_fastapi项目

### ① 项目介绍

项目使用fastapi框架，为UTC提供API调用服务




### ② 目录结构

```
utc_fastapi
*├── config 配置文件目录
 ├── data   数据文件目录  
*├── src    项目代码目录
   *├── api               接口函数目录
   *├── conf              配置变量目录
   *├── crontab           定时任务目录
    ├── exception         自定义异常目录
    ├── schema            序列化/字段校验/接口文档目录
   *├── service           业务代码目录
   *├── utils             工具代码目录
 ├── test       离线测试脚本目录
 
 # 带*号为必要目录
```



### ③ 项目运行

Docker环境运行：需安装Docker

```shell
# 1. 基于Dockerfile，项目根目录运行，构建镜像
docker build . -t [app_name]:[tag]

# 2. 解释器选择构建好的镜像，配置好启动参数(Docker项目目录、本地端口映射等)

# 3. 启动项目：(或进入app.py中右键运行)
python3 src/app.py
```



虚拟环境运行：

```shell
# 1. 新建虚拟环境venv，激活venv，安装依赖：
pip3 install -r requirements.txt

# 2. 启动项目：
python3 src/app.py
```



### ④ 接口文档

项目接口文档地址：

http://0.0.0.0:4568/apidocs
