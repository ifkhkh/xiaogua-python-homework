#coding: utf-8

import socket
import ssl


from HttpMessage import HttpRespone
from HttpMessage import HttpRequest
from log import log

"""
2017/02/16
作业 1


资料:
在 Python3 中，bytes 和 str 的互相转换方式是
str.encode('utf-8')
bytes.decode('utf-8')

send 函数的参数和 recv 函数的返回值都是 bytes 类型
其他请参考上课内容, 不懂在群里发问, 不要憋着
"""


# 补全函数
def parsed_url(url):
    '''
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'
    返回一个 tuple, 内容如下 (protocol, host, port, path)
    '''
    default_protocol = 'http'
    default_host = '127.0.0.1'
    default_port = 80
    default_path = '/'

    protocol = default_protocol
    host = default_host
    port = default_port
    path = default_path

    # 去掉url两端的空白符
    url = url.strip()

    # 解析url协议
    if url.startswith('http://'):
        protocol = 'http'
        port = 80  #更新协议默认端口
        url = url[7:]
    elif url.startswith('https://'):
        protocol = 'https'
        port = 443  #更新协议默认端口
        url = url[8:]


    # 解析path
    if url.count('/') > 0:
        url, path = url.split('/')
        path = '/' + path


    # 解析host和port
    if url.count(':') > 0:
        host, port = url.split(":")
        port = int(port)
    else:
        host = url

    print('parsed_url-->protocol:{}, host:{}, port:{}, path:{} '.format(protocol, host, port, path))
    return (protocol, host, port, path)

def test_parsed_url():
    urls_for_testing = {
    'g.cn'                   : ('http', 'g.cn', 80, '/'),
    'g.cn/'                  : ('http', 'g.cn', 80, '/'),
    '   g.cn/'               : ('http', 'g.cn', 80, '/'),
    'g.cn:3000'              : ('http', 'g.cn', 3000, '/'),
    'g.cn:3000/search'       : ('http', 'g.cn', 3000, '/search'),
    'http://g.cn'            : ('http', 'g.cn', 80, '/'),
    '    http://g.cn    '    : ('http', 'g.cn', 80, '/'),
    'https://g.cn'           : ('https', 'g.cn', 443, '/'),
    'https://g.cn:3000'      : ('https', 'g.cn', 3000, '/'),
    'http://g.cn/'           : ('http', 'g.cn', 80, '/'),
    }
    for url, accept_result in urls_for_testing.items():
        print('parsing url:{}'.format(url))
        result = parsed_url(url)
        print('result: {}'.format(result))
        print('')
        assert(accept_result == result)
    print('test_parsed_url success.')


def socket_by_protocol(protocol):
    # 创建一个 socket 对象
    # 参数 socket.AF_INET 表示是 ipv4 协议
    # 参数 socket.SOCK_STREAM 表示是 tcp 协议
    s = socket.socket()
    # 这两个其实是默认值, 所以你可以不写, 如下
    # s = socket.socket()
    if protocol == 'https':
        s = ssl.wrap_socket(socket.socket())
    return s


# https://www.cnblogs.com/litaozijin/p/6624029.html
# socket 接收完整数据
def recv_basic(the_socket):
    total_data = []
    while True:
        data = the_socket.recv(1024)
        if not len(data): break
        total_data.append(data)
    return b''.join(total_data)


def http_request(socket, method='GET', path='/', header={}, body=None):
    request_text = HttpRequest(method, path, header, body).form_request_text()
    socket.send(request_text)
    return HttpRespone(recv_basic(socket))


# 5
# 把向服务器发送 HTTP 请求并且获得数据这个过程封装成函数
# 定义如下
def get(url):
    '''
    本函数使用上课代码 client.py 中的方式使用 socket 连接服务器
    获取服务器返回的数据并返回
    注意, 返回的数据类型为 bytes
    '''
    print('get url:{}'.format(url))
    protocol, host, port, path = parsed_url(url)

    socket = socket_by_protocol(protocol)
    # 用 connect 函数连接上主机, 参数是一个 tuple
    socket.connect((host, port))


    header = {
        'host' : host,
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Connection' : 'close',   # 不加这个域，recv完后会等待超时，一直卡在那
    }
    response = http_request(socket, method='GET', path=path, header=header)
    socket.close()

    log('respone code {}'.format(response.status_code))
    if response.status_code in [301, 302]:
        log(response.header)
        return get(response.header['Location'])
    else:
        return response.body


# 使用
def main():
    #test_parsed_url()
    url = 'http://movie.douban.com/top250'
    r = get(url)
    print(r)

if __name__ == '__main__':
    main()