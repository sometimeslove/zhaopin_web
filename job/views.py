from django.core.paginator import Paginator
from django.shortcuts import render

from django.shortcuts import render

# Create your views here.
import os
import datetime
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.conf import settings
from django import forms
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from yihang_website.utils import cache
from django.shortcuts import get_object_or_404
from job.models import Job, Category, Tag
import logging
from django.urls import reverse

logger = logging.getLogger(__name__)


class JobListView(ListView):
    # template_name属性用于指定使用哪个模板进行渲染
    template_name = 'job/job_list.html'

    # context_object_name属性用于给上下文变量取名（在模板中使用该名字）
    context_object_name = 'job_list'

    # 页面类型，分类目录或标签列表等
    page_type = ''
    paginate_by = settings.PAGINATE_BY
    page_kwarg = 'page'
    link_type = 'l'

    def get_view_cache_key(self):
        return self.request.get['pages']

    @property
    def page_number(self):
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        return page


    def get_queryset_data(self):
        job_list = Job.objects.filter(pub_status='p')
        return job_list

    def get_queryset_cache_key(self):
        cache_key = 'list_{page}'.format(page=self.page_number)
        return cache_key

    def get_queryset_from_cache(self, cache_key):
        '''
        缓存页面数据
        :param cache_key: 缓存key
        :return:
        '''
        value = cache.get(cache_key)
        if value:
            logger.info('get view cache.key:{key}'.format(key=cache_key))
            return value
        else:
            job_list = self.get_queryset_data()
            cache.set(cache_key, job_list)
            logger.info('set view cache.key:{key}'.format(key=cache_key))
            return job_list

    def get_queryset(self):
        '''
        重写默认，从缓存获取数据
        :return:
        '''
        key = self.get_queryset_cache_key()
        value = self.get_queryset_from_cache(key)
        return value

    def get_context_data(self, **kwargs):
        kwargs['morejobs'] = reverse('job:job_page', kwargs={'page': 1})
        return super(JobListView, self).get_context_data(**kwargs)


class IndexView(JobListView):
    '''
    首页
    '''
    # 友情链接类型
    link_type = 'i'

    # template_name属性用于指定使用哪个模板进行渲染
    template_name = 'job/job_index.html'

    # context_object_name属性用于给上下文变量取名（在模板中使用该名字）
    context_object_name = 'job_list'


    def get_queryset_data(self):
        job_list = Job.objects.filter(pub_status='p')[:6]
        return job_list

    def get_queryset_cache_key(self):
        cache_key = 'index_{page}'.format(page=self.page_number)
        return cache_key

    # def get_context_data(self, **kwargs):
    #     job_list = Job.objects.all()
    #     paginator = Paginator(job_list, 2)
    #     if pindex == "":  # django中默认返回空值，所以加以判断，并设置默认值为1
    #         pindex = 1
    #     else:  # 如果有返回在值，把返回值转为整数型
    #         int(pindex)
    #     page = paginator.page(pindex)  # 传递当前页的实例对象到前端
    #     kwargs['morejobs'] = reverse('job:job_page', kwargs={'page': 1})
    #     return super(JobListView, self).get_context_data(**kwargs)


class JobDetailView(DetailView):
    '''
    文章详情页面
    '''
    template_name = 'job/job_detail.html'
    model = Job
    pk_url_kwarg = 'job_id'
    context_object_name = "job"

    def get_object(self, queryset=None):
        obj = super(JobDetailView, self).get_object()
        obj.viewed()
        return obj

    def get_context_data(self, **kwargs):
        # jobid = int(self.kwargs[self.pk_url_kwarg])
        # comment_form = CommentForm()
        # user = self.request.user
        # # 如果用户已经登录，则隐藏邮件和用户名输入框
        # if user.is_authenticated and not user.is_anonymous and user.email and user.username:
        #     comment_form.fields.update({
        #         'email': forms.CharField(widget=forms.HiddenInput()),
        #         'name': forms.CharField(widget=forms.HiddenInput()),
        #     })
        #     comment_form.fields["email"].initial = user.email
        #     comment_form.fields["name"].initial = user.username
        #
        # article_comments = self.object.comment_list()
        #
        # kwargs['form'] = comment_form
        # kwargs['article_comments'] = article_comments
        # kwargs['comment_count'] = len(article_comments) if article_comments else 0
        #
        # kwargs['next_article'] = self.object.next_article
        # kwargs['prev_article'] = self.object.prev_article

        return super(JobDetailView, self).get_context_data(**kwargs)



class CategoryDetailView(JobListView):
    '''
    分类目录列表
    '''
    page_type = "分类目录归档"

    def get_queryset_data(self):
        slug = self.kwargs['category']
        category = get_object_or_404(Category, slug=slug)

        categoryname = category.name
        self.categoryname = categoryname
        categorynames = list(map(lambda c: c.name, category.get_sub_categorys()))
        article_list = Job.objects.filter(category__name__in=categorynames, status='p')
        return article_list

    def get_queryset_cache_key(self):
        slug = self.kwargs['category_name']
        category = get_object_or_404(Category, slug=slug)
        categoryname = category.name
        self.categoryname = categoryname
        cache_key = 'category_list_{categoryname}_{page}'.format(categoryname=categoryname, page=self.page_number)
        return cache_key

    def get_context_data(self, **kwargs):

        categoryname = self.categoryname
        try:
            categoryname = categoryname.split('/')[-1]
        except:
            pass
        kwargs['page_type'] = CategoryDetailView.page_type
        kwargs['tag_name'] = categoryname
        return super(CategoryDetailView, self).get_context_data(**kwargs)


class AuthorDetailView(JobListView):
    '''
    作者详情页
    '''
    page_type = '作者文章归档'

    def get_queryset_cache_key(self):
        author_name = self.kwargs['author_name']
        cache_key = 'author_{author_name}_{page}'.format(author_name=author_name, page=self.page_number)
        return cache_key

    def get_queryset_data(self):
        author_name = self.kwargs['author_name']
        job_list = Job.objects.filter(author__username=author_name, type='a', status='p')
        return job_list

    def get_context_data(self, **kwargs):
        author_name = self.kwargs['author_name']
        kwargs['page_type'] = AuthorDetailView.page_type
        kwargs['tag_name'] = author_name
        return super(AuthorDetailView, self).get_context_data(**kwargs)


class TagDetailView(JobListView):
    '''
    标签列表页面
    '''
    page_type = '分类标签归档'

    def get_queryset_data(self):
        slug = self.kwargs['tag_name']
        tag = get_object_or_404(Tag, slug=slug)
        tag_name = tag.name
        self.name = tag_name
        job_list = Job.objects.filter(tags__name=tag_name, type='a', status='p')
        return job_list

    def get_queryset_cache_key(self):
        slug = self.kwargs['tag_name']
        tag = get_object_or_404(Tag, slug=slug)
        tag_name = tag.name
        self.name = tag_name
        cache_key = 'tag_{tag_name}_{page}'.format(tag_name=tag_name, page=self.page_number)
        return cache_key

    def get_context_data(self, **kwargs):
        # tag_name = self.kwargs['tag_name']
        tag_name = self.name
        kwargs['page_type'] = TagDetailView.page_type
        kwargs['tag_name'] = tag_name
        return super(TagDetailView, self).get_context_data(**kwargs)


# class ArchivesView(ArticleListView):
#     '''
#     文章归档页面
#     '''
#     page_type = '文章归档'
#     paginate_by = None
#     page_kwarg = None
#     template_name = 'blog/article_archives.html'
#
#     def get_queryset_data(self):
#         return Article.objects.filter(status='p').all()
#
#     def get_queryset_cache_key(self):
#         cache_key = 'archives'
#         return cache_key

