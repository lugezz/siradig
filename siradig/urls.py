from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('homepage.urls')),
    path('admin/', admin.site.urls),
    path('login/', include('login.urls')),
    path('users/', include('users.urls')),
]
