from django.contrib.sites.models import Site
from django.core.cache import cache
from hashlib import md5
import logging
import mistune
from mistune import escape, escape_link


logger = logging.getLogger(__name__)


def cache_decorator(expiration=3 * 60):
    def wrapper(func):
        def news(*args, **kwargs):
            try:
                view = args[0]
                key = view.get_cache_key()
            except:
                key = None
                pass
            if not key:
                unique_str = repr((func, args, kwargs))

                m = md5(unique_str.encode('utf-8'))
                key = m.hexdigest()
            value = cache.get(key)
            if value:
                # logger.info('cache_decorator get cache:%s key:%s' % (func.__name__, key))
                if repr(value) == 'default':
                    return None
                else:
                    return value
            else:
                logger.info('cache_decorator set cache:%s key:%s' % (func.__name__, key))
                value = func(*args, **kwargs)
                if not value:
                    cache.set(key, 'default', expiration)
                else:
                    cache.set(key, value, expiration)
                return value

        return news

    return wrapper


@cache_decorator()
def get_current_site():
    site = Site.objects.get_current()
    return site

def get_blog_setting():
    value = cache.get('get_job_setting')
    if value:
        return value
    else:
        from job.models import JobSettings
        if not JobSettings.objects.count():
            setting = JobSettings()
            setting.sitename = 'DjangoBlog'
            setting.site_description = '基于Django的博客系统'
            setting.site_seo_description = '基于Django的博客系统'
            setting.site_keywords = 'Django,Python'
            setting.article_sub_length = 300
            setting.sidebar_article_count = 10
            setting.sidebar_comment_count = 5
            setting.show_google_adsense = False
            setting.open_site_comment = True
            setting.analyticscode = ''
            setting.beiancode = ''
            setting.show_gongan_code = False
            setting.save()
        value = JobSettings.objects.first()
        logger.info('set cache get_blog_setting')
        return value


class BlogMarkDownRenderer(mistune.Renderer):
    '''
    markdown渲染
    '''

    def block_code(self, text, lang=None):
        # renderer has an options
        inlinestyles = self.options.get('inlinestyles')
        linenos = self.options.get('linenos')
        return block_code(text, lang, inlinestyles, linenos)

    def autolink(self, link, is_email=False):
        text = link = escape(link)

        if is_email:
            link = 'mailto:%s' % link
        if not link:
            link = "#"
        site = get_current_site()
        nofollow = "" if link.find(site.domain) > 0 else "rel='nofollow'"
        return '<a href="%s" %s>%s</a>' % (link, nofollow, text)

    def link(self, link, title, text):
        link = escape_link(link)
        site = get_current_site()
        nofollow = "" if link.find(site.domain) > 0 else "rel='nofollow'"
        if not link:
            link = "#"
        if not title:
            return '<a href="%s" %s>%s</a>' % (link, nofollow, text)
        title = escape(title, quote=True)
        return '<a href="%s" title="%s" %s>%s</a>' % (link, title, nofollow, text)

class CommonMarkdown():
    @staticmethod
    def get_markdown(value):
        renderer = BlogMarkDownRenderer(inlinestyles=False)

        mdp = mistune.Markdown(escape=True, renderer=renderer)
        return mdp(value)