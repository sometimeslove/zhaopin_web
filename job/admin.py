from django.contrib import admin
# Register your models here.
from company.models import Company
from .models import Job, Category, Tag
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.utils.html import format_html




class JobForm(forms.ModelForm):
    # body = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = Job
        fields = (
         'job_name', 'company', 'summary', 'job_body', 'education', 'job_experience', 'job_place',
     'full_part_flag','pub_status', 'job_status', 'salary_range',
      'author',  'job_sortorder', 'category','tags')


def makr_article_publish(modeladmin, request, queryset):
    queryset.update(pub_status='p')


def draft_article(modeladmin, request, queryset):
    queryset.update(pub_status='d')


def close_article_commentstatus(modeladmin, request, queryset):
    queryset.update(pub_status='c')


def open_article_commentstatus(modeladmin, request, queryset):
    queryset.update(pub_status='o')


makr_article_publish.short_description = '发布选中文章'
draft_article.short_description = '选中文章设置为草稿'
close_article_commentstatus.short_description = '关闭文章评论'
open_article_commentstatus.short_description = '打开文章评论'


class JobAdmin(admin.ModelAdmin):
    list_per_page = 20
    search_fields = ('body', 'job_name')
    form = JobForm
    list_display = (
         'job_name', 'company',  'education', 'job_experience', 'job_place',
     'full_part_flag', 'pub_status', 'job_status', 'salary_range',
      'author',  'job_sortorder', 'category')
    # , 'full_part_flag'
    # , 'pub_time', 'pub_status', 'job_status', 'salary_range', 'job_sortorder', 'category'
    list_display_links = ( 'job_name',)
    list_filter = ('pub_status','category', 'tags')
    filter_horizontal = ('tags',)
    # exclude = ('created_time', 'last_mod_time')
    view_on_site = True
    actions = [makr_article_publish, draft_article, close_article_commentstatus, open_article_commentstatus]

    def link_to_category(self, obj):
        info = (obj.category._meta.app_label, obj.category._meta.model_name)
        link = reverse('admin:%s_%s_change' % info, args=(obj.category.id,))
        return format_html(u'<a href="%s">%s</a>' % (link, obj.category.name))

    link_to_category.short_description = '分类目录'

    def get_form(self, request, obj=None, **kwargs):
        form = super(JobAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['author'].queryset = get_user_model().objects.filter(is_superuser=True)
        form.base_fields['company'].queryset = Company.objects
        return form

    def save_model(self, request, obj, form, change):
        super(JobAdmin, self).save_model(request, obj, form, change)

    def get_view_on_site_url(self, obj=None):
        if obj:
            url = obj.get_full_url()
            return url
        else:
            from yihang_website.utils import get_current_site
            site = get_current_site().domain
            return site


class TagAdmin(admin.ModelAdmin):
    exclude = ('slug', 'last_mod_time', 'created_time')


class CategoryAdmin(admin.ModelAdmin):
    exclude = ('slug', 'last_mod_time', 'created_time')

