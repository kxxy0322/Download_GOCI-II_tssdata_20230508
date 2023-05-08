import requests
import os
import time
import random
from datetime import datetime, timedelta

# 设置开始和结束时间
start_date = datetime(2022, 10, 30)
end_date = datetime(2022, 12, 31)

url_prefix = "https://nosc.go.kr/opendap/GOCI-II/"
url_middle = "/L2/GK2_GC2_L2_"
url_suffix1 = "1530/GK2B_GOCI2_L2_{}"
url_suffix2 = "_{}1530_LA_S010_TSS.nc"
path = 'D:/GOCI2'  # 下载文件保存的目录
delay_time = random.uniform(7, 14)
hour_list = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "23"]

current_date = start_date  # 当前需要下载的文件的日期

while current_date < end_date:  # 循环遍历下载起始日期到下载结束日期范围内的每一天

    year = str(current_date.year)
    month = str(current_date.month).zfill(2)
    day = str(current_date.day).zfill(2)

    for hour in hour_list:
        url = url_prefix + year + "/" + month + "/" + day + url_middle + year + month + day + "_" + hour + url_suffix1.format(
            year + month + day) + url_suffix2.format(hour)
        print(url)

        # 检查目录是否存在，如果不存在则创建目录
        if not os.path.exists("D:/GOCI2"):
            os.makedirs("D:/GOCI2")

        try:
            response = requests.get(url)
            # 如果下载的文件小于1MB，则跳过该文件，下载下一个
            if len(response.content) < 1024 * 1024:
                print(f"文件 {url} 小于 1MB，跳过下载。")
                continue

            with open(os.path.join(path, f"GK2B_GOCI2_L2_{year}{month}{day}_{hour}1530_LA_S010_TSS.nc"), "wb") as f:
                f.write(response.content)

        except Exception as e:  # 捕获异常并输出错误信息
            print(f"文件 {url} 下载失败，错误信息为：{str(e)}")
            continue

        # 延迟一段时间，避免请求过于频繁导致被封禁IP
        time.sleep(delay_time)

    # 判断是否为当前月份的最后一天，如果是则将日期加上一个月
    current_date += timedelta(days=1)  # 日期加上一天，继续下载下一天的文件
