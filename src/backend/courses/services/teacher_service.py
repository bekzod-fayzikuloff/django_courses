from typing import Union

from django.contrib.auth.models import User
from django.db.models import QuerySet, Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from .config import BaseService
from courses.models import Course


class UserAsTeacherService(BaseService):
    def get_list(self, request: Request, *args, **kwargs) -> QuerySet:
        pass

    def get_retrieve(self, request: Request, *args, **kwargs) -> Union[list, QuerySet]:
        pk = kwargs.get("pk")
        try:
            query_filter = self._teacher_filter(request=request)
            return self.instance.get_queryset().filter(query_filter).get(pk=pk)
        except Course.DoesNotExist:
            raise Http404

    def get_action_list(self, filter_mask):
        return self.instance.get_queryset().filter(filter_mask)

    def get_course_actions(self, request: Request, pk: int, filter_mask) -> QuerySet:
        try:
            query_filter = self._teacher_filter(request=request)
            course = Course.objects.filter(query_filter).get(pk=pk)
            filter_mask = filter_mask(course)
            queryset = self.instance.get_queryset().filter(filter_mask)
            return queryset
        except Course.DoesNotExist:
            raise Http404

    def add_into_course(self, pk: int) -> Course:
        course = Course.objects.get(pk=pk)
        user = self.instance.request.data["user"]
        user = User.objects.get(pk=user)
        member, _ = self.instance.get_action_mode().objects.get_or_create(user=user)
        member.course.add(course)
        return course

    def remove_into_course(self, pk: int) -> Course:
        course = Course.objects.get(pk=pk)
        user = self.instance.request.data["user"]
        user = User.objects.get(pk=user)
        try:
            student = self.instance.get_action_mode().objects.get(user=user)
            student.course.remove(course)
        finally:
            return course

    def create_lecture(self, pk: int) -> Response:
        course = Course.objects.get(pk=pk)
        serializer = self.instance.get_serializer_class()(data=self.instance.request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(course=course)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_instance(self, queryset: QuerySet, pk: int) -> Response:
        instance = get_object_or_404(queryset, pk=pk)
        return Response(self.instance.get_serializer_class()(instance).data)

    def action_list_filter(self):
        actions = {
            "lectures": Q(course__teacher__user=self.instance.request.user),
            "homeworks": Q(lecture__course__teacher__user=self.instance.request.user),
            "comments": Q(comment_from=self.instance.request.user),
            "scores": Q(grader__user=self.instance.request.user),
        }
        return actions.get(self.instance.action)

    @staticmethod
    def get_course_filter(course) -> Q:
        return Q(course=course)

    @staticmethod
    def get_course_homework_filter(course) -> Q:
        return Q(lecture__course=course)

    @staticmethod
    def get_course_score_filter(course) -> Q:
        return Q(homework__lecture__course=course)

    @staticmethod
    def get_course_comment_filter(course) -> Q:
        return Q(score__homework__lecture__course=course)
