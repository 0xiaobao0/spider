import binascii
import base64
import rsa
from scrapy.http import Request
import time
import scrapy

# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives.asymmetric import rsa
# from cryptography.hazmat.primitives import serialization

pub_key = 'AKXlKKqP9xrsxnXP6q4cIp9apHXYpZcvNe2LnGn\/2X6XMexn5izTTNHrLFF2YFrtUokiyhza0D8N7Q5zZkc6WFDe5b6BltdcY1fqTX2YUOk9nJEgwOqxfORDLhvKzF09t7f3FhnUtDz7kdB74MGrc8c10GHemYptkLFcFL6POguj'

# def populate_public_key(data):
#     # convert bytes to integer with int.from_bytes
#     # 指定从little格式将bytes转换为int，一句话就得到了公钥模数，省了多少事
#     n = int(data,16)
#     e = 65537
#
#     # 使用(e, n)初始化RSAPublicNumbers，并通过public_key方法得到公钥
#     # construct key with parameter (e, n)
#     key = rsa.RSAPublicNumbers(e, n).public_key(default_backend())
#
#
#     return key
#
# # 将公钥以PEM格式保存到文件中
# def save_pub_key(pub_key, pem_name):
#     # 将公钥编码为PEM格式的数据
#     pem = pub_key.public_bytes(
#         encoding=serialization.Encoding.PEM,
#         format=serialization.PublicFormat.SubjectPublicKeyInfo
#     )
#
#     # print(pem)
#
#     # 将PEM个数的数据写入文本文件中
#     with open(pem_name, 'w+') as f:
#         f.writelines(pem.decode())
#
#     return




#删除首位函数
# def delete_first(s):
#     return s[1:]


def b64tohex(s):
    data = base64.b64decode(s)
    hex_data = binascii.b2a_hex(data)
    a = hex_data.decode('ascii')
    # b = delete_first(str(a))
    return a


exponent = 'AQAB'
modulus = 'AJ0qVfsIln5y2jJ1+fmp+C2Ny\/GvBF83BiSSD2z5zHkxLoXNKVkm8Rz5+OZjQZkUe4QS6DijIXbqVqOoMW8EXZKxVlFkSOesctq583VvtpKWvM4xQtTAodkzXVGozCfuiTQegDGdClnqTJgfgaq+j\/FuSseh6RKTgTNbNsFhv+hb'

a = b64tohex(exponent)
b = int(b64tohex(exponent),16)
c = b64tohex(modulus)
d = int(b64tohex(modulus),16)

rsaPublickey = int(b64tohex(modulus),16)
key = rsa.PublicKey(d, b) #创建公钥
message = b'123abc'
passwd = rsa.encrypt(message, key) #加密
passwd = base64.b64encode(passwd)
print(passwd.decode('ascii'))
r0 = Request('http://jwxt.neuq.edu.cn/jwglxt/xtgl/login_slogin.html?'+str(int(time.time())))

payload = {
    'csrftoken': '6aaa9f6c-3719-4351-8dee-f840a8356aed,6aaa9f6c371943518deef840a8356aed',
    'yhm': '20168709',
    'mm': 'X0WiBtBSRbX6oyqXuY4sDI0fzuqazUJf3M2qqpQBNx/2w5bEjiPjNYyx52szB0MijO74bw6MpGIuSARTcwVISf+KsW2httqajfIEUvhD78fXMNF4xVjo2Wvy18BMrnMVl0U1+L7xxnFtlKM3V0A2ikb/ApS0Y4aYLeP0Xa0tEvM=',
    'mm': 'X0WiBtBSRbX6oyqXuY4sDI0fzuqazUJf3M2qqpQBNx/2w5bEjiPjNYyx52szB0MijO74bw6MpGIuSARTcwVISf+KsW2httqajfIEUvhD78fXMNF4xVjo2Wvy18BMrnMVl0U1+L7xxnFtlKM3V0A2ikb/ApS0Y4aYLeP0Xa0tEvM='
}

# r = requests.post('http://jwxt.neuq.edu.cn/jwglxt/xtgl/login_slogin.html?'+str(int(time.time())),json=payload)
print(r0)

# if __name__ == '__main__':
#         pub_key = populate_public_key(data=b64tohex(modulus))
#         pem_file = r'pub_key.pem'
#         save_pub_key(pub_key, pem_file)
#         print(rsa.('123abc',pub_key))



# d = u'AQAB'
# d0 = u'AOsJpi7ntcIJhtFvXhK4HwMZtKmkaLliLq\/zXI7fpjJTjubBjbXVa\/e6zrxgDTqE3aetivhvQhUtI81qC9KinxmESqj\/KCAre2ui88AMTBFkZSxh6K1tC2EJPkB7q3s9nOS2AxNiKgu2nElky\/FGGUwyaKskFULRaPbtywqMAmMv'
#
# #对base64字符串解码
# data = base64.b64decode(d)
#
# #将解码后的base64字符串转换为16进制二进制字符串如b'010001'
# hex_data = binascii.b2a_hex(data)
#
# #将转换后的二进制字符串转换为16进制的ascii码，即得到010001
# a = hex_data.decode('ascii')
#
# #删除首位后得到16进制数
# b = delete_first(str(a))
#
# #十六进制转十进制
# int_exponent = int(b,16)
# print(int_exponent)



