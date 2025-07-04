from django.urls import path
from . import views


urlpatterns = [
    
    path('', views.index, name="index"),
    path('search', views.search, name="search"),
    path('create-course', views.create_course, name="create_course"),
    path('course-list', views.course_list, name="course_list"),
    path('course-edit/<int:id>', views.course_edit,name="course_edit"),
    path('course-delete/<int:id>', views.course_delete,name="course_delete"),
    path('upload', views.upload, name="upload_image"),
    path('<slug:slug>', views.details, name="course_details"),
    path('kategori/<slug:slug>', views.getCoursesByCategory, name='courses_by_category'),
    path('<slug:slug>/enroll/', views.enroll_in_course, name='enroll_in_course'),
    path('assign-exam-grades/', views.assign_exam_grades, name='assign_exam_grades'),
    path('grade-course/<slug:slug>/', views.grade_course, name='grade_course'),
    path('grades/', views.grades, name='grades'),
    path('grades/<slug:slug>/', views.student_course_grades, name='student_course_grades'),
    
]
