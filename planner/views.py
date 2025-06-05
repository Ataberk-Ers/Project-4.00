from django.shortcuts import render
from courses.models import Course

COURSE_COLORS = [
    "#9cffd2", 
    "#a9cbff", 
    "#ffedb3",  
    "#cd84e6", 
    "#5f86d4",  
    "#7bffff",  
    "#c4f0ce",  
    "#ff97fa",  
    "#ffc061",  
    "#60ffff",  
]

def planner(request):
    courses = Course.objects.filter(isActive=True)
    selected_ids = request.GET.getlist('courses')
    selected_courses = Course.objects.filter(id__in=selected_ids) if selected_ids else []

    course_colors = {}
    for idx, course in enumerate(selected_courses):
        course_colors[course.title] = COURSE_COLORS[idx % len(COURSE_COLORS)]

    timetable = [[[] for _ in range(10)] for _ in range(5)]  
    conflicts = [[False for _ in range(10)] for _ in range(5)]
    for course in selected_courses:
        for day_idx, row in enumerate(course.timetable):
            for hour_idx, val in enumerate(row):
                if val:
                    timetable[day_idx][hour_idx].append(course.title)
                    if len(timetable[day_idx][hour_idx]) > 1:
                        conflicts[day_idx][hour_idx] = True


    has_conflict = any(any(row) for row in conflicts)

    days = [
        (0, "Pazartesi"),
        (1, "Salı"),
        (2, "Çarşamba"),
        (3, "Perşembe"),
        (4, "Cuma"),
    ]
    hours = range(1, 11)
    return render(request, "planner/planner.html", {
        "courses": courses,
        "selected_courses": selected_courses,
        "timetable": timetable,
        "conflicts": conflicts,
        "days": days,
        "hours": hours,
        "selected_ids": [int(i) for i in selected_ids],
        "course_colors": course_colors,
        "has_conflict": has_conflict,
    })