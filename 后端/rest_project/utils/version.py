from rest_framework import versioning


class MyVersion(object):
    def determine_version(self, request, *args, **kwargs):
        # 方法的返回值是版本号
        # 获取前端传过来的版本号 并且把版本号返回
        version = request.query_params.get("version")
        if not version:
            version = "v1"
        return version
