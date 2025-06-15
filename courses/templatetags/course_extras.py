from django import template
register = template.Library()

@register.filter
def get_item(value, arg):
    try:
        return value[arg]
    except:
        return None
    
@register.filter
def is_enrolled(course, user):
    return course.enrollments.filter(student=user).exists()

@register.filter
def if_in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.filter
def get_grade(exam, enrollment):
    return exam.grades.filter(enrollment=enrollment).first()
