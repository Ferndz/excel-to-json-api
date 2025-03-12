from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
import io
import json
import datetime
import requests
import traceback
import urllib.parse
from pydantic import BaseModel

# 创建 JSON 编码器处理日期和时间以及特殊浮点数值
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return obj.isoformat()
        elif isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            if np.isnan(obj) or np.isinf(obj):
                return None
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(CustomJSONEncoder, self).default(obj)

# 用于URL转换请求的数据模型
class URLRequest(BaseModel):
    file_url: str

app = FastAPI(title="Excel 转 JSON API")

def is_excel_url(url):
    """
    检查URL是否指向Excel文件，兼容包含查询参数的URL
    """
    # 解析URL
    parsed_url = urllib.parse.urlparse(url)
    # 获取路径部分
    path = parsed_url.path
    # 检查路径是否以.xlsx或.xls结尾
    return path.lower().endswith(('.xlsx', '.xls'))

@app.get("/")
async def read_root():
    return {"message": "欢迎使用 Excel 转 JSON API"}

@app.post("/convert/")
async def convert_excel_to_json(file: UploadFile = File(...)):
    """
    上传 Excel 文件并将其转换为 JSON 格式
    """
    # 检查文件类型
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="请上传 Excel 文件 (.xlsx 或 .xls)")
    
    try:
        # 读取上传的文件内容
        contents = await file.read()
        
        # 使用 pandas 读取 Excel 数据
        df = pd.read_excel(io.BytesIO(contents))
        
        # 替换 NaN 值为 None（null in JSON）
        df = df.replace({np.nan: None})
        
        # 转换为 JSON 格式
        result = df.to_dict(orient='records')
        
        # 使用自定义 JSON 编码器处理日期和时间以及特殊浮点数值
        json_compatible_data = json.loads(
            json.dumps(result, ensure_ascii=False, cls=CustomJSONEncoder)
        )
        
        return JSONResponse(content=json_compatible_data)
    
    except Exception as e:
        error_details = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"转换失败: {str(e)}\n详细信息: {error_details}")

@app.post("/convert-from-url/")
async def convert_excel_from_url(request: URLRequest):
    """
    通过URL获取Excel文件并将其转换为JSON格式
    """
    file_url = request.file_url
    
    # 验证URL格式
    if not file_url.startswith(('http://', 'https://')):
        raise HTTPException(status_code=400, detail="无效的URL格式，必须以http://或https://开头")
    
    # 检查URL是否指向Excel文件
    if not is_excel_url(file_url):
        raise HTTPException(status_code=400, detail="URL必须指向Excel文件 (.xlsx 或 .xls)，请检查URL路径部分")
    
    try:
        # 从URL下载文件
        print(f"正在下载文件: {file_url}")
        response = requests.get(file_url, timeout=30)
        
        # 检查响应状态
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"无法从URL下载文件: HTTP {response.status_code} - {response.reason}")
        
        content_type = response.headers.get('Content-Type', '')
        print(f"文件类型: {content_type}")
        print(f"文件大小: {len(response.content)} 字节")
        
        # 使用pandas读取Excel数据
        try:
            df = pd.read_excel(io.BytesIO(response.content))
            print(f"成功读取Excel文件，行数: {len(df)}, 列数: {len(df.columns)}")
        except Exception as e:
            error_details = traceback.format_exc()
            raise HTTPException(status_code=500, detail=f"无法解析Excel文件: {str(e)}\n详细信息: {error_details}")
        
        # 替换NaN值为None（null in JSON）
        df = df.replace({np.nan: None})
        
        # 转换为JSON格式
        result = df.to_dict(orient='records')
        
        # 使用自定义JSON编码器处理日期、时间和特殊浮点数值
        json_compatible_data = json.loads(
            json.dumps(result, ensure_ascii=False, cls=CustomJSONEncoder)
        )
        
        return JSONResponse(content=json_compatible_data)
    
    except Exception as e:
        error_details = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"转换失败: {str(e)}\n详细信息: {error_details}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
