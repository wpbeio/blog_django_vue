# -*- coding: utf-8 -*-
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User, BaseUserManager, AbstractUser


'''
继承虚类，重写一些字段和方法
'''
class BeioUser(AbstractUser):
    username = models.CharField(max_length=20, unique=True, verbose_name='用户名')
    email = models.EmailField(
        verbose_name='邮箱地址',
        max_length=255,
        unique=True
    )
    is_active = models.BooleanField(default=False)
    date_of_birth = models.DateField(
        verbose_name='生日', default=timezone.now)
    # createdate = models.DateField(auto_now_add=True, verbose_name='创建日期')
    img = models.CharField(max_length=200, default='/media/tx/default.jpg',
                           verbose_name=u'头像地址')
    intro = models.CharField(max_length=200, blank=True, null=True,
                             verbose_name=u'简介')
    # 确定为username的字段
    USERNAME_FIELD = 'username'
    # 必填字段
    REQUIRED_FIELDS = ['email']
