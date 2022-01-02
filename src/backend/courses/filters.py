from django_filters import rest_framework as filters
from .models import Course, Lecture, Homework, Score


class CourseFilter(filters.FilterSet):
    class Meta:
        model = Course
        fields = {
            "name": ['exact', 'contains'],
            "description": ['exact', 'contains'],
            "owner__user__username": ['exact', 'contains'],
        }


class LectureFilter(filters.FilterSet):
    class Meta:
        model = Lecture
        fields = {
            "name": ['exact', 'icontains'],
            "course__name": ['exact', 'contains'],
            "course__owner__user__username": ['exact', 'contains']
        }


class HomeworkFilter(filters.FilterSet):
    class Meta:
        model = Homework
        fields = {
            "owner__user__username": ['exact', 'contains'],
            "lecture__name": ['exact', 'contains'],
            "lecture__course__owner__user__username": ['exact', 'contains']
        }


class ScoreFilter(filters.FilterSet):
    class Meta:
        model = Score
        fields = {
            "grader__user__username": ['exact', 'contains'],
            "score": ['exact', 'contains'],
            "homework__lecture__name": ['exact', 'contains']
        }
