from django.shortcuts import get_object_or_404, redirect, render
from courses.forms import CourseCreateForm, CourseEditForm, UploadForm
from .models import Course, Category, UploadModel
from django.core.paginator import Paginator
import random
import os
from django.contrib.auth.decorators import login_required, user_passes_test
import json


def index(request):
    kurslar = Course.objects.filter(isActive=1)
    kategoriler = Category.objects.all()

    paginator = Paginator(kurslar, 4)
    page = request.GET.get('page',1)
    page_obj = paginator.page(page)

    return render(request, 'courses/index.html', {
        'categories': kategoriler,
        'page_obj': page_obj,
        'courses': kurslar
    })


def isAdmin(user):
    return user.is_superuser


@user_passes_test(isAdmin)
def create_course(request):
    hours = range(1, 11) 
    days = [
        (0, "Pazartesi"),
        (1, "Salı"),
        (2, "Çarşamba"),
        (3, "Perşembe"),
        (4, "Cuma"),
    ]
    if request.method == "POST":
        post_data = request.POST.copy()

        if 'timetable' in post_data:
            try:
                post_data['timetable'] = json.loads(post_data['timetable'])
            except Exception:
                post_data['timetable'] = []
        form = CourseCreateForm(post_data, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/kurslar/")
    else:
        form = CourseCreateForm()
    return render(request, "courses/create-course.html", {"form": form, "hours": hours, "days": days})


@user_passes_test(isAdmin)
def course_list(request):
    kurslar = Course.objects.all()
    return render(request, 'courses/course-list.html', {
        'courses': kurslar
    })


@user_passes_test(isAdmin)
def course_edit(request, id):
    course = get_object_or_404(Course, pk=id)
    hours = range(1, 11)
    days = [
        (0, "Pazartesi"),
        (1, "Salı"),
        (2, "Çarşamba"),
        (3, "Perşembe"),
        (4, "Cuma"),
    ]
    if request.method == "POST":
        post_data = request.POST.copy()
        if 'timetable' in post_data:
            try:
                post_data['timetable'] = json.loads(post_data['timetable'])
            except Exception:
                post_data['timetable'] = []
        form = CourseEditForm(post_data, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect("course_list")
    else:
        form = CourseEditForm(instance=course)
    return render(request, "courses/edit-course.html", {"form": form, "hours": hours, "days": days})


@user_passes_test(isAdmin)
def course_delete(request, id):
    course = get_object_or_404(Course, pk=id)

    if request.method == "POST":
        course.delete()
        return redirect("course_list")

    return render(request, "courses/course-delete.html", { "course":course })


@user_passes_test(isAdmin)
def upload(request):
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            image = form.cleaned_data.get("image")

            if not image:
                image = "uploads/images/default.jpg"  

            model = UploadModel(image=image)
            model.save()
            return render(request, "courses/success.html")
    else:
        form = UploadForm()
    
    return render(request, "courses/upload.html", {"form": form})


def search(request):
    if "q" in request.GET and request.GET["q"] != "":
        q = request.GET["q"]
        kurslar = Course.objects.filter(isActive=True,title__contains=q).order_by("date")
        kategoriler = Category.objects.all()
    else:
        return redirect("/kurslar/")

    return render(request, 'courses/search.html', {
        'categories': kategoriler,
        'courses': kurslar,
    })


def details(request, slug):
    course = get_object_or_404(Course, slug=slug)
    hours = range(1, 11)
    days = [
        (0, "Pazartesi"),
        (1, "Salı"),
        (2, "Çarşamba"),
        (3, "Perşembe"),
        (4, "Cuma"),
    ]
    context = {
        'course': course,
        'hours': hours,
        'days': days,
    }
    return render(request, 'courses/details.html', context)


def getCoursesByCategory(request, slug):
    kurslar = Course.objects.filter(categories__slug=slug, isActive=True).order_by("date")
    kategoriler = Category.objects.all()

    paginator = Paginator(kurslar, 4)
    page = request.GET.get('page',1)
    page_obj = paginator.page(page)

    return render(request, 'courses/list.html', {
        'categories': kategoriler,
        'page_obj': page_obj,
        'seciliKategori': slug
    })