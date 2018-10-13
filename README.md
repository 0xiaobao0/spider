# spider
记一次爬学校教务处的爬虫

主要难点在于模拟登陆过程中遇到的通过公钥生成加密后的密码，通过分析js文件发现是通过前台将明文密码加密后放入表单传给后台利用私钥解密，于是模拟js中的加密方法加密，开始时的加密方法如下：


    def delete_first(self, s):
        return s[1:]


    def b64tohex(self, s):
        data = base64.b64decode(s)
        hex_data = binascii.b2a_hex(data)
        a = hex_data.decode('ascii')
        b = self.delete_first(str(a))
        return b
        
        
    def get_passwd(self):
        result = session.get(
            url='http://jwxt.neuq.edu.cn/jwglxt/xtgl/login_getPublicKey.html')
        bytes_args = result._content
        str_args = bytes_args.decode('ascii')
        list_args = literal_eval(str_args)
        exponent = list_args['exponent']
        modulus = list_args['modulus']
        e = int(self.b64tohex(exponent), 16)
        m = int(self.b64tohex(modulus), 16)
        key = rsa.PublicKey(m, e)
        password = b'123abc'
        passwd = rsa.encrypt(password, key)  # 加密
        passwd = base64.b64encode(passwd)
        return passwd
        
        
  先通过访问接口获取到指数和模的dict（byte形式），将其转成ascii码变成python中的str，再通过函数将该str转换成真正的dict，再通过改dict获取到指数和模（64位的），然后再将64位通过自定义的64位转换为十进制位转换成16进制，随后将16进制转换成10进制，此时得到生成公钥真正要用到的指数和模，然后再利用python中的rsa.Public函数成公钥并对密码加密（此处密码得用b''的形式）。
  
  
  在该过程中对浏览器的编码规则不太明白，一番折腾觉得不断的转码转换进制未免太麻烦，此后找到一位大佬的生成公钥的方法（school_spider2.py），直接获取到byte形式数组中的modulus，和exponent，然后直接用base64.b64decode()函数解码成16位。。随后通过从int.from_bytes(bstring,'big')从bytes中获取int，然后再生成公钥加密。妙哉。。。省了不少功夫
  
  
  还有需要注意的地方就是cookie的保存和加载，以及请求各个接口时不能直接用request.get()或者request.post()，而应该设置session = requests.Session()
随后用session.get()或者session.post()为什么要这样呢，根据request官方文档的解释：会话对象让你能够跨请求保持某些参数。它也会在同一个 Session 实例发出的所有请求之间保持 cookie， 期间使用 urllib3 的 connection pooling 功能。所以如果你向同一主机发送多个请求，底层的 TCP 连接将会被重用，从而带来显著的性能提升。 (参见 HTTP persistent connection).
  
