from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import User
from tagging.fields import TagField
from tagging.models import Tag
from django.conf import settings


# class string_with_title(str):
#     """ 用来修改admin中显示的app名称,因为admin app 名称是用 str.title()显示的,
#     所以修改str类的title方法就可以实现.
#     """
#     def __new__(cls, value, title):
#         instance = str.__new__(cls, value)
#         instance._title = title
#         return instance

#     def title(self):
#         return self._title

#     def __copy__(self): return self

#     def __deepcopy__(self, memodict): return self


STATUS = {
    0: '正常',
    1: '草稿',
    2: '删除',
}


# class beioTag(Tag):
#     class Meta:
#         verbose_name = r'标签'
# Create your models here.


# CASCADE：模拟SQL语言中的ON DELETE CASCADE约束，将定义有外键的模型对象同时删除！（该操作为当前Django版本的默认操作！）
# PROTECT:阻止上面的删除操作，但是弹出ProtectedError异常
# SET_NULL：将外键字段设为null，只有当字段设置了null=True时，方可使用该值。
# SET_DEFAULT:将外键字段设为默认值。只有当字段设置了default参数时，方可使用。
# DO_NOTHING：什么也不做。
# SET()：设置为一个传递给SET()的值或者一个回调函数的返回值。注意大小写。


class Category(models.Model):
    """bolg的分类"""
    name = models.CharField(max_length=100, verbose_name='名称')

    child = models.ForeignKey('self', default=None,
                              blank=True, null=True, verbose_name='下级分类', on_delete=models.SET_NULL)
    rank = models.IntegerField(default=0, verbose_name='排序')
    status = models.IntegerField(default=0, choices=STATUS.items())
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    # img = models.FileField(
    #     upload_to='./upload/img/category/', verbose_name='上传图片')

    class Meta:
        # verbose_name_plural为指定名称的复数类
        verbose_name_plural = verbose_name = u'分类'
        ordering = ['rank', '-create_time']
        # app_label = string_with_title('blog', '博客管理')

    def __str__(self):
        return self.name


class Post(models.Model):
    """新建一个模型,实际上就是一个映射关系，这边是实体，应该可以自动创建数据库字段和表，django的ORM不知道工作原理"""
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='作者', on_delete=models.SET_NULL)
    category = models.ForeignKey(
        Category, verbose_name='分类', default=None, blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200, verbose_name='标题')

    context = models.TextField(verbose_name='正文', default='')
    # 根据分类自动添加图片
    # img = models.CharField(max_length=200,default='/static/img/article/default')
    summary = models.CharField(max_length=200, verbose_name='摘要', default='')

    created_date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    published_date = models.DateTimeField(
        blank=True, null=True, verbose_name='发布时间')

    viewsum = models.IntegerField(default=0, verbose_name='浏览量')

    commentsnum = models.IntegerField(default=0, verbose_name='评论量')

    likenum = models.IntegerField(default=0, verbose_name='点赞数')

    # 可以自动读取已存在标签
    tags = TagField(verbose_name='标签', help_text='用逗号分隔')

    is_top = models.BooleanField(default=False, verbose_name='置顶')

    rank = models.IntegerField(default=0,)

    status = models.IntegerField(default=0, choices=STATUS.items())

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def browseadd(self):
        '''更新浏览数'''
        self.viewsum += 1
        self.save()

    def commentadd(self):
        '''更新评论数'''
        self.commentsnum += 1
        self.save()

    def likeunmadd(self):
        '''更新点赞数'''
        self.likenum += 1
        self.save()

    class Meta:
        verbose_name_plural = verbose_name = u"文章"
        ordering = ['-is_top', 'rank',  '-published_date', '-created_date']
        # app_label = string_with_title('blog', '博客管理')

    def __str__(self):
        return self.title
