import requests
import json
import os

def convert_excel_to_json(excel_file_path, api_url="https://ferndz.pythonanywhere.com/convert/"):
    """
    通过 API 将 Excel 文件转换为 JSON
    
    参数:
        excel_file_path: Excel 文件的路径
        api_url: API 的 URL
        
    返回:
        成功时返回 JSON 数据，失败时返回 None
    """
    # 检查文件是否存在
    if not os.path.exists(excel_file_path):
        print(f"错误: 文件 '{excel_file_path}' 不存在")
        return None
        
    # 检查文件类型
    if not excel_file_path.endswith(('.xlsx', '.xls')):
        print("错误: 请提供 Excel 文件 (.xlsx 或 .xls)")
        return None
    
    try:
        # 构建表单数据
        files = {
            'file': (os.path.basename(excel_file_path), open(excel_file_path, 'rb'), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        }
        
        # 发送请求到 API
        print(f"正在发送请求到 API: {api_url}")
        response = requests.post(api_url, files=files)
        
        # 检查响应状态
        if response.status_code == 200:
            # 解析 JSON 响应
            result = response.json()
            
            # 保存 JSON 文件 (可选)
            output_dir = os.path.dirname(excel_file_path)
            base_name = os.path.splitext(os.path.basename(excel_file_path))[0]
            output_file = os.path.join(output_dir, f"{base_name}.json")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            print(f"转换成功! JSON 文件已保存到: {output_file}")
            return result
        else:
            print(f"API 错误: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"请求失败: {str(e)}")
        return None

def convert_excel_from_url(excel_url, api_url="https://ferndz.pythonanywhere.com/convert-from-url/", save_path=None):
    """
    通过URL和API将Excel文件转换为JSON
    
    参数:
        excel_url: Excel文件的URL地址
        api_url: API的URL
        save_path: 保存JSON文件的路径（可选）
        
    返回:
        成功时返回JSON数据，失败时返回None
    """
    # 检查URL格式
    if not excel_url.startswith(('http://', 'https://')):
        print("错误: 无效的URL格式，必须以http://或https://开头")
        return None
        
    # 检查URL是否指向Excel文件
    if not excel_url.lower().endswith(('.xlsx', '.xls')):
        print("错误: URL必须指向Excel文件 (.xlsx 或 .xls)")
        return None
    
    try:
        # 构建请求数据
        data = {
            "file_url": excel_url
        }
        
        # 发送请求到API
        print(f"正在发送请求到API: {api_url}")
        response = requests.post(api_url, json=data)
        
        # 检查响应状态
        if response.status_code == 200:
            # 解析JSON响应
            result = response.json()
            
            # 保存JSON文件（如果提供了保存路径）
            if save_path:
                # 确保目录存在
                save_dir = os.path.dirname(save_path)
                if save_dir and not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                    
                with open(save_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                
                print(f"转换成功! JSON文件已保存到: {save_path}")
            else:
                print("转换成功!")
                
            return result
        else:
            print(f"API错误: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"请求失败: {str(e)}")
        return None

if __name__ == "__main__":
    # 使用示例1：上传本地Excel文件
    print("===== 示例1：上传本地Excel文件 =====")
    excel_file = "C:\\Users\\Run\\Desktop\\徐润\\2025\\录制句数统计\\【句数统计】G126-2025年2月.xlsx"
    result1 = convert_excel_to_json(excel_file)
    
    if result1:
        print(f"共转换了 {len(result1)} 条记录")
    
    # 使用示例2：通过URL转换Excel文件
    print("\n===== 示例2：通过URL转换Excel文件 =====")
    # 使用一个公开可访问的Excel文件URL（示例）
    excel_url = "https://file-examples.com/wp-content/storage/2017/02/file_example_XLSX_10.xlsx"
    result2 = convert_excel_from_url(
        excel_url, 
        api_url="http://localhost:8000/convert-from-url/",
        save_path="downloaded_excel.json"
    )
    
    if result2:
        print(f"共转换了 {len(result2)} 条记录") 