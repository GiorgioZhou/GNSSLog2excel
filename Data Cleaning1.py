import pandas as pd
import re
import os

# 定义NMEA GSV数据的正则表达式
gsv_pattern = re.compile(
    r"NMEA,\$(?P<system>[A-Z]{2}GSV),(?P<total_msgs>\d+),(?P<msg_num>\d+),(?P<num_sats>\d+),"
    r"(?P<data>.+?),\d+\*[0-9A-F]{2},(?P<timestamp>\d+)"
)



# 解析卫星数据的正则表达式（每组数据四个值：PRN, Elevation, Azimuth, SNR）
satellite_pattern = re.compile(r"(\d+),(\d*),(\d*),(\d*)")

# 读取NMEA数据文件
input_file = r"E:\3087 Mobile Technology\Coursework\building\\gnss_log_2025_03_09_13_43_43.nmea"  # 请替换为实际文件路径
output_file = os.path.splitext(input_file)[0] + ".csv"  # 生成与NMEA相同路径和文件名的CSV文件

# 存储解析后的数据
satellite_data = []

if not os.path.exists(input_file):
    print(f"错误：文件 {input_file} 不存在，请检查路径是否正确。")
    exit()

with open(input_file, "r") as file:
    nmea_sentences = file.readlines()

# 解析数据
for line in nmea_sentences:
    match = gsv_pattern.match(line.strip())
    if match:
        system = match.group("system")
        total_msgs = int(match.group("total_msgs"))
        msg_num = int(match.group("msg_num"))
        num_sats = int(match.group("num_sats"))
        timestamp = match.group("timestamp")

        # 提取卫星数据
        data_part = match.group("data")
        sat_matches = satellite_pattern.findall(data_part)
        
        for sat in sat_matches:
            prn, elevation, azimuth, snr = sat
            satellite_data.append([
                system, total_msgs, msg_num, num_sats, prn,
                elevation if elevation else None,
                azimuth if azimuth else None,
                snr if snr else None,
                timestamp
            ])

# 创建DataFrame
columns = ["System", "Total_Messages", "Message_Number", "Num_Satellites", "PRN", "Elevation", "Azimuth", "SNR", "Timestamp"]
df = pd.DataFrame(satellite_data, columns=columns)

# 保存到CSV
df.to_csv(output_file, index=False)

print(f"数据已处理并保存到 {output_file}")
