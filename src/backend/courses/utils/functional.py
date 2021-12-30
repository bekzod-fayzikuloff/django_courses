from django.db.models import QuerySet

from ..models import Lecture, Student, Teacher, Course, Homework, Score, Comment


def get_course_lectures(course: Course, limit: int = 5) -> QuerySet:
    queryset = Lecture.objects.filter(course=course)
    return queryset[:limit]


def get_course_students(course: Course, limit: int = 5) -> QuerySet:
    queryset = Student.objects.filter(course=course)
    return queryset[:limit]


def get_course_teachers(course: Course, limit: int = 5) -> QuerySet:
    queryset = Teacher.objects.filter(course=course)
    return queryset[:limit]


def get_lecture_homeworks(lecture: Lecture) -> QuerySet:
    queryset = Homework.objects.filter(lecture=lecture)
    return queryset


def get_homework_scores(homework: Homework) -> QuerySet:
    queryset = Score.objects.filter(homework=homework)
    return queryset


def get_score_comments(score: Score):
    queryset = Comment.objects.filter(score=score)
    return queryset
