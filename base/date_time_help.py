from datetime import datetime
from zoneinfo import ZoneInfo # 注意导入方式


def get_timestamp(time_str = "2025/8/6 8:29:02"):
    # 1. 定义原始时间字符串和它的格式
    # time_str = "2025/8/6 8:29:02"
    format_str = "%Y/%m/%d %H:%M:%S"

    # 2. 解析字符串为 naive datetime 对象
    local_naive_dt = datetime.strptime(time_str, format_str)
    # print(f"1. 解析后的本地时间 (无时区信息): {local_naive_dt}")
    #

    # 3. 为 naive datetime 对象添加时区信息
    #    zoneinfo 可以直接在 replace 方法中使用
    local_tz = ZoneInfo('Asia/Shanghai')
    local_aware_dt = local_naive_dt.replace(tzinfo=local_tz)
    # print(f"2. 添加时区后的本地时间: {local_aware_dt}")

    # 4. 将带时区的本地时间转换为 UTC 时间
    #    同样，UTC 也可以直接通过 ZoneInfo 获取
    utc_dt = local_aware_dt.astimezone(ZoneInfo('UTC'))
    # print(f"3. 转换后的 UTC (格林尼治) 时间: {utc_dt}")

    # # 5. (可选) 格式化为你想要的字符串格式
    # utc_time_str = utc_dt.strftime(format_str)
    # print(f"4. 格式化后的 UTC 时间字符串: {utc_time_str}")

    timestamp = utc_dt.timestamp()
    print(f"{timestamp}")
    return timestamp
if __name__ == "__main__":
    timestamp = get_timestamp("2025/8/6 8:29:02")
