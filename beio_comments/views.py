# -*- coding: utf-8 -*-
import logging
import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic  import View,ListView,DetailView,TemplateView
from django.core.exceptions import PermissionDenied
from .models import Comment
# from notifications.signals import notify
from beio_blog.models import Post
from django.contrib.auth.decorators import login_required


PostModel = Post
# logger
logger = logging.getLogger(__name__)


# # Create your views here.
# def latest_comments_list(request):
#     comments =  Comment.objects.order_by("-create_time")[0:10]
#     return render(request, 'comments/latest_comments.html', {'latest_comment_list': comments})
# def comment_list(request, slug):
#     comments = Post.objects.get(pk=slug).comment_set.all()
#     return render(request, 'comments/comments.html', {'comment_list': comments})

# class IndexView(TemplateView):
#     """展示前十名评论"""

#     template_name='latest_comments.html'

#     def get_context_data(self,**kwargs):
#         context = super(IndexView, self).get_context_data(**kwargs)
#         context['latest_comment_list'] =  Comment.objects.order_by("-create_time")[0:10]
#         return context

# class CommentView(TemplateView):
#     template_name = 'comments.html'

#     def get_context_data(self,**kwargs):
#         #在需要的comment.html 的View中 要加入 comment_list
#         pk=self.kwargs.get('pk','')
#         context['comment_list'] = Post.objects.get(pk=pk).comment_set.all()
#         return super(ComengtView,self).get_context_data(**kwargs

class CommentControl(View):
    # @login_required
    def post(self, request, *args, **kwargs):
        # 获取当前用户
        user = self.request.user
        # 获取评论
        text = self.request.POST.get("comment", "")
        # 判断当前用户是否是活动的用户
        if not user.is_authenticated():
            logger.error(
                u'[CommentControl]当前用户非活动用户:[{}]'.format(
                    user.username
                )
            )
            return HttpResponse(u"请登陆！", status=403)

        pk = self.kwargs.get('slug', '')
        try:
            # 默认使用pk来索引(也可根据需要使用title,en_title在索引
            post = PostModel.objects.get(pk=pk)
        except PostModel.DoesNotExist:
            logger.error(u'[CommentControl]此文章不存在:[%s]' % pk)
            raise PermissionDenied

        # 保存评论,使用消息组件进行推送消息
        parent = None
        if text.startswith('@['):
            import ast
            parent_str = text[1:text.find(':')]
            parent_id = ast.literal_eval(parent_str)[1]
            text = text[text.find(':')+2:]
            try:
                parent = Comment.objects.get(pk=parent_id)
                info = u'{}回复了你在 {} 的评论'.format(
                    user.username,
                    parent.post.title
                )

                Notification.objects.create(
                    title=info,
                    text=text,
                    from_user=user,
                    to_user=parent.user,
                    url='/post/'+pk+'.html'
                )
            except Comment.DoesNotExist:
                logger.error(u'[CommentControl]评论引用错误:%s' % parent_str)
                return HttpResponse(u"请勿修改评论代码！", status=403)

        if not text:
            logger.error(
                u'[CommentControl]当前用户输入空评论:[{}]'.format(
                    user.username
                )
            )
            return HttpResponse(u"请输入评论内容！", status=403)

        comment = Comment.objects.create(
            user=user,
            post=post,
            text=text,
            parent=parent
        )

        comment.post.commentadd()
        try:
            img = comment.user.img
        except Exception as e:
            img = "http://vmaig.qiniudn.com/image/tx/tx-default.jpg"

        print_comment = u"<p>评论：{}</p>".format(text)
        if parent:
            print_comment = u"<div class=\"comment-quote\">\
                                  <p>\
                                      <a>@{}</a>\
                                      {}\
                                  </p>\
                              </div>".format(
                parent.user.username,
                parent.text
            ) + print_comment
        # 返回当前评论
        html = u"<li>\
                    <div class=\"vmaig-comment-tx\">\
                        <img src={} width=\"40\"></img>\
                    </div>\
                    <div class=\"vmaig-comment-content\">\
                        <a><h1>{}</h1></a>\
                        {}\
                        <p>{}</p>\
                    </div>\
                </li>".format(
            img,
            comment.user.username,
            print_comment,
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        return HttpResponse(html)
