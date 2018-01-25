"""
课 5 上课内容预习


本次上课的主要内容如下


增加作业中的 redirect 函数
    routes.py 中

一个简单 todo 程序项目, 包含的文件如下
    routes_todo.py 包含了项目的所有路由函数
        显示所有todo (包含在文件中)
        增加todo (包含在文件中)
        删除todo (上课讲)
        删除todo (上课讲, 需要更改 Model)
    todo.py
        包含了 Todo Model, 用于处理数据
    templates/todo_index.html
        显示所有 todo 的页面
    templates/todo_edit.html
        显示编辑 todo 的界面 (现在是空白文件 上课会增加内容)

把 TODO 改写为带用户功能的高级版(这部分上课讲)
    涉及到不同数据的关联
    关联数据在服务器/浏览器之间的传递
"""



# 下面是一些 HTTP 请求和响应的例子, 本课用不着
"""
POST /login?id=2 HTTP/1.1
Host: localhost:3000
Connection: keep-alive
Content-Length: 25
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36
Content-Type: application/x-www-form-urlencoded
Cookie: Pycharm-7367d7d5=bf094603-b9e9-4994-9ebd-564f1f5ad2c0

username=gua&password=123
"""

"""
2017/02/22 19:42:48 login 的响应
HTTP/1.1 210 VERY OK
Content-Type: text/html
Set-Cookie: user=gua1

<html>
"""

"""
2017/02/22 19:45:16 ip and request, ('127.0.0.1', 50317)
GET /login HTTP/1.1
Host: localhost:3000
Connection: keep-alive
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Cookie: user=gua1
"""
