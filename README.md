# view-oj-backend
此项目是view-oj的后端项目(ZUCC-ACM-LAB)

前端项目地址: https://github.com/KeadinZhou/view-oj-web

接口文档: https://www.showdoc.cc/417895562132382

# 安装
```bash
# cd到安装目录
cd /your-work-dir

# clone项目
git clone https://github.com/taoting1234/view-oj-backend

# 进入程序目录
cd view-oj-backend

# 创建虚拟环境
virtualenv venv

# 进入虚拟环境
source venv/bin/activate

# 安装依赖
pip install requirements.txt
```
# 运行

## 直接运行(仅用于测试)
```bash
# 运行web服务器（测试环境）
python app.py

# 运行计划任务worker
celery -A tasks worker -l info -c 8 --pool=eventlet

# 运行计划任务beat
celery -A tasks beat -l info
```

## supervisor守护运行(推荐)
1.安装supervisor

2.修改view-oj.ini文件中的目录

3.将配置文件复制到supervisor目录下的conf.d文件夹下

4.运行supervisor