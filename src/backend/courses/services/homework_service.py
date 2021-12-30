from typing import Union

from django.db.models import QuerySet, Q
from rest_framework.generics import get_object_or_404

from .config import BaseService
from ..models import Homework, Score, Teacher


class HomeworkService(BaseService):
    def get_list(self, request, *args, **kwargs) -> QuerySet:
        query_filter = self.query_filter(request.user)
        queryset = self.instance.queryset.filter(query_filter)
        return queryset

    def get_retrieve(self, request, *args, **kwargs) -> QuerySet:
        queryset = get_object_or_404(Homework, *args, **kwargs)
        return queryset

    @staticmethod
    def query_filter(user) -> Q:
        query_filter = Q(owner__user=user)
        return query_filter

    def course_action_service(self, **kwargs) -> Union[list, QuerySet]:
        pk = kwargs.get("pk")
        if pk is None:
            return list()
        homework = get_object_or_404(self.instance.queryset, pk=pk)
        return self.instance.get_queryset().filter(homework=homework)

    @staticmethod
    def add_score(request, **kwargs):
        pk = kwargs.get("pk")
        homework = Homework.objects.get(pk=pk)
        teacher = Teacher.objects.get(user=request.user)
        score, _ = Score.objects.get_or_create(grader=teacher, homework=homework, score=request.data["score"])
        score.save()
        return score
