from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView



urlpatterns = [
    # Admin (Developer only)
    path('admin/', admin.site.urls),

    # Public + Client app URLs
    path('', include('home.urls')),
    path('member/', include('member.urls')),  
    path('news/', include('news.urls')),  
   

]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin panel branding
admin.site.site_header = "BBAdmin Admin"
admin.site.site_title = "BBAdmin Admin Portal"
admin.site.index_title = "Welcome to BBAdmin App"
