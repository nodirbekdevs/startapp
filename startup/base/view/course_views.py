from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from ..models import Course, Teacher, Category
from ..serializers import CourseSerializer, TeacherSerializer, TeacherSerializerWithToken
from ..permissions import IsTeacher


@api_view(['GET'])
def get_courses(request):
    try:
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)
    except:
        message = {'detail': 'Courses do not exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_course(request, pk):
    try:
        course = Course.objects.get(id=pk)
        course.views += 1
        course.save()
        serializer = CourseSerializer(course, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'Course does not exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsTeacher])
def make_course(request):
    data = request.data, teacher = request.user
    try:
        course = Course.objects.create(
            name=data['name'],
            description=data['description'],
            category=data['category'],
            coach=teacher
        )
        if course.category:
            category = Category.objects.get(id=course.category)
            category.total_courses += 1
            category.save()
        teacher.courses.append(course)
        teacher.total_courses += 1
        teacher.save()
        serializer = CourseSerializer(course, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'Course with this name already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def confirm_course(request, pk):
    try:
        data = request.data
        course = Course.objects.get(id=pk)
        if data['is_active']:
            course.is_active = True
            course.save()
            message = {'detail': 'Course activated'}
        else:
            message = {'detail': 'Course was not activated'}

        return Response(message)
    except:
        message = {'detail': 'Course has not updated'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsTeacher])
def update_course(request, pk):
    try:
        data = request.data
        course = Course.objects.get(id=pk)
        course.name = data['name']
        course.description = data['description']
        if course.category != data['category']:
            category = Category.objects.get(id=course.category)
            category.total_courses -= 1
            category.save()
            course.category = data['category']
        if course.coach != data['coach']:
            teacher = Teacher.objects.get(id=course.coach)
            teacher.courses.remove(course)
            teacher.total_courses -= 1
            teacher.save()
            course.coach = data['coach']
        course.save()
        serializer = CourseSerializer(course, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'Course has not updated'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsTeacher])
def delete_course(request, pk):
    try:
        course = Course.objects.get(id=pk)
        if len(course.students) and course.total_students > 1:
            message = {'detail': 'Course has not deleted'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            course.delete()
            message = {'detail': 'Course has deleted'}
            return Response(message)
    except:
        message = {'detail': 'Course has not deleted'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)