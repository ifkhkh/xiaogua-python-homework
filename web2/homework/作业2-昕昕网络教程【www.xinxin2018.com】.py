# 2017/02/18
# 作业 2
# ========
#
#
# 请直接在我的代码中更改/添加, 不要新建别的文件


# 定义我们的 log 函数
def log(*args, **kwargs):
    print('log', *args, **kwargs)


# 作业 2.1
#
# 实现函数
def path_with_query(path, query):
    '''
    path 是一个字符串
    query 是一个字典

    返回一个拼接后的 url
    详情请看下方测试函数
    '''
    result_list = []
    for k, v in query.items():
        if result_list:
            result_list.append('&')
        result_list.append('{key}={value}'.format(key=k, value=v))
    if result_list :
        result_list = [path, '?']+result_list
    else:
        result_list.append(path)
    log('result_list {}'.format(result_list))
    return ''.join(result_list)


def test_path_with_query():
    # 注意 height 是一个数字
    path = '/'
    query = {
        'name': 'gua',
        'height': 169,
    }
    expected = [
        '/?name=gua&height=169',
        '/?height=169&name=gua',
    ]
    # NOTE, 字典是无序的, 不知道哪个参数在前面, 所以这样测试
    assert path_with_query(path, query) in expected


# 作业 2.2
#
# 为作业1 的 get 函数增加一个参数 query
# query 是字典

# GET 方法中 url中的query参数是通过http请求头的path传递给服务器的

import socket
import ssl
from HttpMessage import HttpRespone
from HttpMessage import HttpRequest
from log import log
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
        if not len(data):
            break
        log('recv_basic {}'.format(data))
        total_data.append(data)

    return b''.join(total_data)


def http_request(socket, method='GET', path='/', header=None, body=None):
    request_text = HttpRequest(method, path, header, body).form_request_text()
    socket.send(request_text)
    return HttpRespone(recv_basic(socket))


# 5
# 把向服务器发送 HTTP 请求并且获得数据这个过程封装成函数
# 定义如下
def get_with_query(url, query=None):
    '''
    本函数使用上课代码 client.py 中的方式使用 socket 连接服务器
    获取服务器返回的数据并返回
    注意, 返回的数据类型为 bytes
    '''
    print('get url:{}'.format(url))
    protocol, host, port, path = parsed_url(url)

    if query:
        path = path_with_query(path, query)

    socket = socket_by_protocol(protocol)
    # 用 connect 函数连接上主机, 参数是一个 tuple
    socket.connect((host, port))


    header = {
        'host': host,
        #'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
        #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Connection': 'close',   # 不加这个域，recv完后会一直卡在那等待超时.
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       # 'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    }
    response = http_request(socket, method='GET', path=path, header=header)
    socket.close()

    log('respone code {}'.format(response.status_code))
    if response.status_code in [301, 302]:
        log(response.header)
        return get_with_query(response.header['Location'], query)
    else:
        return response.body


def test_get_with_query():
    url = 'https://movie.douban.com/top250'
    query = {
        'start': '10',
    }
    r = get_with_query(url, query)
    print(r.decode('utf-8'))


# 作业 2.3
#
# 实现函数
def header_from_dict(headers):
    '''
    headers 是一个字典
    范例如下
    对于
    {
    	'Content-Type': 'text/html',
        'Content-Length': 127,
    }
    返回如下 str
    'Content-Type: text/html\r\nContent-Length: 127\r\n'
    '''
    result_list = ['{key}: {value}\r\n'.format(key=k, value=v) for k, v in headers.items()]
    log('header_from_dict result_list {}'.format(result_list))
    return ''.join(result_list)


# 作业 2.4
#
# 为作业 2.3 写测试
def test_header_from_dict():
    header = {
        'Content-Length': 127,
        'Content-Type' : 'text/html',
    }
    expected = [
        'Content-Type: text/html\r\nContent-Length: 127\r\n',
        'Content-Length: 127\r\nContent-Type: text/html\r\n',
    ]
    # NOTE, 字典是无序的, 不知道哪个参数在前面, 所以这样测试
    assert header_from_dict(header) in expected


# 作业 2.5
#
"""
豆瓣电影 Top250 页面链接如下
https://movie.douban.com/top250
我们的 client_ssl.py 已经可以获取 https 的内容了
这页一共有 25 个条目

所以现在的程序就只剩下了解析 HTML

请观察页面的规律，解析出
1，电影名
2，分数
3，评价人数
4，引用语（比如第一部肖申克的救赎中的「希望让人自由。」）

解析方式可以用任意手段，如果你没有想法，用字符串查找匹配比较好(find 特征字符串加切片)
"""

from bs4 import BeautifulSoup


def parse_doubanmovies250_onepage(html):
    parsed_html = BeautifulSoup(html, 'html.parser')
    log('parse_doubanmovies250_onepage', parsed_html.body.find_all('li'))
    #log('parse_doubanmovies250_onepage', parsed_html.body.find('ol', class_='grid_view'))

# 作业 2.6
#
"""
通过在浏览器页面中访问 豆瓣电影 top250 可以发现
1, 每页 25 个条目
2, 下一页的 URL 如下
https://movie.douban.com/top250?start=25

因此可以用循环爬出豆瓣 top250 的所有网页

于是就有了豆瓣电影 top250 的所有网页

由于这 10 个页面都是一样的结构，所以我们只要能解析其中一个页面就能循环得到所有信息

所以现在的程序就只剩下了解析 HTML

请观察规律，解析出
1，电影名
2，分数
3，评价人数
4，引用语（比如第一部肖申克的救赎中的「希望让人自由。」）

解析方式可以用任意手段，如果你没有想法，用字符串查找匹配比较好(find 特征字符串加切片)
"""
import requests
import time
if __name__ == '__main__':
    #test_path_with_query()
    #test_header_from_dict()
    #test_get_with_query()

    #with open('./test1.html', 'wb') as f:
    #    #f.write(get_with_query('http://www.baidu.com'))
    #    f.write(get_with_query('https://movie.douban.com/top250'))
    with open('./test2.html', 'wb') as f:
        f.write(requests.get('https://movie.douban.com/top250').text.encode('utf-8'))
    parse_doubanmovies250_onepage(requests.get('https://movie.douban.com/top250').text)