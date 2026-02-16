from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Admin (Developer only)
    path('admin/', admin.site.urls),

    # Public + Client app URLs
    path('', include('home.urls')),
    path('member/', include('member.urls')),  
    path('news/', include('news.urls')),  
    path('', include('marketplace.urls')),
   

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Admin panel branding
admin.site.site_header = "BBAdmin Admin"
admin.site.site_title = "BBAdmin Admin Portal"
admin.site.index_title = "Welcome to BBAdmin App"
