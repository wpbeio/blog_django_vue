# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, Http404, StreamingHttpResponse
from django.views.generic import View
from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied
from django.contrib import auth
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
# from django.contrib.sites.models import get_current_site
from django.utils.http import (base36_to_int, is_safe_url,
                               urlsafe_base64_decode, urlsafe_base64_encode)
from .forms import UserCreationForm, PasswordRestForm
from django.core.files.base import ContentFile
from .models import BeioUser
from beio_system.models import Notification
import time
import datetime
from PIL import Image
import os
import json
import base64
import logging


logger = logging.getLogger(__name__)

# Create your views here.


# def big_file_download(request):
#     # do something...

#     def file_iterator(file_name, chunk_size=512):
#         with open(file_name) as f:
#             while True:
#                 c = f.read(chunk_size)
#                 if c:
#                     yield c
#                 else:
#                     break

#     the_file_name = "upload/2017/03/01/haha.docx"
#     response = StreamingHttpResponse(file_iterator(the_file_name))
#     response['Content-Type'] = 'application/octet-stream'
#     response['Content-Disposition'] = 'attachment;filename="{0}"'.format(
#         the_file_name)

#     return response


class UserControl(View):

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        if slug == "logout":
            return self.logout(request)

        return render(request, 'beio_auth/' + slug + '.html')

        raise PermissionDenied

    def post(self, request, *args, **kwargs):
        # 获取要对用户进行什么操作
        slug = self.kwargs.get('slug')

        if slug == 'login':
            return self.login(request)
        elif slug == "logout":
            return self.logout(request)
        elif slug == "register":
            return self.register(request)
        elif slug == "changepassword":
            return self.changepassword(request)
        elif slug == "forgetpassword":
            return self.forgetpassword(request)
        elif slug == "changetx":
            return self.changetx(request)
        elif slug == "resetpassword":
            return self.resetpassword(request)
        elif slug == "notification":
            return self.notification(request)

        raise PermissionDenied

    def login(self, request):
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = auth.authenticate(username=username, password=password)

        errors = []

        if user is not None and user.is_active:
            auth.login(request, user)
        else:
            errors.append(u"密码或者用户名不正确")

        mydict = {"errors": errors}
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )

    def logout(self, request):
        if not request.user.is_authenticated():
            logger.error(u'[UserControl]用户未登陆')
            raise PermissionDenied
        else:
            auth.logout(request)
            return HttpResponse(u"账号已退出", status=200)

    def register(self, request):
        username = self.request.POST.get("username", "")
        password1 = self.request.POST.get("password1", "")
        password2 = self.request.POST.get("password2", "")
        email = self.request.POST.get("email", "")

        form = UserCreationForm(request.POST)

        errors = []
        # 验证表单是否正确
        if form.is_valid():

            try:
                new_user = form.save()
                current_site = request.get_host()
                token = default_token_generator(new_user)
                title = u"欢迎来到 {} ！".format(settings.WEBSITE_TITLE)
                message = "".join([
                    u"你好！ {} ,感谢注册 {} ！\n\n".format(username, current_site),
                    u"请牢记以下信息：\n",
                    u"用户名：{}\n".format(username),
                    u"邮箱：{}\n".format(email),
                    u"网站：http://{}\n\n".format(settings.DOMAIN),
                    u'请访问该链接，完成用户验证:'.join(
                        [settings.DOMAIN, 'activate', token])
                ])
                from_email = settings.DEFAULT_FROM_EMAIL
                logger.info(current_site)

                new_user.email_user(title, message, from_email)
                '''登陆系统'''
                user = auth.authenticate(username=username, password=password2)
                auth.login(request, user)
            except Exception as e:
                logger.error(
                    u'[UserControl]用户注册邮件发送失败:[{}]/[{}]'.format(
                        username, email
                    )
                )
                return HttpResponse(u"发送邮件错误!\n注册失败", status=500)

        else:
            # 如果表单不正确,保存错误到errors列表中
            for k, v in form.errors.items():
                # v.as_text() 详见django.forms.util.ErrorList 中
                errors.append(v.as_text())

        mydict = {"errors": errors}
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )

    def changepassword(self, request):
        if not request.user.is_authenticated():
            logger.error(u'[UserControl]用户未登陆')
            raise PermissionDenied

        form = PasswordChangeForm(request.user, request.POST)

        errors = []
        # 验证表单是否正确
        if form.is_valid():
            user = form.save()
            auth.logout(request)
        else:
            # 如果表单不正确,保存错误到errors列表中
            for k, v in form.errors.items():
                # v.as_text() 详见django.forms.util.ErrorList 中
                errors.append(v.as_text())

        mydict = {"errors": errors}
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )

    def forgetpassword(self, request):
        username = self.request.POST.get("username", "")
        email = self.request.POST.get("email", "")

        form = PasswordRestForm(request.POST)

        errors = []

        # 验证表单是否正确
        if form.is_valid():
            token_generator = default_token_generator
            from_email = None
            opts = {
                'token_generator': token_generator,
                'from_email': from_email,
                'request': request,
            }
            user = form.save(**opts)

        else:
            # 如果表单不正确,保存错误到errors列表中
            for k, v in form.errors.items():
                # v.as_text() 详见django.forms.util.ErrorList 中
                errors.append(v.as_text())

        mydict = {"errors": errors}
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )

    def resetpassword(self, request):
        uidb64 = self.request.POST.get("uidb64", "")
        token = self.request.POST.get("token", "")
        password1 = self.request.POST.get("password1", "")
        password2 = self.request.POST.get("password2", "")

        try:
            uid = urlsafe_base64_decode(uidb64)
            user = BeioUser._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, BeioUser.DoesNotExist):
            user = None

        token_generator = default_token_generator

        if user is not None and token_generator.check_token(user, token):
            form = SetPasswordForm(user, request.POST)
            errors = []
            if form.is_valid():
                user = form.save()
            else:
                # 如果表单不正确,保存错误到errors列表中
                for k, v in form.errors.items():
                    # v.as_text() 详见django.forms.util.ErrorList 中
                    errors.append(v.as_text())

            mydict = {"errors": errors}
            return HttpResponse(
                json.dumps(mydict),
                content_type="application/json"
            )
        else:
            logger.error(
                u'[UserControl]用户重置密码连接错误:[{}]/[{}]'.format(
                    uid64, token
                )
            )
            return HttpResponse(
                u"密码重设失败!\n密码重置链接无效，可能是因为它已使用。可以请求一次新的密码重置.",
                status=403
            )

    def changetx(self, request):
        if not request.user.is_authenticated():
            logger.error(u'[UserControl]用户未登陆')
            raise PermissionDenied

        # 本地保存头像
        data = request.POST['tx']
        # file_content = ContentFile(request.FILES['upload_tx'].read())
        # img = request.FILES['upload_tx']
        if not data:
            logger.error(
                u'[UserControl]用户上传头像为空:[%s]'.format(
                    request.user.username
                )
            )
            return HttpResponse(u"上传头像错误", status=500)

        imgData = base64.b64decode(data)
        filename = "images/tx/tx_100x100_{}.jpg".format(request.user.id)
        filedir = "media/"

        if not os.path.exists(filedir):
            os.makedirs(filedir)
        # baseDir = os.path.dirname(os.path.abspath(__name__))
        path = os.path.join(filedir, filename)

        # path = "media/images/tx/tx_100x100_{}.jpg".format(request.user.id)
        try:
            with open(path, 'wb+')as destination:
                destination.write(imgData)

            im = Image.open(path)
            out = im.resize((100, 100), Image.ANTIALIAS)
            out.save(path)
            request.user.img = "/media/" + filename
            request.user.save()
            return HttpResponse(u"上传头像成功!\n")
        # file = open(path, "wb+")
        # file.write(imgData)
        # file.flush()
        # file.close()

        # 修改头像分辨率
        except Exception as e:
            if not os.path.exists(path):
                logger.error(
                    u'[UserControl]用户上传头像出错:[{}]'.format(
                        request.user.username
                    )
                )
            return HttpResponse(u"上传头像错误", status=500)

        # # 选择上传头像到七牛还是本地
        # try:
        #     # 上传头像到七牛
        #     import qiniu

        #     qiniu_access_key = settings.QINIU_ACCESS_KEY
        #     qiniu_secret_key = settings.QINIU_SECRET_KEY
        #     qiniu_bucket_name = settings.QINIU_BUCKET_NAME

        #     assert qiniu_access_key and qiniu_secret_key and qiniu_bucket_name
        #     q = qiniu.Auth(qiniu_access_key, qiniu_secret_key)

        #     key = filename
        #     localfile = path

        #     mime_type = "text/plain"
        #     params = {'x:a': 'a'}

        #     token = q.upload_token(qiniu_bucket_name, key)
        #     ret, info = qiniu.put_file(token, key, localfile,
        #                                mime_type=mime_type, check_crc=True)

        #     # 图片连接加上 v?时间  是因为七牛云缓存，图片不能很快的更新，
        #     # 用filename?v201504261312的形式来获取最新的图片
        #     request.user.img = "http://{}/{}?v{}".format(
        #         settings.QINIU_URL,
        #         filename,
        #         time.strftime('%Y%m%d%H%M%S')
        #     )
        #     request.user.save()

        #     # 验证上传是否错误
        #     if ret['key'] != key or ret['hash'] != qiniu.etag(localfile):
        #         logger.error(
        #             u'[UserControl]上传头像错误：[{}]'.format(
        #                 request.user.username
        #             )
        #         )
        #         return HttpResponse(u"上传头像错误", status=500)

        #     return HttpResponse(u"上传头像成功!\n(注意有10分钟缓存)")

        # except Exception as e:
        #     request.user.img = "/static/images/tx/" + filename
        #     request.user.save()

        #     # 验证上传是否错误
        #     if not os.path.exists(path):
        #         logger.error(
        #             u'[UserControl]用户上传头像出错:[{}]'.format(
        #                 request.user.username
        #             )
        #         )
        #         return HttpResponse(u"上传头像错误", status=500)

        #     return HttpResponse(u"上传头像成功!\n(注意有10分钟缓存)")

    def notification(self, request):
        if not request.user.is_authenticated():
            logger.error(u'[UserControl]用户未登陆')
            raise PermissionDenied

        notification_id = self.request.POST.get("notification_id", "")
        notification_id = int(notification_id)

        notification = Notification.objects.filter(
            pk=notification_id
        ).first()

        if notification:
            notification.is_read = True
            notification.save()
            mydict = {"url": notification.url}
            print(mydict)
        else:
            mydict = {"url": '#'}

        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )
