from django.contrib import admin
from django import forms
from django.urls import reverse
from django.utils.html import format_html

from company.models import Company


class CompanyForm(forms.ModelForm):
    # body = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = Company
        fields = ('company_id', 'company_name', 'company_scale', 'company_finance', 'company_class', 'company_place')


# Register your models here.
class CompanyAdmin(admin.ModelAdmin):
    list_per_page = 20
    search_fields = ('body', 'job_name')
    form = CompanyForm
    list_display = (
         'company_id', 'company_name', 'company_scale', 'company_finance', 'company_class', 'company_place')
    # , 'full_part_flag'
    # , 'pub_time', 'pub_status', 'job_status', 'salary_range', 'job_sortorder', 'category'
    list_display_links = ('company_id', 'company_name')
    list_filter = ('company_tags','company_scale', 'company_finance')
    filter_horizontal = ('company_tags',)
    # exclude = ('created_time', 'last_mod_time')
    view_on_site = True
    # actions = [makr_article_publish, draft_article, close_article_commentstatus, open_article_commentstatus]

    def link_to_category(self, obj):
        info = (obj.category._meta.app_label, obj.category._meta.model_name)
        link = reverse('admin:%s_%s_change' % info, args=(obj.category.id,))
        return format_html(u'<a href="%s">%s</a>' % (link, obj.category.name))

    link_to_category.short_description = '分类目录'

    def get_form(self, request, obj=None, **kwargs):
        form = super(CompanyAdmin, self).get_form(request, obj, **kwargs)
        return form

    def save_model(self, request, obj, form, change):
        super(CompanyAdmin, self).save_model(request, obj, form, change)

    def get_view_on_site_url(self, obj=None):
        if obj:
            url = obj.get_full_url()
            return url
        else:
            from yihang_website.utils import get_current_site
            site = get_current_site().domain
            return site
