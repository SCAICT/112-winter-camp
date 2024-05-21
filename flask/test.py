import pytz
from datetime import datetime

# 假設有一個已有的時間戳 timestamp
timestamp = 1609459200  # 這裡使用一個示例時間戳

# 將時間戳轉換為 datetime 對象，假設原本是在 UTC 時區
dt_object_utc = datetime.utcfromtimestamp(timestamp)

# 設定所需的目標時區，這裡是 'Asia/Taipei'
desired_timezone = pytz.timezone('Asia/Taipei')

# 使用目標時區設定 datetime 對象
dt_object_with_desired_timezone = dt_object_utc.replace(tzinfo=pytz.utc).astimezone(desired_timezone)

# 將調整後的 datetime 對象轉換回時間戳
adjusted_timestamp = int(dt_object_with_desired_timezone.timestamp())

# 打印結果
print("原始時間戳:", timestamp)
print("目標時區時間:", dt_object_with_desired_timezone)
print("調整後的時間戳:", adjusted_timestamp)
