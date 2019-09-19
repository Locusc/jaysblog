# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 @Time    : 2019/9/18 10:00
 @Author  : Jay Chen
 @FileName: manager.py
 @GitHub  : https://github.com/cRiii
"""

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from jaysblog import create_app
from jaysblog import db

"""
   数据库迁移文件 
        修改数据库映射模型后都会先drop掉以前的表然后调用db.create_all()重新映射
        flask_migrate可以将修改后的模型重新映射到数据库中
        相关命令:
            1.python manage.py mysql init  :初始化一个迁移脚本的环境，只需要执行一次
            2.python manage.py mysql migrate :将模型生成迁移文件，只要模型改变就需要执行
            3.python manage.py mysql upgrade :把前一文件真正的映射到数据库中，每次运行了migrate就需要执行该命令 
"""
# 选择配置模式 生产环境/开发环境
app = create_app('development')
# 命令行方式启动项目  manager接管项目
manager = Manager(app)
# flask对象创建的数据表进行建表和迁移绑定
Migrate(app, db)
# 数据库建表和迁移提供命令行标识符
manager.add_command('mysql', MigrateCommand)

if __name__ == '__main__':
    manager.run()