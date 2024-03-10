# coding=utf-8
"""
用于读取饭卡的dump文件，解析出卡号、学号、余额等信息，并生成原始卡和中介卡的dump文件
适用于中国计量大学 CJLU 饭卡
仅供学习交流使用，禁止用于非法用途
@Author: FoskyM
@Date: 2024-03-10
"""


# 打印饭卡数据
def print_hex(content):
    for i in range(0, len(content), 64):
        print('第', i // 64, '扇区')
        for j in range(4):
            for k in range(0, 16):
                print('%02x' % content[i + j * 16 + k], end=' ')
            print()


# file_path = 'F:\path_to_file\nfc_data.dump'

file_path = input('请输入文件路径：')

with open(file_path, 'rb') as file:
    content = file.read()
    file.close()

    if len(content) == 4096:
        print('This is a S70 4K file')
        content = content[0:1024]
    elif len(content) == 1024:
        print('This is a S50 1K file')

    print_hex(content)

    card_no = int.from_bytes(content[0:4], byteorder='little')
    print('卡号：', card_no)
    stu_no = content[960:970].decode('utf-8')
    print('学号：', stu_no)
    money = int.from_bytes(content[64:66], byteorder='little') / 100
    print('余额：', money)

    new_file_path = file_path.replace('.dump', '_原始卡.dump')
    with open(new_file_path, 'wb') as f:
        f.write(content)
        f.close()

    content = bytearray(content)
    new_file_path = file_path.replace('.dump', '_原始卡_修改0扇区控制位.dump')
    content[54:58] = b'\xff\x07\x80\x69'
    with open(new_file_path, 'wb') as f:
        f.write(content)
        f.close()

    for i in range(0, 1024, 64):
        if i != 0:
            content[i:i + 48] = b'\x00' * 48  # 清空数据
        content[i + 48:i + 48 + 6] = b'\xff' * 6  # A密钥
        content[i + 48 + 6:i + 48 + 10] = b'\xff\x07\x80\x69'  # 控制位
        content[i + 48 + 10:i + 48 + 16] = b'\xff' * 6  # B密钥

    new_file_path = file_path.replace('.dump', '_中介卡.dump')
    with open(new_file_path, 'wb') as f:
        f.write(content)
        f.close()
