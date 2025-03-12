import pandas as pd
import json
import os
import sys
import datetime

# 创建 JSON 编码器处理日期和时间
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)

def convert_excel_to_json(excel_file_path):
    """
    将指定的 Excel 文件转换为 JSON 并保存到相同目录
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(excel_file_path):
            print(f"错误: 文件 '{excel_file_path}' 不存在")
            return False
            
        # 检查文件类型
        if not excel_file_path.endswith(('.xlsx', '.xls')):
            print("错误: 请提供 Excel 文件 (.xlsx 或 .xls)")
            return False
        
        # 使用 pandas 读取 Excel 数据
        print(f"正在读取 Excel 文件: {excel_file_path}")
        df = pd.read_excel(excel_file_path)
        
        # 转换为 JSON 格式
        result = df.to_dict(orient='records')
        
        # 确定输出文件路径 (与输入文件相同目录)
        output_dir = os.path.dirname(excel_file_path)
        base_name = os.path.splitext(os.path.basename(excel_file_path))[0]
        output_file = os.path.join(output_dir, f"{base_name}.json")
        
        # 保存 JSON 文件，使用自定义编码器处理日期和时间
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2, cls=DateTimeEncoder)
        
        print(f"转换成功! JSON 文件已保存到: {output_file}")
        return True
        
    except Exception as e:
        print(f"转换失败: {str(e)}")
        return False

if __name__ == "__main__":
    # 检查是否提供了文件路径
    if len(sys.argv) < 2:
        print("请提供 Excel 文件路径")
        print("用法: python convert_file.py <excel文件路径>")
        sys.exit(1)
    
    # 获取文件路径
    excel_file_path = sys.argv[1]
    
    # 执行转换
    if convert_excel_to_json(excel_file_path):
        sys.exit(0)
    else:
        sys.exit(1)
