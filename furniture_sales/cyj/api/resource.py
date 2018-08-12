from django.conf.urls import url
from django.http import HttpResponse

"""
接口类
"""


class Api(object):
    # 构造函数
    def __init__(self, name="v1"):
        self.name = name
        # 资源队列
        self.resources = []

    def add_resource(self, resource):
        """
		添加资源
		"""
        self.resources.append(resource)

    @property
    def urls(self):
        """
        生成url的函数
        """
        patterns = [

            url(r'^{version}/{name}'.format(version=self.name, name=resource.name), resource.process_request)
            for resource in self.resources
        ]

        return patterns


"""
资源类
"""


class Resource(object):
    # 构造函数
    def __init__(self, name=None):
        self.name = name or self.__class__.__name__.lower()

    def process_request(self, request, *args, **kwargs):
        method = request.method
        if method == "GET":
            return self.get(request, *args, **kwargs)
        if method == "POST":
            return self.post(request, *args, **kwargs)
        if method == "PUT":
            return self.post(request, *args, **kwargs)
        if method == "DELETE":
            return self.delete(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return HttpResponse("get")

    def post(self, request, *args, **kwargs):
        return HttpResponse("post")

    def put(self, request, *args, **kwargs):
        return HttpResponse("put")

    def delete(self, request, *args, **kwargs):
        return HttpResponse("delete")
