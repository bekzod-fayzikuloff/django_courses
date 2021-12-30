from django.conf import settings
from django.db import models


class Student(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ManyToManyField("Course", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.user.username}: {self.course.name}"

    class Meta:
        verbose_name = "student"
        verbose_name_plural = "students"


class Teacher(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ManyToManyField("Course", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.user.username}: {self.course.name}"

    class Meta:
        verbose_name = "teacher"
        verbose_name_plural = "teachers"


class Course(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    owner = models.ForeignKey(Teacher, models.CASCADE, related_name="owner")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = "course"
        verbose_name_plural = "courses"


class Lecture(models.Model):
    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    presentation = models.FileField(upload_to="media/lecture/%Y/%m/%d")
    homework_question = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = "lecture"
        verbose_name_plural = "lectures"


class Homework(models.Model):
    owner = models.ForeignKey(Student, models.CASCADE)
    lecture = models.ForeignKey(Lecture, models.CASCADE)
    file = models.FileField(upload_to="media/homeworks/%Y/%m/%d")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.lecture.name}: -> {self.owner.user}"

    class Meta:
        verbose_name = "homework"
        verbose_name_plural = "homeworks"


class Score(models.Model):
    grader = models.ForeignKey(Teacher, models.CASCADE)
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.homework}: {self.score}"

    class Meta:
        verbose_name = "score"
        verbose_name_plural = "scores"


class Comment(models.Model):
    comment_from = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    score = models.ForeignKey(Score, models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    text = models.TextField()

    def __str__(self):
        return f"{self.comment_from}: {self.score}"

    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"
        order_with_respect_to = "score"
