from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.urls import reverse
from yihang_website.utils import get_current_site
from django.utils.timezone import now
from django.core.mail import send_mail
from django.conf import settings

# Create your models here.
class JobUser(AbstractUser):
    nickname = models.CharField('昵称', max_length=100, blank=True)
    mugshot = models.ImageField('头像', upload_to='upload/mugshots', blank=True)
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)
    home_address = models.CharField('家庭住址',max_length=200,blank=True)

    # objects = BlogUserManager()

    def get_absolute_url(self):
        return reverse('job:author_detail', kwargs={'author_name': self.username})

    def __str__(self):
        return self.email

    def get_full_url(self):
        site = get_current_site().domain
        url = "https://{site}{path}".format(site=site, path=self.get_absolute_url())
        return url

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        from_email = settings.DEFAULT_FROM_EMAIL
        super(JobUser, self).email_user(subject, message, from_email, **kwargs)
        # send_mail(subject, message, from_email, [self.email], **kwargs)