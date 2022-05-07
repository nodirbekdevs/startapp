from django.db import models


class Teacher(models.Model):
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=200, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=200, unique=True, null=True, blank=True)
    password = models.CharField(max_length=200, null=True, blank=True)
    number = models.CharField(max_length=200, unique=True, null=True, blank=True)
    courses = models.ManyToManyField('Course', null=True, blank=True)
    total_courses = models.IntegerField(default=0)
    status = models.CharField(max_length=200, null=True, blank=True)
    is_teacher = models.BooleanField(default=True, null=True, blank=True)
    is_active = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Student(models.Model):
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=200, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=200, unique=True, null=True, blank=True)
    password = models.CharField(max_length=200, null=True, blank=True)
    number = models.CharField(max_length=200, unique=True, null=True, blank=True)
    courses = models.ManyToManyField('Course', null=True, blank=True)
    total_courses = models.IntegerField(default=0)
    is_student = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Category(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    total_courses = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    coach = models.OneToOneField(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    students = models.ManyToManyField(Student, null=True, blank=True)
    total_students = models.IntegerField(default=0)
    views = models.IntegerField(default=0, null=True, blank=True)
    is_active = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


