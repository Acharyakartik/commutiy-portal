from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = "news"



urlpatterns = [
    path('', views.news_list, name='news_list'),
    path('add/', views.news_form, name='news_add'),
    path('edit/<int:pk>/', views.news_form, name='news_edit'),
    path('delete/<int:pk>/', views.news_delete, name='news_delete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
