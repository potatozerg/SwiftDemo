"""demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views


app_name = 'project'
urlpatterns = [
    path('list/<container_name>/', views.container_detail, name="container_detail"),
    path('containers/', views.container_list, name="container"),
    path('add_container/', views.add_container, name="add_container"),
    path('remove_container/', views.remove_container, name="remove_container"),
    path('remove_container_content/', views.remove_container_content, name="remove_container_content"),
    path('upload/<container_name>/', views.add_container_content, name="add_container_content"),
    path('download/<container_name>/<file_name>/', views.get_content_temp_url, name="get_content_temp_url"),
    path('', views.index, name="index"),
    path('logout/', views.logout, name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
