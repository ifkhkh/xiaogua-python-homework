# 2017/02/23
#
# ========
# 作业 4
#


# 1 2 课的作业, 保存到你的代码中, 名字分别为 web4a1 web4a2
# 注意, 收费的支付宝帐号是 xiaogua255@outlook.com 姓 何
# 付款时, 请备注以如下的格式备注
# web4 3400711034 瓜


# 作业 4.1
#
# 给 User 添加 1 个新属性 note 表示签名
# 做法如下
# 1, 在 注册 页面添加一个新的 input 让用户输入 note
# 2, 在 User 类的初始化中添加一个新的属性 note 并且用 form 里的元素赋值


# 作业 4.2
#
# 添加一个新的路由 /profile (在 routes.py 文件中)
# 如果登录了, 则返回一个页面显示用户的三项资料(id, username, note)
# 如果没登录, 返回 302 为状态码来 重定向到登录界面
# 当返回 302 响应的时候, 必须在 HTTP 头部加一个 Location 字段并且设置值为你想要定向的页面
# 如果不理解这个格式, 请查看之前作业中豆瓣电影页面返回的 301 响应的格式
