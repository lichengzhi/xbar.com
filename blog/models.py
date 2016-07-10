# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from tagging.models import Tag
from tagging.fields import TagField
from tagging.registry import register

POST_STATUS = {
        0: u'草稿',
        1: u'发布',
        2: u'删除',
}
CATALOGUE_STATUS = {
        0: u'ENABLE',
        1: u'DISABLE',
        
}
ANSW_TYPE = {
        0: u'public',
        1: u'private',
        2: u'instant',
        
}
EDITOR = [
    u'tinyMCE',
    u'MarkDown',
]


# 复写TagField的sava方法，让它不做任何事
class TagField_Mine(TagField):
    def _save(self, **kwargs):
        pass


# class Editor(models.Model):
#     name = models.CharField(max_length=20, primary_key=True)
#     avaliable = models.BooleanField(default=True)
#
#     def __str__(self):
#         return self.name


class User(AbstractUser):
    name = models.CharField(max_length=12)
    # editor_choice = models.ForeignKey(Editor, null=True, blank=True, default="tinyMCE")
    editor_choice = models.CharField(max_length=20, default='tinyMCE')
    avatar_path = models.ImageField(upload_to="/avatar", default="/static/image/avatar_default.jpg")
    num_gold = models.IntegerField(editable=True, default=0)
    num_diamond = models.IntegerField(editable=True, default=0)
	
	

    def __str__(self):
        return self.name


class Catalogue(models.Model):
   name = models.CharField(max_length=20, primary_key=True)
   owner = models.CharField(max_length=20)
   status = models.SmallIntegerField(default=1, choices=CATALOGUE_STATUS.items())  # 0为草稿，1为发布，2为删除
	
	
   def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    publish_time = models.DateTimeField(auto_now_add=True)  # 第一次保存时自动添加时间
    modify_time = models.DateTimeField(auto_now_add=True)  # 每次保存自动更新时间
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='post_author')
    content = models.TextField()
    catalogue = models.ForeignKey(Catalogue)
    tag = TagField_Mine()
    view_count = models.IntegerField(editable=False, default=0)
    status = models.SmallIntegerField(default=0, choices=POST_STATUS.items())  # 0为草稿，1为发布，2为删除
    # editor_choice = models.ForeignKey(Editor)
    editor_choice = models.CharField(max_length=20)
    price = models.IntegerField(editable=True,default=0) 
    likes = models.IntegerField(editable=False,default=0)
    dislikes = models.IntegerField(editable=False,default=0)
    viewers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='post_viewers')
    score = models.IntegerField(editable=False,default=0)
    def __str__(self):
        return self.title

    def get_tags(self):
        return Tag.objects.get_for_object(self)

    def update_tags(self, tag_name):
        # 把list转为string
        tag_str = "".join(tag_name)
        Tag.objects.update_tags(self, tag_str)

    def remove_tags(self):
        Tag.objects.update_tags(self, None)
    def get_absolute_url(self):
        return "/post/%i/" % self.id

    class Meta:
        ordering = ['-modify_time']

class Question(models.Model):
    title = models.CharField(max_length=100)
    publish_time = models.DateTimeField(auto_now_add=True)  # 第一次保存时自动添加时间
    modify_time = models.DateTimeField(auto_now_add=True)  # 每次保存自动更新时间
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='question_author')
    content = models.TextField()
    catalogue = models.ForeignKey(Catalogue)
    tag = TagField_Mine()
    view_count = models.IntegerField(editable=False, default=0)
    status = models.SmallIntegerField(default=0, choices=POST_STATUS.items())  # 0为草稿，1为发布，2为删除
    # editor_choice = models.ForeignKey(Editor)
    editor_choice = models.CharField(max_length=20)
    price = models.IntegerField(editable=True,default=0) 
    likes = models.IntegerField(editable=False,default=0)
    dislikes = models.IntegerField(editable=False,default=0)
    viewers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='question_viewers')
    score = models.IntegerField(editable=False,default=0)
    def __str__(self):
        return self.title

    def get_tags(self):
        return Tag.objects.get_for_object(self)

    def update_tags(self, tag_name):
        # 把list转为string
        tag_str = "".join(tag_name)
        Tag.objects.update_tags(self, tag_str)

    def remove_tags(self):
        Tag.objects.update_tags(self, None)
    def get_absolute_url(self):
        return "/post/%i/" % self.id

    class Meta:
        ordering = ['-modify_time']
        
        
class Answer(models.Model):
    
    publish_time = models.DateTimeField(auto_now_add=True)  # 第一次保存时自动添加时间
    modify_time = models.DateTimeField(auto_now_add=True)  # 每次保存自动更新时间
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='answer_author')
    question = models.ForeignKey(Question)
    content = models.TextField()
    catalogue = models.ForeignKey(Catalogue)
    status = models.SmallIntegerField(default=0, choices=POST_STATUS.items())  # 0为草稿，1为发布，2为删除
    type = models.SmallIntegerField(default=0, choices=ANSW_TYPE.items())  
    # editor_choice = models.ForeignKey(Editor)
    editor_choice = models.CharField(max_length=20)
    
    score = models.IntegerField(editable=False,default=0)
  
 
    def get_absolute_url(self):
        return "/post/%i/" % self.id

    class Meta:
        ordering = ['-modify_time']
        
        
class Comment(models.Model):
    post = models.ForeignKey(Post)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    publish_Time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    content = models.TextField()
    root_id = models.IntegerField(default=0)  # 评论的最上层评论，若该评论处于最上层，则为0，
    parent_id = models.IntegerField(default=0)  # 评论的父评论，若无父评论，则为0

    def __str__(self):
        return self.content


class Carousel(models.Model):
    title = models.CharField(max_length=100)
    img = models.ImageField(upload_to="/carousel")
    post = models.ForeignKey(Post)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-create_time']


# 知识库模型
class Repository(models.Model):
    title = models.CharField(max_length=100)
    publish_time = models.DateTimeField(auto_now_add=True)  # 第一次保存时自动添加时间
    author = models.CharField(max_length=20)
    content = models.TextField()
    tag = models.ManyToManyField(Tag, blank=True, default="")  # 外键tag可为空，外键被删除时该值设定为默认值“”
    view_count = models.IntegerField(editable=False, default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publish_time']


register(Post)