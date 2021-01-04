from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.conf import settings
from django import forms
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from company.models import Company
from yihang_website.utils import cache
from django.shortcuts import get_object_or_404
from job.models import Job, Category, Tag
import logging

logger = logging.getLogger(__name__)

class CompanyListView(ListView):
    # template_name属性用于指定使用哪个模板进行渲染
    template_name = 'company/company_view_list.html'

    # context_object_name属性用于给上下文变量取名（在模板中使用该名字）
    context_object_name = 'company_list'

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

    def get_queryset_cache_key(self):
        cache_key = 'company_{page}'.format(page=self.page_number)
        return cache_key

    def get_queryset_data(self):
        company_list = Company.objects.all()
        return company_list

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
            company_list = self.get_queryset_data()
            cache.set(cache_key, company_list)
            logger.info('set view cache.key:{key}'.format(key=cache_key))
            return company_list

    def get_queryset(self):
        '''
        重写默认，从缓存获取数据
        :return:
        '''
        key = self.get_queryset_cache_key()
        value = self.get_queryset_from_cache(key)
        return value

    def get_context_data(self, **kwargs):

        return super(CompanyListView, self).get_context_data(**kwargs)


class CompanyDetailView(DetailView):
    '''
    文章详情页面
    '''
    template_name = 'company/company_detail.html'
    model = Company
    pk_url_kwarg = 'company_id'
    context_object_name = "company"

    def get_object(self, queryset=None):
        obj = super(CompanyDetailView, self).get_object()
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
        jobs = Job.objects.all()
        kwargs['job_list'] = jobs
        return super(CompanyDetailView, self).get_context_data(**kwargs)