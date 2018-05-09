# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from beio_blog.models import Post

# Create your models here.


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


# CASCADE：模拟SQL语言中的ON DELETE CASCADE约束，将定义有外键的模型对象同时删除！（该操作为当前Django版本的默认操作！）
# PROTECT:阻止上面的删除操作，但是弹出ProtectedError异常
# SET_NULL：将外键字段设为null，只有当字段设置了null=True时，方可使用该值。
# SET_DEFAULT:将外键字段设为默认值。只有当字段设置了default参数时，方可使用。
# DO_NOTHING：什么也不做。
# SET()：设置为一个传递给SET()的值或者一个回调函数的返回值。注意大小写。

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name=u'用户', on_delete=models.CASCADE)
    #   user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'用户')
    post = models.ForeignKey(Post, verbose_name=u'文章', on_delete=models.CASCADE)
    text = models.TextField(verbose_name=u'评论内容')
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)

    parent = models.ForeignKey('self', default=None, blank=True, null=True,
                               verbose_name=u'引用', on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = verbose_name = u'评论'
        ordering = ['-create_time']
        # app_label = string_with_title('comments', u"评论管理")

    def __unicode__(self):
        return self.post.title + '_' + str(self.pk)

    __str__ = __unicode__
