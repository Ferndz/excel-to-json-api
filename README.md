# Excel 转 JSON API

这是一个简单的 API 服务，用于将 Excel 文件转换为 JSON 格式。

## 功能

- 上传 Excel 文件 (.xlsx 或 .xls)
- 将 Excel 数据转换为 JSON 格式
- 通过 API 返回 JSON 数据

## 安装

1. 克隆此仓库
2. 安装依赖项：
   ```
   pip install -r requirements.txt
   ```

## 使用方法

1. 启动服务器：
   ```
   uvicorn app.main:app --reload
   ```

2. 访问 API 文档：
   - 在浏览器中打开 http://localhost:8000/docs

3. 使用 API：
   - 通过 POST 请求上传 Excel 文件到 `/convert/` 端点
   - 接收 JSON 格式的响应

## API 端点

- `GET /`: 检查 API 是否正常运行
- `POST /convert/`: 上传 Excel 文件并转换为 JSON

## 示例

使用 curl 命令行工具：
```
curl -X POST "http://localhost:8000/convert/" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@your_excel_file.xlsx"
```
