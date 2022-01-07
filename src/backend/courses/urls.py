from django.urls import path
from rest_framework import routers

from .views import CourseViewSet, LectureViewSet, HomeworkViewSet, ScoreViewSet, UserViewSet, UserAsTeacherViewSet

router = routers.DefaultRouter()
router.register(r"courses", CourseViewSet, basename="courses")
router.register(r"lectures", LectureViewSet, basename="lectures")
router.register(r"homeworks", HomeworkViewSet, basename="homeworks")
router.register(r"scores", ScoreViewSet, basename="scores")
router.register(r"me", UserViewSet, basename="me")
router.register(r"me-as-teacher", UserAsTeacherViewSet, basename="me_as_teacher")

urlpatterns = [
    path(
        'me-as-teacher/<int:pk>/course_lecture/<int:lecture_pk>/',
        UserAsTeacherViewSet.as_view({"get": "course_lecture"}),
        name="lecture-course-detail"
    ),
    path(
        'me-as-teacher/<int:pk>/course_homeworks/<int:homework_pk>/',
        UserAsTeacherViewSet.as_view({"get": "course_homeworks"}),
        name="lecture-course-detail"
    ),
    path(
        'me-as-teacher/<int:pk>/course_scores/<int:homework_pk>/',
        UserAsTeacherViewSet.as_view({"post": "add_score"}),
        name="lecture-course-detail"
    ),
]

urlpatterns += router.urls
