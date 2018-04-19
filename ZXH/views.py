
# Create your views here.
from django.contrib.auth.models import User, Group
from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.decorators import api_view

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from ZXH.permissions import *
from ZXH.serializers import *
from ZXH.httpcheck import *

# class LogsAPIView(viewsets.ModelViewSet):
#     queryset = Log.objects.all()
#     serializer_class = LogSerializer
# 用于登录
class UserLoginAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = User.objects.get(username__exact=username)
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
            return Response("用户名已存在", HTTP_400_BAD_REQUEST)
        serializer = UserRegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


#


class LogViewSet(viewsets.ViewSet):
    queryset = Log.objects.filter(owner=2)
    def list(self, request):
        owner = request.session.get('user_id')
        if(owner is None):
            return noLogin()
        queryset = Log.objects.filter(owner=1)
        serializer = LogSerializer(queryset, many=True)
        return Response(serializer.data)

    # 检索数据

    def retrieve(self, request, pk=None):
        owner = request.session.get('user_id')
        queryset = Log.objects.filter(owner=owner, pk=pk)
        serializer = LogSerializer(queryset, many=True)
        return Response(serializer.data)



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


#登出
class LogoutAPIView(APIView):
    def get(self, requests, format=None):
        if self.request.session['user_id'] is not None:
            self.request.session['user_id'] = None
            return Response({"message": "退出成功"}, status=HTTP_200_OK)
        else:
            return Response({"message": "暂未登陆，无需登出"}, status=HTTP_400_BAD_REQUEST)
