from django.urls import path
from . import views

app_name = "company"
urlpatterns = [
    path(r'companypage/<int:page>/', views.CompanyListView.as_view(), name='company_page'),
]