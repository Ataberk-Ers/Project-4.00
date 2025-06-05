from django import forms
from django.forms import SelectMultiple, TextInput, Textarea, HiddenInput
from courses.models import Course
import json

class JSONListField(forms.CharField):
    def to_python(self, value):
        if not value:
            return []
        if isinstance(value, list):
            return value
        try:
            return json.loads(value)
        except Exception:
            return []



class CourseCreateForm(forms.ModelForm):
    timetable = JSONListField(widget=HiddenInput(), required=False)

    class Meta:
        model = Course
        fields = ('title','description','image','slug','timetable')  
        labels = {
            'title':"kurs başlığı",
            'description':'açıklama'
        }
        widgets = {
            "title": TextInput(attrs={"class":"form-control"}),
            "description": Textarea(attrs={"class":"form-control"}),
            "slug": TextInput(attrs={"class":"form-control"}),
        }
        error_messages = {
            "title": {
                "required":"kurs başlığı girmelisiniz.",
                "max_length": "maksimum 50 karakter girmelisiniz"
            },
            "description": {
                "required":"kurs açıklaması gereklidir."
            }
        }

class CourseEditForm(forms.ModelForm):
    timetable = JSONListField(widget=HiddenInput(), required=False)

    class Meta:
        model = Course
        fields = ('title','description','image','slug','categories','isActive','timetable') 
        labels = {
            'title':"kurs başlığı",
            'description':'açıklama'
        }
        widgets = {
            "title": TextInput(attrs={"class":"form-control"}),
            "description": Textarea(attrs={"class":"form-control"}),
            "slug": TextInput(attrs={"class":"form-control"}),
            "categories": SelectMultiple(attrs={"class":"form-control"})
        }
        error_messages = {
            "title": {
                "required":"kurs başlığı girmelisiniz.",
                "max_length": "maksimum 50 karakter girmelisiniz"
            },
            "description": {
                "required":"kurs açıklaması gereklidir."
            }
        }

class UploadForm(forms.Form):
    image = forms.ImageField(required=False)
