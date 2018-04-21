# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView,UpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from ZXH.permissions import *
from ZXH.Util import  *
from ZXH.serializers import *
from ZXH.httpResponse import *


# 用于登录
class UserLoginAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    Encryption =  Encryption()
    def post(self, request, format=None):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = User.objects.get(username__exact=username)
        regip = IPAddress(request)
        password = username + username
        password = Encryption.SHA256Encryption(password)
        if user.password == password:
            serializer = UserSerializer(user)
            new_data = serializer.data
            # 记忆已登录用户
            self.request.session['user_id'] = user.id
            return Response(new_data, status=HTTP_200_OK)
        return Response('password error', HTTP_400_BAD_REQUEST)


# 用于注册
class UserRegisterAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        data = request.data
        username = data.get('username')

        if User.objects.filter(username__exact=username):
            return Json("",message="注册失败,用户名已经存在",state="200")
        elif User.objects.filter(email__exact=data.get('email')):
            return Json("", message="注册失败,邮箱已经存在", state="200")
        elif User.objects.filter(email__exact=data.get('user')):
            return Json("", message="注册失败,邮箱已经存在", state="200")

        # 密码加密
        data["password"] =Encryption.SHA256Encryption(Encryption,(data.get('password') + str(username)))

        serializer = UserRegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Json({"name":data["name"]},message="登录成功",state="200")
        return Json({"name":data["name"]},message="登录成功",state="200")


class LogViewSet(viewsets.ViewSet, RetrieveUpdateDestroyAPIView):
    queryset = Log.objects.filter(owner=0)
    permission_classes = (AllowAny,)

    def list(self, request):
        owner = isLogin(request)
        if (owner is None):return noLogin()
        queryset = Log.objects.filter(owner=owner)
        serializer = LogSerializer(queryset, many=True)
        if len(queryset) ==0:
            return Json("",message="获取失败，")
        return Json(serializer.data)

    # 检索数据
    def retrieve(self, request, pk=None):
        owner = isLogin(request)
        if (owner is None):return noLogin()
        queryset = Log.objects.filter(pk=pk, owner=owner)
        serializer = LogSerializer(queryset, many=True)
        return Json(serializer.data)
    def post(self, request, format=None):
        owner = isLogin(request)
        if (owner is None): return noLogin()
        data = request.data
        serializer = LogSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Json(serializer.data)
        return Json(serializer.errors, status=HTTP_400_BAD_REQUEST)


class LogView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = None
    queryset = None

    def put(self, request, *args, **kwargs):
        owner = isLogin(request)
        if owner is None:
            return Json("", state=233, message="更新日志失败")
        else:
            self.serializer_class = LogSerializer
            vid = self.kwargs['pk']
            id = request.data.get('id')
            if vid != id:
                return Json("", state=233, message="更新日志失败,未找到该篇日志")
            self.queryset = Log.objects.filter(owner=owner, pk=id)
            self.update(request, *args, **kwargs)
            return Json("", status=HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# 登出
class LogoutAPIView(APIView):
    def get(self, requests, format=None):
        if self.request.session['user_id'] is not None:
            self.request.session['user_id'] = None
            return Response({"message": "退出成功"}, status=HTTP_200_OK)
        else:
            return Response({"message": "暂未登陆，无需登出"}, status=HTTP_400_BAD_REQUEST)
