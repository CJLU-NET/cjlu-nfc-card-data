# 计量饭卡

## 数据分析

共计 16 扇区、64 区块（每扇区 4 区块）、1024 字节（每区块 16 字节）

```python
card_no = data[0:4] # 卡号

stu_no = data[960:970].decode('utf-8') # 学号（15扇区60块）
# 当然 5 扇区 22 块也存储了学号信息

money = int.from_bytes(data[64:66], byteorder='little') / 100
# 余额小端存储

""" 1 扇区数据格式（4、5 区块一致，首位为余额，其余不清楚）
XX XX 00 XX 03 XX 00 XX 30 XX 03 00 XX XX XX XX
XX XX 00 XX 03 XX 00 XX 30 XX 03 00 XX XX XX XX
XX XX 00 00 00 00 00 00 00 00 00 00 00 00 00 00
"""

is_locked = data[24] # 0 为异常、1 为正常，可能是圈存时问题？如果出现刷卡时显示无效卡，可尝试修改一下写入。


```