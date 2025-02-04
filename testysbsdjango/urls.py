from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from viewer.views import homepage, test
from testysbsdjango.backend.login_session import check_correct
from testysbsdjango.backend.CRUD import create_test, continue_test

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

    path('', homepage, name='homepage'),
    path('test/', test, name='test'),
    # path('my_tests/<hash>/', my_tests, name='my_tests'),
    # path('test_history/<hash>/<int:test_number>/', test_history, name='test_history'),
    # path('lector_view/<str:lector_hash>/', lector_view, name='lector_view'),
    # path('course_view/<str:course_hash>/', course_view, name='course_view'),
    # path('course_view/<str:course_hash>/<lector_hash>/', course_view, name='course_view'),
    # path('test_overview_course/<course_hash>/<pin_hash>/<int:test_num>/', test_overview_course, name='test_overview_course'),

    path('check_correct/', check_correct, name='check_correct'),
    # path('correct_or_incorrect/', correct_or_incorrect, name='correct_or_incorrect'),
    # path('delete_session/', delete_session, name='delete_session'),
    # path('api/get-last-change/', GetLastChangeView.as_view(), name='get_last_change'),
    # path('api/get-questions-s/', GetQuestionsSView.as_view(), name='get_questions_s'),
    # path('api/get-questions-p/', GetQuestionsPView.as_view(), name='get_questions_p'),
    # path('api/get_saved_questions/', get_saved_questions, name='get_saved_questions'),
    path('admin/', admin.site.urls),
    # path('login_with_pin/', login_with_pin, name='login_with_pin'),
    # path('finish_test/', finish_test, name='finish_test'),
    # path('send_email/', send_email, name='send_email'),
    # path('login_lector/', login_lector, name='login_lector'),
    # path('open_pdf/', open_pdf, name='open_pdf'),

    ########## CRUD

    path('create_test/', create_test, name='create_test'),
    path('continue_test/', continue_test, name='continue_test'),
    # path('create_students/', create_students, name='create_students'),
    # path('create_course/', create_course, name='create_course'),
    # path('change_name_surname_pin/', change_name_surname_pin, name='change_name_surname_pin'),
    # path('change_name_start_course/', change_name_start_course, name='change_name_start_course'),
    # path('delete_pin/', delete_pin, name='delete_pin'),
    # path('delete_course/', delete_course, name='delete_course'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)