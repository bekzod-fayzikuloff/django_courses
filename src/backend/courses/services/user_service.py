from django.db.models import QuerySet, Q
from rest_framework.request import Request

from .config import BaseService


class UserService(BaseService):
    def get_list(self, request: Request, *args, **kwargs) -> QuerySet:
        pass

    def get_retrieve(self, request: Request, *args, **kwargs) -> QuerySet:
        pass

    def get_courses(self):
        queryset = self.instance.get_queryset().filter(self._user_filter(self.instance.request))
        return queryset

    def get_courses_as_teacher(self):
        qs_filter = Q(teacher__user=self.instance.request.user)
        queryset = self.instance.get_queryset().filter(qs_filter)
        return queryset

    def get_courses_as_student(self):
        qs_filter = Q(student__user=self.instance.request.user)
        queryset = self.instance.get_queryset().filter(qs_filter)
        return queryset

    def get_comments(self):
        qs_filter = Q(comment_from=self.instance.request.user)
        queryset = self.instance.get_queryset().filter(qs_filter)
        return queryset

    def get_lecture(self):
        qs_filter = Q(course__teacher__user=self.instance.request.user) | Q(
            course__student__user=self.instance.request.user
        )
        queryset = self.instance.get_queryset().filter(qs_filter)
        return queryset

    def get_homeworks(self):
        qs_filter = Q(owner__user=self.instance.request.user)
        queryset = self.instance.get_queryset().filter(qs_filter)
        return queryset

    def get_scores(self):
        qs_filter = Q(homework__owner__user=self.instance.request.user)
        queryset = self.instance.get_queryset().filter(qs_filter)
        return queryset
