#!/usr/bin/env python
# encoding: utf-8

import time


class OnlineMiddleware(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super().__init__()

    def __call__(self, request):
        # 自定义中间件常用场景举例：
        # 禁止特定IP地址的用户或未登录的用户访问我们的View视图函数
        # 对同一IP地址单位时间内发送的请求数量做出限制
        # 在View视图函数执行前记录用户的IP地址
        # 在View视图函数执行前传递额外的变量或参数
        # 在View视图函数执行前或执行后把特定信息打印到log日志（代码如下）
        # 在View视图函数执行后对reponse数据进行修改后返回给用户
        start_time = time.time()
        response = self.get_response(request)
        http_user_agent = request.META.get('HTTP_USER_AGENT', [])
        # 对于爬虫不做处理
        if 'Spider' in http_user_agent or 'spider' in http_user_agent:
            return response

        cast_time = time.time() - start_time
        response.content = response.content.replace(b'<!!LOAD_TIMES!!>', str.encode(str(cast_time)[:5]))
        return response
