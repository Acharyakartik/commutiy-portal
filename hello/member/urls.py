from django.urls import path
from . import views


app_name = "member"  # important! this is the namespace

urlpatterns = [
    path("login/", views.customer_login, name="customer_login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logout_view, name="logout"),
    path("api/profile/", views.profile_api, name="profile_api"),
    path("edit/", views.member_edit, name="member_edit"),
    path('member-detail/add/', views.member_detail_add, name='member_detail_add'),
    path('member-detail/<int:member_id>/edit/', views.member_detail_edit, name='member_detail_edit'),
    path('profile/', views.profile, name='profile'),
    path('memberjson/', views.memberjson, name='memberjson'),
]
