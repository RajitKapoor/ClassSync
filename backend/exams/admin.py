"""
Admin for exams app.
"""
from django.contrib import admin
from .models import Exam, Question, Option, StudentAnswer, AutoGradingResult


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'teacher', 'start_time', 'end_time', 'is_published', 'max_marks')
    list_filter = ('is_published', 'start_time', 'course')
    search_fields = ('title', 'course__code', 'teacher__email')
    readonly_fields = ('created_at', 'updated_at')


class OptionInline(admin.TabularInline):
    model = Option
    extra = 4


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'exam', 'question_type', 'marks', 'order')
    list_filter = ('question_type', 'exam')
    search_fields = ('question_text', 'exam__title')
    inlines = [OptionInline]
    ordering = ['exam', 'order']


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('option_text', 'question', 'is_correct', 'order')
    list_filter = ('is_correct',)


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'question', 'marks_obtained', 'is_correct', 'submitted_at')
    list_filter = ('is_correct', 'submitted_at', 'exam')
    search_fields = ('student__email', 'exam__title')


@admin.register(AutoGradingResult)
class AutoGradingResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'total_marks_obtained', 'total_marks_possible', 'percentage', 'is_passed', 'graded_at')
    list_filter = ('is_passed', 'graded_at', 'exam')
    search_fields = ('student__email', 'exam__title')

