#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: superstrongz
@license: MIT Licence
@contact: 857508399@qq.com
@site: http://www.superstrongz.com/
@software: PyCharm
@file: blog_tags.py
@time: ??
"""

from django import template
from django.db.models import Q
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
import random
from django.urls import reverse

from company.models import Company
from job.models import Job
from django.utils.encoding import force_text
from django.shortcuts import get_object_or_404
import hashlib
import urllib
from yihang_website.utils import cache_decorator, cache
from django.contrib.auth import get_user_model
from yihang_website.utils import get_current_site
import logging

logger = logging.getLogger(__name__)

register = template.Library()


@register.simple_tag
def timeformat(data):
    try:
        return data.strftime(settings.TIME_FORMAT)
        # print(data.strftime(settings.TIME_FORMAT))
        # return "ddd"
    except Exception as e:
        logger.error(e)
        return ""

@register.simple_tag
def hourminuteformat(data):
    try:
        return data.strftime(settings.HOUR_MINUTE_FORMAT)
        # print(data.strftime(settings.TIME_FORMAT))
        # return "ddd"
    except Exception as e:
        logger.error(e)
        return ""

@register.simple_tag
def datetimeformat(data):
    try:
        return data.strftime(settings.DATE_TIME_FORMAT)
    except Exception as e:
        logger.error(e)
        return ""

# 判断该值是否除3后余数等于1
@register.filter(is_safe=True)
@stringfilter
def mod_three_one(num):
    return int(num)%3==1

# 判断该值是否除3后余数等于1
@register.filter(is_safe=True)
@stringfilter
def mod_three_zero(num):
    return num%3==0

@register.filter(is_safe=True)
@stringfilter
def custom_markdown(content):
    from yihang_website.utils import CommonMarkdown
    return mark_safe(CommonMarkdown.get_markdown(content))


@register.filter(is_safe=True)
@stringfilter
def truncatechars_content(content):
    """
    获得文章内容的摘要
    :param content:
    :return:
    """
    from django.template.defaultfilters import truncatechars_html
    from yihang_website.utils import get_blog_setting
    blogsetting = get_blog_setting()
    return truncatechars_html(content, blogsetting.article_sub_length)


@register.filter(is_safe=True)
@stringfilter
def truncate(content):
    from django.utils.html import strip_tags

    return strip_tags(content)[:150]



@register.inclusion_tag('job/tags/job_info.html')
def load_job_detail(job, isindex, user):
    """
    加载职位详情
    :param job:
    :param isindex:是否列表页，若是列表页只显示摘要
    :return:
    """
    # from yihang_website.utils import get_blog_setting
    # blogsetting = get_blog_setting()

    return {
        'job': job,
        'isindex': isindex,
        'user': user,
        'open_site_comment': "一行招聘",
        # 'open_site_comment': blogsetting.open_site_comment,
    }

@register.inclusion_tag('job/tags/joblist_info.html')
def load_joblist_info(job):
    """
    加载职位详情
    :param job:
    :param isindex:是否列表页，若是列表页只显示摘要
    :return:
    """
    # from yihang_website.utils import get_blog_setting
    # blogsetting = get_blog_setting()

    return {
        'job': job,
    }
@register.inclusion_tag('company/tags/company_list.html')
def load_company_list():
    """
    获得文章meta信息
    :param article:
    :return:
    """
    company_list = Company.objects.filter(state='0')[:8]
    return {
        'company_list': company_list
    }


@register.inclusion_tag('job/tags/job_pagination.html')
def load_pagination_info(page_obj, page_type, tag_name):
    previous_url = ''
    next_url = ''
    if page_type == '':
        if page_obj.has_next():
            next_number = page_obj.next_page_number()
            next_url = reverse('job:job_page', kwargs={'page': next_number})
        if page_obj.has_previous():
            previous_number = page_obj.previous_page_number()
            previous_url = reverse('job:job_page', kwargs={'page': previous_number})
    # if page_type == '分类标签归档':
    #     tag = get_object_or_404(Tag, name=tag_name)
    #     if page_obj.has_next():
    #         next_number = page_obj.next_page_number()
    #         next_url = reverse('blog:tag_detail_page', kwargs={'page': next_number, 'tag_name': tag.slug})
    #     if page_obj.has_previous():
    #         previous_number = page_obj.previous_page_number()
    #         previous_url = reverse('blog:tag_detail_page', kwargs={'page': previous_number, 'tag_name': tag.slug})
    # if page_type == '作者文章归档':
    #     if page_obj.has_next():
    #         next_number = page_obj.next_page_number()
    #         next_url = reverse('blog:author_detail_page', kwargs={'page': next_number, 'author_name': tag_name})
    #     if page_obj.has_previous():
    #         previous_number = page_obj.previous_page_number()
    #         previous_url = reverse('blog:author_detail_page', kwargs={'page': previous_number, 'author_name': tag_name})
    #
    # if page_type == '分类目录归档':
    #     category = get_object_or_404(Category, name=tag_name)
    #     if page_obj.has_next():
    #         next_number = page_obj.next_page_number()
    #         next_url = reverse('blog:category_detail_page',
    #                            kwargs={'page': next_number, 'category_name': category.slug})
    #     if page_obj.has_previous():
    #         previous_number = page_obj.previous_page_number()
    #         previous_url = reverse('blog:category_detail_page',
    #                                kwargs={'page': previous_number, 'category_name': category.slug})

    return {
        'previous_url': previous_url,
        'next_url': next_url,
        'page_obj': page_obj
    }


@register.inclusion_tag('job/tags/tag_link.html')
def load_tag_link():
    return {
    }


@register.inclusion_tag('share_layout/search.html')
def load_search():
    return {
    }

# return only the URL of the gravatar
# TEMPLATE USE:  {{ email|gravatar_url:150 }}
@register.filter
def gravatar_url(email, size=40):
    """获得gravatar头像"""
    cachekey = 'gravatat/' + email
    if cache.get(cachekey):
        return cache.get(cachekey)
    else:
        usermodels = OAuthUser.objects.filter(email=email)
        if usermodels:
            o = list(filter(lambda x: x.picture is not None, usermodels))
            if o:
                return o[0].picture
        email = email.encode('utf-8')

        default = "https://resource.lylinux.net/image/2017/03/26/120117.jpg".encode('utf-8')

        url = "https://www.gravatar.com/avatar/%s?%s" % (
            hashlib.md5(email.lower()).hexdigest(), urllib.parse.urlencode({'d': default, 's': str(size)}))
        cache.set(cachekey, url, 60 * 60 * 10)
        return url


@register.filter
def gravatar(email, size=40):
    """获得gravatar头像"""
    url = gravatar_url(email, size)
    return mark_safe('<img src="%s" height="%d" width="%d">' % (url, size, size))


@register.simple_tag
def query(qs, **kwargs):
    """ template tag which allows queryset filtering. Usage:
          {% query books author=author as mybooks %}
          {% for book in mybooks %}
            ...
          {% endfor %}
    """
    return qs.filter(**kwargs)
