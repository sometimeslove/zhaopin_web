from django.db import models
from django.utils.timezone import now
from django.conf import settings

# Create your models here.
class Company(models.Model):
    SCALE_RANGE = (
        ('a', '少于15人'),
        ('b', '15-50人'),
        ('c', '50-150人'),
        ('d', '150-500人'),
        ('e', '500-2000人'),
        ('f', '2000人以上'),
    )
    FINANCE_RANGE = (
        ('a', '未融资'),
        ('b', '天使轮'),
        ('c', 'A轮'),
        ('d', 'B轮'),
        ('e', 'C轮'),
        ('f', 'D轮及以上'),
        ('g', '上市公司'),
        ('h', '不需要融资'),
    )

    CLASS_RANGE = (
        ('1', '移动互联网'),
        ('2', '电商'),
        ('3', '金融'),
        ('4', '企业服务'),
        ('5', '教育'),
        ('6', '文娱|内容'),
        ('7', '游戏'),
        ('8', '消费生活'),
    )

    STATE_RANGE = (
        ('0', '营业'),
        ('1', '关闭'),
    )

    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField('公司名称', max_length=100, blank=False)
    summary = models.CharField('公司概要', max_length=200, blank=True)
    company_scale = models.CharField('公司规模', max_length=20, choices=SCALE_RANGE, default='a')
    company_finance = models.CharField('融资情况', max_length=20, choices=FINANCE_RANGE, default='a')
    company_class = models.CharField('公司类别', max_length=10, choices=CLASS_RANGE, default='1')
    company_place = models.CharField('公司地点', max_length=20, blank=True)
    company_tags = models.ManyToManyField(settings.TAG_MODEL, verbose_name='公司标签', blank=True)
    setup_time = models.DateTimeField('公司成立时间', blank=True, null=True)
    state = models.CharField('公司状态', max_length=1, choices=STATE_RANGE, default='0')
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)
    views = models.PositiveIntegerField('浏览量', default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-company_id', '-created_time']
        verbose_name = "公司"
        verbose_name_plural = verbose_name
        get_latest_by = 'company_id'

    def __str__(self):
        return self.company_name