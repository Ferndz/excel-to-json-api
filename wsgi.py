import sys
import os

# 添加项目目录到路径
path = '/home/ferndz/excel-to-json-api'
if path not in sys.path:
    sys.path.append(path)

# 导入 FastAPI 应用
from fastapi import FastAPI
from app.main import app

# FastAPI 应用需要特殊处理
from fastapi.middleware.wsgi import WSGIMiddleware
application = WSGIMiddleware(app)

if __name__ == "__main__":
    app.run() 