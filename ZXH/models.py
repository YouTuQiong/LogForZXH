# from django.contrib.auth.models import User
from django.db import models
from filer.fields.image import FilerImageField
class User(models.Model):
    username = models.CharField(max_length=20,null=False)
    password = models.CharField(max_length=20,null=False)
    name = models.CharField(max_length=10,null=False) #名称
    Email = models.EmailField(max_length=50)
class Log(models.Model):
    img = FilerImageField(null=True, blank=True,
                           related_name="head_Article")

    title = models.CharField(max_length=70, verbose_name='标题')
    body = models.TextField(verbose_name='正文')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(verbose_name='最后修改时间',)
    excerpt = models.TextField(verbose_name='摘要')
    location = models.CharField(max_length=100,verbose_name='位置')
    weather = models.CharField(max_length=100,verbose_name='天气')
    tags = models.CharField(max_length=100,blank=True, verbose_name='标签')
    mood = models.CharField(max_length=100, blank=True, verbose_name='标签')
    isShow = models.BooleanField(default=True, verbose_name='是否显示')
    views = models.PositiveIntegerField(default=0, verbose_name='阅读量')
    owner = models.ForeignKey(User)  # 博客的创建者


