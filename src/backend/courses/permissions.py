from rest_framework.permissions import BasePermission

from .models import Student


class IsCourseTeacher(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj) -> bool:

        return bool(obj.teacher_set.filter(user=request.user))


class IsCourseStudent(BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:

        return bool(obj.student_set.filter(user=request.user))


class IsLectureCourseTeacher(BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:
        return bool(obj.course.teacher_set.filter(user=request.user))


class IsLectureCourseStudent(BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:
        return bool(obj.course.student_set.filter(user=request.user))


class IsHomeWorkOwner(BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:
        try:
            student = Student.objects.get(user=request.user)
            return bool(obj.owner == student)
        except Student.DoesNotExist:
            return False
