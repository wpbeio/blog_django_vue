# -*- coding: utf-8 -*-
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User, BaseUserManager, AbstractUser


# 用来修改admin中显示的app名称,因为admin app 名称是用 str.title()显示的,所以修改str类的title方法就可以实现.
# class string_with_title(str):
#     def __new__(cls, value, title):
#         instance = str.__new__(cls, value)
#         instance._title = title
#         return instance

#     def title(self):
#         return self._title

#     __copy__ = lambda self: self
#     __deepcopy__ = lambda self, memodict: self


# Create your models here.
# class BeioUserManager(BaseUserManager):
#     def create_user(self, username, email,  password=None):
#         """
#         保存用户，测试是否是邮箱
#         """
#         if not email:
#             raise ValueError('必须使用正确的邮箱')

#         user = self.model(
#             username=username,
#             email=self.normalize_email(email),
#             # date_of_birth=date_of_birth,
#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, email,  password):

#         user = self.create_user(
#             username,
#             email,
#             password=password,

#         )
#         user.is_admin = True
#         user.save(using=self._db)
#         return user

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
