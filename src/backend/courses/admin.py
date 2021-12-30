from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Lecture, Course, Teacher, Student, Comment, Score, Homework

admin.site.site_header = "Course Dashboard"
admin.site.unregister(Group)


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ("name", "course")
    list_display_links = ("name", "course")
    list_filter = ("created_at",)
    search_fields = ("name", "course__name", "course__owner__user__username")
    empty_value_display = "<--->"


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_select_related = ("owner",)
    list_display = ("name", "owner")
    list_filter = ("created_at",)
    search_fields = ("name", "owner__user__username")
    empty_value_display = "<--->"
    fieldsets = (
        (None, {"fields": ("name", "description", "owner")}),
        (
            "Flag options",
            {
                "classes": ("wide",),
                "fields": ("is_active",),
            },
        ),
    )


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_select_related = ("user",)
    list_display = ("user",)
    list_filter = ("user__username",)
    search_fields = ("user__username",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_select_related = ("user",)
    list_display = ("user",)
    list_filter = ("user__username",)
    search_fields = ("user__username",)
    empty_value_display = "<--->"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_select_related = ("comment_from", "score")
    list_display = ("comment_from", "score")
    list_filter = ("created_at",)
    search_fields = ("comment_from__username", "score__grader__user__username")
    empty_value_display = "<--->"


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ("homework", "score")
    list_filter = ("created_at",)
    empty_value_display = "<--->"


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ("lecture",)
    list_filter = ("created_at",)
    empty_value_display = "<--->"
