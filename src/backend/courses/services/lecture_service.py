from typing import Union

from django.db.models import QuerySet
from rest_framework.generics import get_object_or_404

from .config import BaseService
from ..models import Lecture


class LectureService(BaseService):
    def get_list(self, request, *args, **kwargs) -> QuerySet:
        queryset = self.instance.queryset
        return queryset

    def get_retrieve(self, request, *args, **kwargs) -> Lecture:
        queryset = get_object_or_404(Lecture, *args, **kwargs)
        return queryset

    def course_action_service(self, **kwargs) -> Union[list, QuerySet]:
        pk = kwargs.get("pk")
        if pk is None:
            return list()
        lecture = get_object_or_404(self.instance.queryset, pk=pk)
        return self.instance.get_queryset().filter(lecture=lecture)
