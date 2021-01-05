from django.urls import path
from . import views

app_name = "company"
urlpatterns = [
    path(r'company/<int:company_id>/<int:page>.html',
         views.CompanyDetailView.as_view(),
         name='companybyid'),
    path(r'companypage/<int:page>/', views.CompanyListView.as_view(), name='company_page'),
]