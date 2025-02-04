from django.contrib import admin
from .models import Test, Question, PinCode, LectorPin, Course


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('pin', 'order', 'id', 'done', 'points')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('pin', 'name', 'id', 'start')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('test', 'question_no', 'question_text', 'correct_answer', 'picked_answer')


@admin.register(PinCode)
class PinCodeAdmin(admin.ModelAdmin):
    list_display = ('pin', 'name_surname', 'id', 'hash', 'active', 'course_pin')


@admin.register(LectorPin)
class LectorPinCodeAdmin(admin.ModelAdmin):
    list_display = ('pin', 'id', 'hash')
