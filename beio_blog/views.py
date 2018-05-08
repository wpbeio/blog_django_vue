from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Post
from django.contrib import auth
from beio_comments.models import Comment
from .forms import PostForm
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import View, TemplateView, ListView, DetailView, FormView, DeleteView, CreateView
from beio_system.models import Link, Notification, Nav

import logging
from django.conf import settings


# logger
logger = logging.getLogger(__name__)


class BaseMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super(BaseMixin, self).get_context_data(**kwargs)
        try:
            # 网站标题等内容
            context['website_title'] = settings.WEBSITE_TITLE
            context['website_welcome'] = settings.WEBSITE_WELCOME
            # 热门文章
            context['hot_article_list'] = Post.objects.order_by(
                "-view_times")[0:10]
            # 导航条
            context['nav_list'] = Nav.objects.filter(status=0)
            # 最新评论
            context['latest_comment_list'] = Comment.objects.order_by(
                "-create_time")[0:10]
            # 友情链接
            context['links'] = Link.objects.order_by('create_time').all()
            colors = ['primary', 'success', 'info', 'warning', 'danger']
            for index, link in enumerate(context['links']):
                link.color = colors[index % len(colors)]
            # 用户未读消息数
            user = self.request.user
            if user.is_authenticated():
                context['notification_count'] = \
                    user.to_user_notification_set.filter(is_read=0).count()
        except Exception as e:
            logger.error(u'[BaseMixin]加载基本信息出错')

        return context


class IndexView(BaseMixin, ListView):
    """首页列表"""

    template_name = 'beio_blog/index.html'
    context_object_name = 'posts'
    model = Post
    paginate_by = 3
    # paginator_class = <class 'django.core.paginator.Paginator'>

    def get_queryset(self, *args, **kwargs):
        posts = Post.objects.filter(
            published_date__isnull=False).order_by('-published_date')
        # posts = Post.objects.order_by('-published_date')
        # paginator = Paginator(posts, 3)

        # page = self.kwargs.get('page',1)
        # try:
        #     posts = paginator.page(page)
        # except PageNotAnInteger:
        # # If page is not an integer, deliver first page.
        #     posts = paginator.page(1)
        # except EmptyPage:
        # # If page is out of range (e.g. 9999), deliver last page of results.
        #     posts = paginator.page(paginator.num_pages)
        return posts

    def get_context_data(self, **kwargs):
        kwargs['latest_comment_list'] = Comment.objects.order_by(
            '-create_time')[0:10]
        kwargs['page'] = True
        return super(IndexView, self).get_context_data(**kwargs)


class UserView(BaseMixin, TemplateView):
    template_name = 'beio_auth/login.html'

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        if slug in ["forgetpassword", "register", "login"]:
            self.template_name = "beio_auth/" + slug + ".html"
            return render(request, "beio_auth/" + slug + ".html")
        if not request.user.is_authenticated():
            logger.error(u'[UserView]用户未登陆')
            return render(request, 'beio_auth/login.html')
        if slug == "logout":
            auth.logout(request)
            return render(request, 'beio_auth/login.html')
        if slug in ["logout", "changepassword", "changetx"]:
            self.template_name = "beio_auth/" + slug + ".html"
            return render(request, "beio_auth/" + slug + ".html")
        return super(UserView, self).get(request, *args, **kwargs)
        logger.error(u'[UserView]不存在此接口')
        raise Http404

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)

        slug = self.kwargs.get('slug')

        if slug == 'notification':
            context['notifications'] = \
                self.request.user.to_user_notification_set.order_by(
                    '-create_time'
            ).all()

        return context


# def post_list(request):

#     posts = Post.objects.filter(
#         published_date__isnull=False).order_by('-published_date')
#     paginator = Paginator(posts, 3)

#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         # If page is not an integer, deliver first page.
#         posts = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range (e.g. 9999), deliver last page of results.
#         posts = paginator.page(paginator.num_pages)
#     return render(request, 'blog/post_list.html', {'posts': posts, 'page': True})


class Post_Detail_View(BaseMixin, DetailView):
    """详细页面视图"""
    model = Post
    template_name = 'beio_blog/post_detail.html'
    context_object_name = 'post'
    slug_field = 'pk'

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk', '')
        # 在需要vmaig_comment.html 的View中加入 comment_list
        kwargs['comment_list'] = Post.objects.get(pk=pk).comment_set.all()
        # 在需要的latest_comment.html 的view中 要加入 laset_comment_list
        kwargs['latest_comment_list'] = Comment.objects.order_by(
            "-create_time")[0:10]

        return super(Post_Detail_View, self).get_context_data(**kwargs)


class Post_Add_View(BaseMixin, FormView):
    template_name = 'beio_blog/post_edit.html'
    form_class = PostForm


class Post_Create_View(BaseMixin, CreateView):
    model = Post
    # template_name = 'beio_blog/post_detail.html'
    form_class = PostForm
    # success_url = reverse("post_detail", kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        if form.is_valid():
            post = form.save(commit=False)
            post.summary = post.context if post.summary == '' else post.context[0:15]
            post.author = self.request.user
            if request.POST['flag'] == '1':
                post.publish()
            else:
                post.save()
            # return redirect(reverse("post_detail", arg=(post.pk,)))
        return super(Post_new_view, self).form_valid(form)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment_list = Post.objects.get(pk=pk).comment_set.all()
    latest_comment_list = Comment.objects.order_by("-create_time")[0:10]
    post.browseadd()
    return render(request, 'beio_blog/post_detail.html', {'post': post, 'comment_list': comment_list, 'latest_comment_list': latest_comment_list})


@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():

            post = form.save(commit=False)
            post.summary = post.context if post.summary == '' else post.context[0:15]
            post.author = request.user
            if request.POST['flag'] == '1':
                post.publish()
            else:
                post.save()
            return redirect(reverse("post_detail", arg=(post.pk,)))
            # return render(request,'beio_blog/post_edit.html',)
    else:
        form = PostForm()
    return render(request, 'beio_blog/post_edit.html', {'form': form})


@login_required
def post_draft_list(request):

    posts = Post.objects.filter(
        published_date__isnull=True).order_by('-created_date')
    return render(request, 'beio_blog/post_draft_list.html', {'posts': posts})


@login_required
def post_publish(request, pk):

    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect(post_detail, pk=pk)


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('/')


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(post_detail, pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'beio_blog/post_edit.html', {'form': form})
