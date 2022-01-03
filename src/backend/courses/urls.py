from rest_framework import routers

from .views import CourseViewSet, LectureViewSet, HomeworkViewSet, ScoreViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r"courses", CourseViewSet, basename="courses")
router.register(r"lectures", LectureViewSet, basename="lectures")
router.register(r"homeworks", HomeworkViewSet, basename="homeworks")
router.register(r"scores", ScoreViewSet, basename="scores")
router.register(r"me", UserViewSet, basename="me")

urlpatterns = []

urlpatterns += router.urls
