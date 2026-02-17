from django.urls import path

from . import views


app_name = "member"

urlpatterns = [
    path("login/", views.customer_login, name="customer_login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logout_view, name="logout"),
    path("api/profile/", views.profile_api, name="profile_api"),
    path("api/public/profile/", views.public_profile_api, name="public_profile_api"),

    path("api/members/create/", views.member_create_api, name="member_create_api"),
    path("api/members/pending/", views.pending_member_requests_api, name="pending_member_requests_api"),
    path("api/members/<int:member_no>/approve/", views.approve_member_api, name="approve_member_api"),
    path("api/members/<int:member_no>/reject/", views.reject_member_api, name="reject_member_api"),

    path("api/master/countries/", views.country_list_api, name="country_list_api"),
    path("api/master/states/", views.state_list_api, name="state_list_api"),
    path("api/master/cities/", views.city_list_api, name="city_list_api"),

    path("members/create/", views.member_create_page, name="member_create_page"),
    path("edit/", views.member_edit, name="member_edit"),
    path("member-detail/add/", views.member_detail_add, name="member_detail_add"),
    path("member-detail/<int:member_id>/edit/", views.member_detail_edit, name="member_detail_edit"),
    path("profile/", views.profile, name="profile"),
    path("memberjson/", views.memberjson, name="memberjson"),
]
