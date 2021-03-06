from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.timezone import now
from uuslug import slugify
from yihang_website.utils import cache_decorator, cache, logger, get_current_site
from django.conf import settings
from mdeditor.fields import MDTextField
from django.core.exceptions import ValidationError


class Job(models.Model):
    """文章"""
    PUB_CHOICES = (
        ('d', '草稿'),
        ('p', '发布'),
    )
    JOB_CHOICES = (
        ('o', '在招'),
        ('c', '关闭'),
    )

    FULL_PART_FLAG = (
        ('0', '全职'),
        ('1', '兼职'),
    )

    EDUCATION_LIST = (
        ('a', '本科'),
        ('b', '硕士'),
        ('c', '博士'),
        ('z', '不限'),
    )
    EXPERIENCE_LIST = (
        ('a', '1年以内'),
        ('b', '1-3年'),
        ('c', '3-5年'),
        ('d', '5-8年'),
        ('e', '8年以上'),
        ('z', '不限'),
    )
    SALARY_RANGE = (
        ('a', '1k-5k'),
        ('b', '5k-10k'),
        ('c', '10k-15k'),
        ('d', '15k-20k'),
        ('e', '20k-30k'),
        ('f', '>30k'),
        ('z', '面议'),
    )
    job_id = models.AutoField(primary_key=True)
    job_name = models.CharField('标题', max_length=200, unique=True)
    # company_id = models.CharField('公司ID', max_length=20, blank=False)
    company =models.ForeignKey(settings.COMPANY_MODEL, verbose_name='公司', on_delete=models.CASCADE)
    summary = models.CharField('职位概要', max_length=200, blank=True)
    job_body = MDTextField('正文')
    education = models.CharField('学历要求', max_length=20, choices=EDUCATION_LIST, default='z')
    job_experience = models.CharField('工作经验', max_length=10, choices=EXPERIENCE_LIST, default='z')
    job_place = models.CharField('工作地点', max_length=20, blank=True)
    full_part_flag = models.CharField('全职/兼职', max_length=10,choices=FULL_PART_FLAG, default='0')
    # pub_time = models.DateTimeField('发布时间', blank=True, null=True)
    pub_status = models.CharField('职位发布状态', max_length=1, choices=PUB_CHOICES, default='p')
    job_status = models.CharField('职位招聘状态', max_length=1, choices=JOB_CHOICES, default='o')
    salary_range = models.CharField('职位薪酬范围', max_length=1, choices=SALARY_RANGE, default='z')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者', on_delete=models.CASCADE)
    job_sortorder = models.IntegerField('排序,数字越大越靠前', blank=False, null=False, default=0)
    category = models.ForeignKey('Category', verbose_name='分类', on_delete=models.CASCADE, blank=False, null=False)
    tags = models.ManyToManyField('Tag', verbose_name='标签集合', blank=True)
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)
    views = models.PositiveIntegerField('浏览量', default=0)

    def save(self, *args, **kwargs):

        if not isinstance(self, Job) and 'slug' in self.__dict__:
            if getattr(self, 'slug') == 'no-slug' or not self.id:
                slug = getattr(self, 'job_name') if 'job_name' in self.__dict__ else getattr(self, 'name')
                setattr(self, 'slug', slugify(slug))
        super().save(*args, **kwargs)
        # is_update_views = 'update_fields' in kwargs and len(kwargs['update_fields']) == 1 and kwargs['update_fields'][
        #     0] == 'views'
        # from DjangoBlog.blog_signals import article_save_signal
        # article_save_signal.send(sender=self.__class__, is_update_views=is_update_views, id=self.id)

    def get_full_url(self):
        site = get_current_site().domain
        url = "https://{site}{path}".format(site=site, path=self.get_absolute_url())
        return url

    def body_to_string(self):
        return self.job_body

    def __str__(self):
        return self.job_name

    class Meta:
        ordering = ['-job_sortorder', '-created_time']
        verbose_name = "职位"
        verbose_name_plural = verbose_name
        get_latest_by = 'job_id'

    def get_absolute_url(self):
        return reverse('job:detailbyid', kwargs={
            'job_id': self.job_id,
            'year': self.created_time.year,
            'month': self.created_time.month,
            'day': self.created_time.day
        })

    @cache_decorator(60 * 60 * 10)
    def get_category_tree(self):
        tree = self.category.get_category_tree()
        names = list(map(lambda c: (c.name, c.get_absolute_url()), tree))

        return names

    def viewed(self):
        self.views += 1
        self.save(update_fields=['views'])

    # def comment_list(self):
    #     cache_key = 'article_comments_{id}'.format(id=self.id)
    #     value = cache.get(cache_key)
    #     if value:
    #         logger.info('get job comments:{id}'.format(id=self.id))
    #         return value
    #     else:
    #         comments = self.comment_set.filter(is_enable=True)
    #         cache.set(cache_key, comments, 60 * 100)
    #         logger.info('set job comments:{id}'.format(id=self.id))
    #         return comments

    def get_admin_url(self):
        info = (self._meta.app_label, self._meta.model_name)
        return reverse('admin:%s_%s_change' % info, args=(self.pk,))

    # @cache_decorator(expiration=60 * 100)
    # def next_article(self):
    #     # 下一篇
    #     return Article.objects.filter(id__gt=self.id, status='p').order_by('id').first()
    #
    # @cache_decorator(expiration=60 * 100)
    # def prev_article(self):
    #     # 前一篇
    #     return Article.objects.filter(id__lt=self.id, status='p').first()


class Category(models.Model):
    """职能分类"""
    name = models.CharField('分类名', max_length=30, unique=True)
    parent_category = models.ForeignKey('self', verbose_name="父级分类", blank=True, null=True, on_delete=models.CASCADE)
    slug = models.SlugField(default='no-slug', max_length=60, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = "分类"
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('job:category_detail', kwargs={'category_name': self.slug})

    def __str__(self):
        return self.name

    @cache_decorator(60 * 60 * 10)
    def get_category_tree(self):
        """
        递归获得分类目录的父级
        :return:
        """
        categorys = []

        def parse(category):
            categorys.append(category)
            if category.parent_category:
                parse(category.parent_category)

        parse(self)
        return categorys

    @cache_decorator(60 * 60 * 10)
    def get_sub_categorys(self):
        """
        获得当前分类目录所有子集
        :return:
        """
        categorys = []
        all_categorys = Category.objects.all()

        def parse(category):
            if category not in categorys:
                categorys.append(category)
            childs = all_categorys.filter(parent_category=category)
            for child in childs:
                if category not in categorys:
                    categorys.append(child)
                parse(child)

        parse(self)
        return categorys


class Tag(models.Model):
    """职位标签"""
    name = models.CharField('标签名', max_length=30, unique=True)
    slug = models.SlugField(default='no-slug', max_length=60, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('job:tag_detail', kwargs={'tag_name': self.slug})

    @cache_decorator(60 * 60 * 10)
    def get_job_count(self):
        return Job.objects.filter(tags__name=self.name).distinct().count()

    class Meta:
        ordering = ['name']
        verbose_name = "标签"
        verbose_name_plural = verbose_name


class JobSettings(models.Model):
    '''站点设置 '''
    sitename = models.CharField("网站名称", max_length=200, null=False, blank=False, default='')
    site_description = models.TextField("网站描述", max_length=1000, null=False, blank=False, default='')
    site_seo_description = models.TextField("网站SEO描述", max_length=1000, null=False, blank=False, default='')
    site_keywords = models.TextField("网站关键字", max_length=1000, null=False, blank=False, default='')
    article_sub_length = models.IntegerField("文章摘要长度", default=300)
    sidebar_article_count = models.IntegerField("侧边栏文章数目", default=10)
    sidebar_comment_count = models.IntegerField("侧边栏评论数目", default=5)
    show_google_adsense = models.BooleanField('是否显示谷歌广告', default=False)
    google_adsense_codes = models.TextField('广告内容', max_length=2000, null=True, blank=True, default='')
    open_site_comment = models.BooleanField('是否打开网站评论功能', default=True)
    beiancode = models.CharField('备案号', max_length=2000, null=True, blank=True, default='')
    analyticscode = models.TextField("网站统计代码", max_length=1000, null=False, blank=False, default='')
    show_gongan_code = models.BooleanField('是否显示公安备案号', default=False, null=False)
    gongan_beiancode = models.TextField('公安备案号', max_length=2000, null=True, blank=True, default='')
    resource_path = models.CharField("静态文件保存地址", max_length=300, null=False, default='/var/www/resource/')

    class Meta:
        verbose_name = '网站配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sitename

    def clean(self):
        if JobSettings.objects.exclude(id=self.id).count():
            raise ValidationError(_('只能有一个配置'))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)