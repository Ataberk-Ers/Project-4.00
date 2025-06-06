from django.db import models
from django.utils.text import slugify

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

    def __str__(self):
        return f"{self.title}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class UploadModel(models.Model):
    image = models.ImageField(upload_to="images", blank=True, default="images/default.jpg")


