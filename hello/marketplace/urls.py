from django.urls import path
from . import views


app_name = "marketplace"

urlpatterns = [
    path("member/marketplace/", views.member_marketplace_list, name="member_marketplace_list"),
    path("member/marketplace/add/", views.member_marketplace_form, name="member_marketplace_add"),
    path("member/marketplace/<int:pk>/edit/", views.member_marketplace_form, name="member_marketplace_edit"),
    path("member/marketplace/<int:pk>/delete/", views.member_marketplace_delete, name="member_marketplace_delete"),
    path("api/marketplace/", views.api_all_marketplace, name="api_all_marketplace"),
    path("api/marketplace/listing-types/", views.api_listing_type_list, name="api_listing_type_list"),
]
