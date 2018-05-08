# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-23 17:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('url', models.CharField(blank=True, max_length=200, null=True, verbose_name='连接')),
                ('type', models.CharField(blank=True, max_length=20, null=True, verbose_name='类型')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '友情链接',
                'ordering': ['-create_time'],
                'verbose_name_plural': '友情链接',
            },
        ),
        migrations.CreateModel(
            name='Nav',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='导航条内容')),
                ('url', models.CharField(blank=True, max_length=200, null=True, verbose_name='指向地址')),
                ('status', models.IntegerField(choices=[(0, '开启'), (1, '关闭')], default=0, verbose_name='状态')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '导航条',
                'ordering': ['-create_time'],
                'verbose_name_plural': '导航条',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('text', models.TextField(verbose_name='内容')),
                ('url', models.CharField(blank=True, max_length=200, null=True, verbose_name='连接')),
                ('type', models.CharField(blank=True, max_length=20, null=True, verbose_name='类型')),
                ('is_read', models.IntegerField(choices=[(0, '未读'), (1, '已读')], default=0, verbose_name='是否读过')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('from_user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='from_user_notification_set', to=settings.AUTH_USER_MODEL, verbose_name='发送者')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user_notification_set', to=settings.AUTH_USER_MODEL, verbose_name='接收者')),
            ],
            options={
                'verbose_name': '消息',
                'ordering': ['-create_time'],
                'verbose_name_plural': '消息',
            },
        ),
    ]