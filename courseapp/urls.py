from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin', admin.site.urls),
    path('', include('courses.urls')),
    path('planner/', include('planner.urls')),
    path('forum/', include('pages.urls')),
    path('kurslar/', include('courses.urls')),
    path('account/', include('account.urls')),
    
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) 