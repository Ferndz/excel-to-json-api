from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import io
import json
import datetime

# 创建 JSON 编码器处理日期和时间
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)

app = FastAPI(title="Excel 转 JSON API")

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
        
        # 转换为 JSON 格式
        result = df.to_dict(orient='records')
        
        # 使用自定义 JSON 编码器处理日期和时间
        json_compatible_data = json.loads(
            json.dumps(result, ensure_ascii=False, cls=DateTimeEncoder)
        )
        
        return JSONResponse(content=json_compatible_data)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"转换失败: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
