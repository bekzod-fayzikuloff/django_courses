from typing import Union

from django.contrib.auth.models import User
from django.db.models import QuerySet
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request

from .config import BaseService
from ..models import Course, Student


class CourseService(BaseService):
    def get_list(self, request: Request, *args, **kwargs) -> QuerySet:
        query_filter = self._user_filter(request)
        queryset = self.instance.queryset.filter(query_filter)
        return queryset

    def get_retrieve(self, request: Request, *args, **kwargs) -> Course:
        query_filter = self._user_filter(request)
        queryset = get_object_or_404(self.instance.queryset.filter(query_filter), *args, **kwargs)
        return queryset

    def course_action_service(self, **kwargs) -> Union[list, QuerySet]:
        pk = kwargs.get("pk")
        if pk is None:
            return list()
        course = get_object_or_404(self.instance.queryset, pk=pk)
        return self.instance.get_queryset().filter(course=course)

    @staticmethod
    def add_into_course(request: Request, action_mode, **kwargs) -> Course:
        course = Course.objects.get(pk=kwargs.get("pk"))
        user = request.data["user"]
        user = User.objects.get(pk=user)
        member, _ = action_mode.objects.get_or_create(user=user)
        member.course.add(course)
        return course

    @staticmethod
    def remove_into_course(request: Request, action_mode, **kwargs) -> Course:
        course = Course.objects.get(pk=kwargs.get("pk"))
        user = request.data["user"]
        user = User.objects.get(pk=user)
        try:
            student = action_mode.objects.get(user=user)
            student.course.remove(course)
        finally:
            return course

    @staticmethod
    def join_to_course(request: Request, **kwargs) -> Course:
        course = Course.objects.get(pk=kwargs.get("pk"))
        student, _ = Student.objects.get_or_create(user=request.user)
        try:
            student.course.add(course)
        finally:
            return course
