from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    preview = models.ImageField(upload_to="course_previews/", blank=True, null=True, verbose_name="Превью")
    description = models.TextField(blank=True, verbose_name="Описание")

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс")
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    preview = models.ImageField(upload_to="lesson_preview/", blank=True, null=True, verbose_name="Превью")
    video_url = models.URLField(blank=True, null=True, verbose_name="Видео")

    def __str__(self):
        return f"{self.course.title} - {self.title}"