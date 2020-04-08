from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse,redirect,reverse
class MD(MiddlewareMixin):

    # def process_request(self,request):
    #     path=request.path_info
    #     if path == "/login/":
    #         return None
    #     else:
    #         try:
    #             ret = request.COOKIES['verify']
    #             if ret == "pass":
    #                 return None
    #             else:
    #                 return HttpResponse("你还没有登录")
    #         except:
    #             return redirect(reverse('app01:login'))
    #             print('process_request')

    def process_request(self,request):
        path = request.path_info
        white_list=['/login/',]
        black_list=['/index/','/home/']
        if path in white_list:
            return None
        elif path in black_list:
            try:
                ret = request.session['verify']
                if ret == "pass":
                    return None
            except Exception:
                return redirect('/login/?next=%s'%path)
        else:
            return redirect('/login/?new=%s'%path)

visit_list={}
class Frequence(MiddlewareMixin):

    def process_request(self,request):
        #1.获取ip
        # print(request.META)
        ip = request.META['REMOTE_ADDR']
        #2.记录ip
        print('old',visit_list)
        if not visit_list.get(ip):
            visit_list[ip]=[]
        print('new',visit_list)
        history = visit_list[ip]
        #3.判断访问记录
        import time
        now = time.time()
        while history and now-history[0]>5:
            history.pop(0)
        if len(history)>2:
            return HttpResponse('你访问的频率过快，自动关闭网页')
        history.append(now)
        print(history)


