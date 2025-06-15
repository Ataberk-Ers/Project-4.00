from django.db import models
from django.utils.text import slugify
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(default="", null=False,unique=True,db_index=True, max_length=50)

    def __str__(self):
        return f"{self.name}"

class Course(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to="images",blank=True,default="images/default.jpg")
    date= models.DateField(auto_now=True)
    isActive = models.BooleanField(default=False)
    isHome = models.BooleanField(default=False)
    slug = models.SlugField(default="",blank=True,null=False, unique=True, db_index=True) 
    categories = models.ManyToManyField(Category)
    timetable = models.JSONField(default=list, blank=True)
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses_taught',
        limit_choices_to={'groups__name': 'Instructor'}
    )

    def __str__(self):
        return f"{self.title}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class UploadModel(models.Model):
    image = models.ImageField(upload_to="images", blank=True, default="images/default.jpg")

class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='enrollments')
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='instructed_courses')
    date_enrolled = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

class Exam(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='exams')
    name = models.CharField(max_length=50)
    weight = models.FloatField() 

class Grade(models.Model):
    enrollment = models.ForeignKey('Enrollment', on_delete=models.CASCADE, related_name='grades')
    exam = models.ForeignKey('Exam', on_delete=models.CASCADE, related_name='grades')
    score = models.FloatField()



