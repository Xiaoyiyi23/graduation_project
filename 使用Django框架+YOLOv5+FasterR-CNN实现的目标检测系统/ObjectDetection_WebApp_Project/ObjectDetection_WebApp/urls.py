from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path("", views.index, name="index"),
    path('gotoregister/', views.gotoregister, name='register'),
    path('gotologin/', views.gotologin, name='login'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path("objectdetection/", views.object_detection, name="objectdetection"),
    path('upload_success/', views.upload_file, name='upload_file'),
    path('start_detect/', views.start_detect, name='start_detect'),
    path('clear_cache/', views.clear_cache, name='clear_cache'),
    path('download_data/', views.download_data, name='download_data'),
    path('video/', views.video),
    #path('run_object_detection/', views.run_object_detection, name='run_object_detection'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)