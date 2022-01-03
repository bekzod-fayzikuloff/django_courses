"""
    Course app views module
    Declared view handlers, for response on request to server
"""
from django.db.models import QuerySet
from rest_framework import viewsets, status
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response


from .mixins import BaseActionMixin
from .filters import CourseFilter, LectureFilter, HomeworkFilter, ScoreFilter, CommentFilter
from .permissions import IsCourseTeacher, IsLectureCourseTeacher, IsLectureCourseStudent, IsHomeWorkOwner
from .services import (
    CourseService,
    LectureService,
    HomeworkService,
    UserService,
    get_represent_retrieve_data,
    get_represent_action_data,
    get_comments,
    get_represent_list_data,
)

from .models import Course, Lecture, Homework, Score, Teacher, Student, Comment
from .serializers import (
    BaseCourseSerializer,
    ListCourseSerializer,
    RetrieveCourseSerializer,
    BaseLectureSerializer,
    ListLectureSerializer,
    RetrieveLectureSerializer,
    BaseHomeworkSerializer,
    ListHomeworkSerializer,
    RetrieveHomeworkSerializer,
    BaseScoreSerializer,
    RetrieveScoreSerializer,
    ListTeacherSerializer,
    BaseStudentSerializer,
    ListStudentSerializer,
    CommentSerializer,
    CommentCreateSerializer,
    UserSerializer,
)


class CourseViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    BaseActionMixin,
):
    """
    class CourseViewSet, declare need methods for Course Entity
    """

    queryset = Course.objects.all()
    serializer_class = BaseCourseSerializer
    actions = {"list": ListCourseSerializer, "retrieve": RetrieveCourseSerializer}
    permission_classes = [
        permissions.IsAuthenticated(),
    ]
    _filterset_class = CourseFilter
    service = CourseService

    def list(self, request: Request, *args, **kwargs) -> Response:
        """
        list method get <request: Request>, with *args and **kwargs, and realize performance output course list which
        hiding in service layer
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # data = get_represent_list_data(self, request, *args, **kwargs)  # Customize course list result

        return super().list(request, *args, **kwargs)  # Response(data=data)

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        """
        retrieve method get <request: Request>, with *args and **kwargs, and realize performance output course instance
        retrieve which hiding in service layer
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        data = get_represent_retrieve_data(self, request, *args, **kwargs)

        return Response(data=data)

    @action(methods=["GET"], detail=True, name="Course students")
    def course_students(self, request: Request, **kwargs) -> Response:
        """
        course_students method get <request: Request>, with **kwargs, and realize performance output course
        instance students list which hiding in service layer
        :param request:
        :param kwargs:
        :return:
        """
        data = get_represent_action_data(self, **kwargs)
        return Response(data)

    @action(methods=["GET"], detail=True, name="Course teachers")
    def course_teachers(self, request: Request, **kwargs) -> Response:
        """
        course_teachers method get <request: Request>, with **kwargs, and realize performance output course
        instance teachers list which hiding in service layer
        :param request:
        :param kwargs:
        :return:
        """
        data = get_represent_action_data(self, **kwargs)

        return Response(data)

    @action(methods=["GET"], detail=True)
    def lectures(self, request: Request, **kwargs) -> Response:
        """
        lectures method get <request: Request>, with **kwargs, and realize performance output course instance
        lectures list which hiding in service layer
        :param request:
        :param kwargs:
        :return:
        """
        data = get_represent_action_data(self, **kwargs)
        return Response(data)

    @action(methods=["POST"], detail=True, name="Add Teacher")
    def add_teacher(self, request: Request, **kwargs) -> Response:
        """
        add_teacher method get <request: Request>, with **kwargs, and realize performance for adding teacher
        instance into course hiding in service layer
        :param request:
        :param kwargs:
        :return:
        """
        result = self.service(self).add_into_course(request, self.get_create_model(), **kwargs)
        data = self.serializer_class(result).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(methods=["POST"], detail=True, name="Add Student")
    def add_student(self, request, **kwargs) -> Response:
        """
        add_student method get <request: Request>, with **kwargs, and realize performance for adding student
        instance into course hiding in service layer
        :return:
        """
        result = self.service(self).add_into_course(request, self.get_create_model(), **kwargs)
        data = self.serializer_class(result).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(methods=["POST"], detail=True)
    def remove_student(self, request: Request, **kwargs):
        """
        remove_student method get <request: Request>, with **kwargs, and realize performance for remove student
        instance into course hiding in service layer
        :return:
        """
        result = self.service(self).remove_into_course(request, self.get_create_model(), **kwargs)
        data = self.serializer_class(result).data
        return Response(data=data)

    def perform_create(self, serializer) -> None:
        """
        method which call in time create action `start create` instance
        :param serializer:
        :return:
        """
        if self.action == "create":
            self.get_permissions()
            teacher, _ = Teacher.objects.get_or_create(user=self.request.user)
            course = serializer.save(owner=teacher)
            teacher.course.add(course)

    def get_queryset(self) -> QuerySet:
        """
        override get_queryset method for getting soft interface to take need queryset depending on action
        :return:
        """
        actions = {
            "course_students": Student.objects.all(),
            "course_teachers": Teacher.objects.all(),
            "lectures": Lecture.objects.all(),
        }
        return actions.get(self.action, self.queryset)

    def filter_queryset(self, queryset):
        """
        override filter_queryset method for getting soft interface to take need queryset with filtering
        :param queryset:
        :return:
        """
        return self._filterset_class(self.request.GET, self.queryset).qs

    def get_serializer_class(self):
        """
        override get_serializer_class method for getting soft interface to take need serialize class depending on action
        :return:
        """
        actions = {
            "course_students": ListStudentSerializer,
            "course_teachers": ListTeacherSerializer,
            "lectures": RetrieveLectureSerializer,
            "add_teacher": ListTeacherSerializer,
            "add_student": BaseStudentSerializer,
            "remove_student": BaseStudentSerializer,
        }

        return actions.get(self.action, self.serializer_class)

    def get_permissions(self):
        """
        override get_permissions method for getting soft interface to take need permissions depending on action
        :return:
        """
        actions = {
            "update": [IsCourseTeacher()],
            "delete": [IsCourseTeacher()],
            "add_teacher": [
                IsCourseTeacher(),
            ],
            "add_student": [
                IsCourseTeacher(),
            ],
            "remove_student": [
                IsCourseTeacher(),
            ],
        }
        return actions.get(self.action, self.permission_classes)

    def get_create_model(self):
        """
        write custom method for getting need model depending on action
        :return:
        """
        actions = {"add_teacher": Teacher, "add_student": Student, "remove_student": Student}
        return actions.get(self.action)


class LectureViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
    BaseActionMixin,
):
    """
    class realize handling requests for Lecture entity
    """

    serializer_class = BaseLectureSerializer
    permission_classes = [permissions.IsAuthenticated(), IsLectureCourseTeacher(), IsLectureCourseStudent()]
    actions = {"list": ListLectureSerializer, "retrieve": RetrieveLectureSerializer}
    queryset = Lecture.objects.all()
    _filterset_class = LectureFilter
    service = LectureService

    def list(self, request: Request, *args, **kwargs) -> Response:
        """
        list method get <request: Request>, with *args and **kwargs, and realize performance output lecture list which
        hiding in service layer
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # data = get_represent_list_data(self, request, *args, **kwargs)  # Customize lecture list result

        return super().list(request, *args, **kwargs)  # Response(data=data)

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        """
        retrieve method get <request: Request>, with *args and **kwargs, and realize performance output lecture instace
        which hiding in service layer
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        data = get_represent_retrieve_data(self, request, *args, **kwargs)

        return Response(data=data)

    @action(methods=["GET"], detail=True)
    def homeworks(self, request: Request, **kwargs) -> Response:
        """
        homeworks method get <request: Request>, with **kwargs, and realize performance output lecture instace
        homeworks list which hiding in service layer
        :param request:
        :param kwargs:
        :return:
        """
        data = get_represent_action_data(self, **kwargs)

        return Response(data=data)

    @action(methods=["POST"], detail=True)
    def add_homework(self, request: Request, **kwargs) -> Response:
        """
        add_homework method get <request: Request>, with **kwargs, and realize performance for adding add_homework
        instance into lecture
        :param request:
        :param kwargs:
        :return:
        """
        lecture = Lecture.objects.get(**kwargs)
        owner, _ = Student.objects.get_or_create(user=request.user)
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save(lecture=lecture, owner=owner)
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        """
        override get_permissions method for getting soft interface to take need permissions class depending on action
        :return:
        """
        actions = {
            "create": [
                IsLectureCourseTeacher(),
            ],
            "update": [
                IsLectureCourseTeacher(),
            ],
            "add_homework": [
                IsLectureCourseStudent(),
            ],
        }
        return actions.get(self.action, self.permission_classes)

    def get_serializer_class(self):
        """
        override get_serializer_class method for getting soft interface to take need serialize class depending on action
        :return:
        """
        actions = {
            "homeworks": RetrieveHomeworkSerializer,
            "add_homework": BaseHomeworkSerializer,
        }
        return actions.get(self.action, self.serializer_class)

    def get_queryset(self) -> QuerySet:
        """
        override get_queryset method for getting soft interface to take need queryset class depending on action
        :return:
        """
        actions = {"homeworks": Homework.objects.all()}
        return actions.get(self.action, self.queryset)

    def filter_queryset(self, queryset):
        """
        override filter_queryset method for getting soft interface to take need queryset with filtering
        :param queryset:
        :return:
        """
        return self._filterset_class(self.request.GET, self.queryset).qs


class HomeworkViewSet(viewsets.ModelViewSet, BaseActionMixin):
    """
    class realize handling requests for Homework entity
    """

    serializer_class = BaseHomeworkSerializer
    actions = {"list": ListHomeworkSerializer, "retrieve": RetrieveHomeworkSerializer}
    permission_classes = [permissions.IsAuthenticated()]
    _filterset_class = HomeworkFilter
    queryset = Homework.objects.all()
    service = HomeworkService

    def list(self, request: Request, *args, **kwargs) -> Response:
        """
        list method get <request: Request>, with *args and **kwargs, and realize performance output homework list which
        hiding in service layer
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # data = get_represent_list_data(self, request, *args, **kwargs)  # Customize homework list result

        return super().list(request, *args, **kwargs)  # Response(data=data)

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        """
        retrieve method get <request: Request>, with *args and **kwargs, and realize performance output homework
        instance which hiding in service layer
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        data = get_represent_retrieve_data(self, request, *args, **kwargs)

        return Response(data=data)

    @action(methods=["GET"], detail=True)
    def scores(self, request: Request, **kwargs) -> Response:
        """
        scores method get <request: Request>, with **kwargs, and realize perform
        instance score list or add score to homework which hiding in service layer
        :param request:
        :param kwargs:
        :return:
        """
        data = get_represent_action_data(self, **kwargs)

        return Response(data=data)

    @action(methods=["POST"], detail=True)
    def add_score(self, request, **kwargs):
        """
        add_score method get <request: Request>, with  **kwargs, and realize performance add to homework
        instance score to homework which hiding in service layer
        :param request:
        :param kwargs:
        :return:
        """
        result = self.service(self).add_score(request, **kwargs)
        data = self.get_serializer_class()(result).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        """
        override get_permissions method for getting soft interface to take need permissions class depending on action
        :return:
        """
        actions = {
            "retrieve": [
                IsHomeWorkOwner(),
            ]
        }
        return actions.get(self.action, self.permission_classes)

    def get_serializer_class(self):
        """def filter_queryset(self, queryset):
        return self._filterset_class(self.request.GET, self.queryset).qs
        override get_serializer_class method for getting soft interface
        to take need serializer class depending on action
        :return:
        """
        actions = {
            "scores": RetrieveScoreSerializer,
            "add_score": RetrieveScoreSerializer,
        }
        return actions.get(self.action, self.serializer_class)

    def filter_queryset(self, queryset):
        """
        override filter_queryset method for getting soft interface to take need queryset with filtering
        :param queryset:
        :return:
        """
        return self._filterset_class(self.request.GET, self.queryset).qs

    def get_queryset(self) -> QuerySet:
        """
        override get_queryset method for getting soft interface to take need queryset depending on action
        :return:
        """
        actions = {"scores": Score.objects.all()}
        return actions.get(self.action, self.queryset)


class ScoreViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    class realize handling requests for Score entity
    """

    queryset = Score.objects.all()
    serializer_class = BaseScoreSerializer
    _filterset_class = ScoreFilter

    @action(methods=["GET"], detail=True)
    def comments(self, request: Request, **kwargs) -> Response:
        """
        comments method get <request: Request>, with  **kwargs, and realize performance output score
        instance comment list which hiding in service layer
        :param request:
        :param kwargs:
        :return:
        """
        pk = kwargs.get("pk")
        data = get_comments(self, pk=pk).data
        return Response(data=data)

    @action(methods=["POST"], detail=True)
    def add_comment(self, request: Request, **kwargs) -> Response:
        """
        add_comment method get <request: Request>, with  **kwargs, and realize performance create comment
        instance and link with score instance
        :param request:
        :param kwargs:
        :return:
        """
        pk = kwargs.get("pk")
        serialize = self.get_serializer_class()(data=request.data)
        if serialize.is_valid(raise_exception=True):
            text = serialize.validated_data["text"]
            score = self.get_action_model().objects.get(pk=pk)
            comment = Comment.objects.create(text=text, score=score, comment_from=request.user)
            comment.save()
            data = CommentSerializer(comment).data
            return Response(data=data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        """
        override get_serializer_class method for getting soft interface to take need serialize class depending on action
        :return:
        """
        actions = {
            "retrieve": RetrieveScoreSerializer,
            "comments": CommentSerializer,
            "add_comment": CommentCreateSerializer,
        }
        return actions.get(self.action, self.serializer_class)

    def get_queryset(self):
        """
        override get_queryset method for getting soft interface to take need queryset depending on action
        :return:
        """
        actions = {
            "comments": Comment.objects.all(),
        }
        return actions.get(self.action, self.queryset)

    def filter_queryset(self, queryset):
        """
        override filter_queryset method for getting soft interface to take need queryset with filtering
        :param queryset:
        :return:
        """
        return self._filterset_class(self.request.GET, self.queryset).qs

    def get_action_model(self):
        """
        method get_action_model method for getting soft interface to take need model depending on action
        :return:
        """
        actions = {
            "add_comment": Score,
        }
        return actions.get(self.action, self.queryset)


class UserViewSet(viewsets.GenericViewSet):
    """
    class UserViewSet realize user actions and endpoints handling
    """

    serializer_class = UserSerializer
    service = UserService

    def list(self, request: Request) -> Response:
        """
        list method get <request: Request>, and realize performance output current user
        instance data which hiding in service layer
        :param request:
        :return:
        """
        data = self.get_serializer_class()(self.request.user).data
        return Response(data)

    @action(methods=["GET"], detail=False)
    def courses(self, request: Request) -> Response:
        """
        courses method get <request: Request>, and realize performance output current user
        instance all courses list data which hiding in service layer
        :param request:
        :return:
        """
        queryset = self.filter_queryset(self.service(self).get_courses())
        data = self.get_serializer_class()(queryset, many=True).data
        return Response(data=data)

    @action(methods=["GET"], detail=False)
    def course_as_teacher(self, request: Request) -> Response:
        """
        course_as_teacher method get <request: Request>, and realize performance output current user
        instance with courses list data where current user is a teacher, logic hiding in service layer
        :param request:
        :return:
        """
        queryset = self.filter_queryset(self.service(self).get_courses_as_teacher())
        data = self.get_serializer_class()(queryset, many=True).data
        return Response(data=data)

    @action(methods=["GET"], detail=False)
    def course_as_student(self, request: Request) -> Response:
        """
        course_as_student method get <request: Request>, and realize performance output current user
        instance with courses list data where current user is a student, logic hiding in service layer
        :param request:
        :return:
        """
        queryset = self.filter_queryset(self.service(self).get_courses_as_student())
        data = self.get_serializer_class()(queryset, many=True).data
        return Response(data=data)

    @action(methods=["GET"], detail=False)
    def lectures(self, request: Request) -> Response:
        """
        lectures method get <request: Request>, and realize performance output current user
        instance lectures list data which hiding in service layer
        :param request:
        :return:
        """
        queryset = self.filter_queryset(self.service(self).get_lecture())
        data = self.get_serializer_class()(queryset, many=True).data
        return Response(data=data)

    @action(methods=["GET"], detail=False)
    def homeworks(self, request: Request) -> Response:
        """
        homeworks method get <request: Request>, and realize performance output current user
        instance homeworks list data which hiding in service layer
        :param request:
        :return:
        """
        queryset = self.filter_queryset(self.service(self).get_homeworks())
        data = self.get_serializer_class()(queryset, many=True).data
        return Response(data=data)

    @action(methods=["GET"], detail=False)
    def comments(self, request: Request) -> Response:
        """
        comments method get <request: Request>, and realize performance output current user
        instance comments list data which hiding in service layer
        :param request:
        :return:
        """
        queryset = self.filter_queryset(self.service(self).get_comments())
        data = self.get_serializer_class()(queryset, many=True).data
        return Response(data=data)

    @action(methods=["GET"], detail=False)
    def scores(self, request: Request) -> Response:
        """
        scores method get <request: Request>, and realize performance output current user
        instance scores list data which hiding in service layer
        :param request:
        :return:
        """
        queryset = self.filter_queryset(self.service(self).get_scores())
        data = self.get_serializer_class()(queryset, many=True).data
        return Response(data)

    def get_queryset(self):
        """
        override get_queryset method for getting soft interface to take need queryset depending on action
        :return:
        """
        actions = {
            "courses": Course.objects.all(),
            "course_as_teacher": Course.objects.all(),
            "course_as_student": Course.objects.all(),
            "lectures": Lecture.objects.all(),
            "homeworks": Homework.objects.all(),
            "comments": Comment.objects.all(),
            "scores": Score.objects.all(),
        }
        return actions.get(self.action, list())

    def get_serializer_class(self):
        """
        override get_queryset method for getting soft interface to take need serializer class depending on action
        :return:
        """
        actions = {
            "courses": ListCourseSerializer,
            "course_as_teacher": ListCourseSerializer,
            "course_as_student": ListCourseSerializer,
            "lectures": ListLectureSerializer,
            "homeworks": ListHomeworkSerializer,
            "comments": CommentSerializer,
            "scores": BaseScoreSerializer,
        }
        return actions.get(self.action, self.serializer_class)

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        """
        override filter_queryset method for getting soft interface to take need queryset with filtering
        :param queryset:
        :return:
        """
        actions = {
            "courses": CourseFilter,
            "course_as_teacher": CourseFilter,
            "course_as_student": CourseFilter,
            "lectures": LectureFilter,
            "homeworks": HomeworkFilter,
            "comments": CommentFilter,
            "scores": ScoreFilter,
        }
        return actions.get(self.action)(self.request.GET, queryset).qs
