from django.urls import path
from . import views

app_name = "job"
urlpatterns = [
    path(r'', views.IndexView.as_view(), name='index'),
    path(r'job/<int:year>/<int:month>/<int:day>/<int:job_id>.html',
         views.JobDetailView.as_view(),
         name='detailbyid'),
]
