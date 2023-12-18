import re

def is_email(input_str):
    # 定義電子郵件地址的正規表達式
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(email_pattern, input_str) is not None
def is_phone_number(input_str):
    # 定義電話號碼的正規表達式
    phone_pattern = r'\b\d{4}[-.\s]?\d{3}[-.\s]?\d{3}\b'
    
    # 移除字串中的空格，只保留數字和可能的分隔符
    cleaned_input = re.sub(r'[^\d.-]', '', input_str)
    # 檢測是否符合正規表達式
    return re.match(phone_pattern, cleaned_input) is not None

# 測試
print(is_email("a0909.956502@hotmail.com"))
