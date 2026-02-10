from django.urls import path
from . import views


app_name = "member"  # important! this is the namespace

urlpatterns = [
    path("login/", views.customer_login, name="customer_login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logout_view, name="logout"),
    path('member-detail/add/', views.member_detail_add, name='member_detail_add'),
    path('profile/', views.profile, name='profile'),
    path('memberjson/', views.memberjson, name='memberjson'),
]
