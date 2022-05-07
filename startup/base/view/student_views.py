from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from ..models import Student, Course
from ..serializers import StudentSerializer, StudentSerializerWithToken, StudentLoginSerializer
from ..permissions import IsStudent

class StudentLoginView(TokenObtainPairView):
    serializer_class = StudentLoginSerializer


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_students(request):
    try:
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    except:
        message = {'detail': 'Student does not exists'}
        return Response(message, status=HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_student(request, pk):
    try:
        student = Student.objects.get(id=pk)
        serializer = StudentSerializer(student, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'Student does not exists'}
        return Response(message, status=HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsStudent])
def get_student_profile(request):
    try:
        serializer = StudentSerializer(request.user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'Student does not exists'}
        return Response(message, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsStudent])
def add_course(request, pk):
    student = request.user
    try:
        course = Course.objects.get(id=pk)
        serializer = StudentSerializerWithToken(student, many=False)
        course.students.append(student)
        course.total_students += 1
        course.save()
        student.courses.append(course)
        student.total_courses += 1
        student.save()
        return Response(serializer.data)
    except:
        message = {'detail': 'Course does not find'}
        return Response(message, status=HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsStudent])
def remove_course(request, pk):
    student = request.user
    try:
        course = Course.objects.get(id=pk)
        serializer = StudentSerializerWithToken(student, many=False)
        course.students.remove(student)
        course.total_students -= 1
        course.save()
        student.courses.remove(course)
        student.total_courses -= 1
        student.save()
        return Response(serializer.data)
    except:
        message = {'detail': 'Course does not find'}
        return Response(message, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def make_student(request):
    data = request.data
    try:
        student = Student.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            username=data['username'],
            number=data['number'],
            password=make_password(data['password'])
        )
        serializer = StudentSerializerWithToken(student, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'Student with this email already exists'}
        return Response(message, status=HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsStudent])
def update_student_profile(request):
    try:
        student = request.user
        serializer = StudentSerializerWithToken(student, many=False)
        data = request.data
        student.first_name = data['name']
        student.last_name = data['last_name']
        student.email = data['email']
        student.username = data['username']
        student.number = data['number']
        if data['password'] != '':
            student.password = make_password(data['password'])
        student.save()
        return Response(serializer.data)
    except:
        message = {'detail': 'Student has not updated'}
        return Response(message, status=HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_student(request, pk):
    try:
        data = request.data
        student = Student.objects.get(id=pk)
        student.first_name = data['first_name']
        student.last_name = data['last_name']
        student.email = data['email']
        student.username = data['username']
        student.number = data['number']
        if data['password'] != '':
            student.password = make_password(data['password'])
        student.save()
        serializer = StudentSerializer(student, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'Student has not updated'}
        return Response(message, status=HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_student(request, pk):
    try:
        student = Student.objects.get(id=pk)
        if len(student.courses) and student.total_courses > 1:
            message = {'detail': 'Student has not deleted'}
            return Response(message, status=HTTP_400_BAD_REQUEST)
        else:
            student.delete()
            message = {'detail': 'Student has deleted'}
            return Response(message)
    except:
        message = {'detail': 'Student has not deleted'}
        return Response(message, status=HTTP_400_BAD_REQUEST)