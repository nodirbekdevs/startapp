from django.contrib import admin
from .models import Teacher, Student, Category, Course


admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Category)
admin.site.register(Course)