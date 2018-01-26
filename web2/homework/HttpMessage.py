# http 请求报文格式
# <method> <path> <version> \r\n
# <headers> \r\n
# \r\n
# <body>
from log import log


class HttpRequest(object):
    supported_method_list = [
        'GET',
        'POST',
        'HEAD',
        'PUT',
        'TRACE',
        'OPTIONS',
        'DELETE',
    ]

    def __init__(self, method='GET', path='/', header=None, body=None):
        self._method = method.upper()
        self._path = path.lower()
        self._header = header
        self._body = ''

    def form_request_text(self):
        request_line = '{method} {path} HTTP/1.1\r\n'.format(method=self._method, path=self._path)

        header_lines = ''
        if self._header :
            for k, v  in self._header.items():
                header_lines += '{key}:{value}\r\n'.format(key=k, value=v)
        else:
            header_lines = '\r\n'

        body = self._body

        text = request_line + header_lines + '\r\n' +body
        print('HttpRequest: {}'.format(text))
        return text.encode('utf-8')


# http响应报文格式
# <version> <status-code> <status-string> \r\n
# <headers> \r\n
# \r\n
# <body>
import time
class HttpRespone(object):
    def __init__(self, text=None):
        #with open('./httprespone-{}.txt'.format(time.strftime("%Y%m%d%H%M%S", time.localtime())), 'wb') as f:
        #    f.write(text)
        self._text = text
        text = text.decode('utf-8')
        self._status_code = 0
        self._status_string = ''
        self._version = ''
        self._headers = {}
        self._body = None
        log('HttpRespone text: {}'.format(type(text)))
        if text:
            log('HttpRespone {}'.format(text.split('\r\n')))
            if len(text.split('\r\n')) > 2:
                respone_line,text = text.split('\r\n', 1)
                log('HttpRespone respone_line:{}'.format(respone_line))
                self._version = respone_line.split(maxsplit=2)[0].strip()
                self._status_code = int(respone_line.split(maxsplit=2)[1].strip())
                self._status_string = respone_line.split(maxsplit=2)[2].strip()

                # fixme text 没有实体的时候怎么处理
                header_lines = text.split('\r\n\r\n')[0]
                print('header_lines: {}'.format(header_lines))
                for item in header_lines.split('\r\n'):
                    k, v = item.split(':', 1)
                    self._headers[k] = v

                if len(text.split('\r\n\r\n')) >=2:
                    self._body = text.split('\r\n\r\n')[1].encode('utf-8')
                    log('HttpRespone', self._body)
    @property
    def status_code(self):
        return self._status_code


    @property
    def status_string(self):
        return self._status_string

    @property
    def version(self):
        return self._version

    @property
    def header(self):
        return self._headers

    @property
    def body(self):
        return self._body
