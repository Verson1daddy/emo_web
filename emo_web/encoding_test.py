import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding']

file_path = './.env'  # 替换为实际的文件路径
encoding = detect_encoding(file_path)
print(f"文件编码格式为: {encoding}")