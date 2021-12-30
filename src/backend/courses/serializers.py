from rest_framework import serializers
from .utils.functional import (
    get_course_lectures,
    get_course_students,
    get_course_teachers,
    get_lecture_homeworks,
    get_homework_scores,
    get_score_comments,
)
from .models import Course, Lecture, Student, Teacher, Homework, Score, Comment


class BaseCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"
        depth = 1


class ListCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "name", "description", "owner")
        depth = 1


class RetrieveCourseSerializer(serializers.ModelSerializer):
    lectures = serializers.SerializerMethodField("retrieve_lectures")
    students = serializers.SerializerMethodField("retrieve_students")
    teachers = serializers.SerializerMethodField("retrieve_teachers")

    class Meta:
        model = Course
        fields = ("id", "name", "description", "owner", "lectures", "students", "teachers")
        depth = 1

    @staticmethod
    def retrieve_lectures(course):
        return BaseLectureSerializer(get_course_lectures(course), many=True).data

    @staticmethod
    def retrieve_students(course):
        return BaseStudentSerializer(get_course_students(course), many=True).data

    @staticmethod
    def retrieve_teachers(course):
        return BaseTeacherSerializer(get_course_teachers(course), many=True).data


class BaseLectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = "__all__"


class ListLectureSerializer(BaseLectureSerializer):
    pass


class RetrieveLectureSerializer(BaseLectureSerializer):
    homeworks = serializers.SerializerMethodField("retrieve_homeworks")

    @staticmethod
    def retrieve_homeworks(lecture):
        return ListHomeworkSerializer(get_lecture_homeworks(lecture), many=True).data


class BaseStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ("id", "user")


class ListStudentSerializer(BaseStudentSerializer):
    pass


class RetrieveStudentSerializer(BaseStudentSerializer):
    pass


class BaseTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ("id", "user")


class ListTeacherSerializer(BaseTeacherSerializer):
    pass


class RetrieveTeacherSerializer(BaseTeacherSerializer):
    pass


class BaseHomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = "__all__"
        depth = 1


class ListHomeworkSerializer(BaseHomeworkSerializer):
    class Meta:
        model = Homework
        fields = "__all__"


class RetrieveHomeworkSerializer(BaseHomeworkSerializer):
    scores = serializers.SerializerMethodField("retrieve_scores")

    @staticmethod
    def retrieve_scores(homework):
        return ListScoreSerializer(get_homework_scores(homework), many=True).data


class BaseScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = "__all__"


class ListScoreSerializer(BaseScoreSerializer):
    comments = serializers.SerializerMethodField("retrieve_scores")

    @staticmethod
    def retrieve_scores(score):
        return CommentSerializer(get_score_comments(score), many=True).data


class RetrieveScoreSerializer(BaseScoreSerializer):
    comments = serializers.SerializerMethodField("retrieve_scores")

    @staticmethod
    def retrieve_scores(score):
        return CommentSerializer(get_score_comments(score), many=True).data

    class Meta:
        model = Score
        fields = "__all__"  # ("id", "score", "grader", "homework", "comments")
        depth = 1


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("text",)
