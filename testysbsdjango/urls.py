from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from viewer.views import homepage, test
from testysbsdjango.backend.check_answer import check_correct
from testysbsdjango.backend.CRUD import create_test, continue_test

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

    path('', homepage, name='homepage'),
    path('test/', test, name='test'),

    path('check_correct/', check_correct, name='check_correct'),
    path('admin/', admin.site.urls),

    ########## CRUD

    path('create_test/', create_test, name='create_test'),
    path('continue_test/', continue_test, name='continue_test'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)