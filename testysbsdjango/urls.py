from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from viewer.views import homepage, test
from testysbsdjango.backend_funcs import create_test, continue_test, check_answer

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

    path('', homepage, name='homepage'),
    path('test/', test, name='test'),

    path('check_answer/', check_answer, name='check_answer'),
    path('admin/', admin.site.urls),

    ########## API

    path('create_test/', create_test, name='create_test'),
    path('continue_test/', continue_test, name='continue_test'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)