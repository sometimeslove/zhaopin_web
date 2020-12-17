from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "job"
urlpatterns = [
    path(r'', views.IndexView.as_view(), name='index'),
    path(r'job/<int:year>/<int:month>/<int:day>/<int:job_id>.html',
         views.JobDetailView.as_view(),
         name='detailbyid'),
]
if settings.DEBUG:
    # urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)