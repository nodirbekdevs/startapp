from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from ..models import Teacher, Course
from ..serializers import TeacherSerializer, TeacherSerializerWithToken, TeacherLoginSerializer, CourseSerializer
from ..permissions import IsTeacher


class TeacherLoginView(TokenObtainPairView):
    serializer_class = TeacherLoginSerializer


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_teachers(request):
    try:
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)
    except:
        message = {'detail': 'Teacher does not exists'}
        return Response(message, status=HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_teacher(request, pk):
    try:
        teacher = Teacher.objects.get(id=pk)
        serializer = TeacherSerializer(teacher, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'Teacher does not exists'}
        return Response(message, status=HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsTeacher])
def get_teacher_courses(request):
    try:
        teacher = request.user
        courses = Course.objects.all(coach=teacher)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)
    except:
        message = {'detail': 'Teacher does not exists'}
        return Response(message, status=HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsTeacher])
def get_teacher_profile(request):
    try:
        serializer = TeacherSerializer(request.user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'Teacher does not exists'}
        return Response(message, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def make_teacher(request):
    data = request.data
    try:
        teacher = Teacher.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            username=data['username'],
            number=data['number'],
            password=make_password(data['password'])
        )
        serializer = TeacherSerializerWithToken(teacher, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'Teacher with this email already exists'}
        return Response(message, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def confirm_teacher(request, pk):
    try:
        data = request.data
        teacher = Teacher.objects.get(id=pk)
        if data['status'] == 'Approve':
            teacher.is_active = True
            teacher.status = data['status']
            teacher.save()
            serializer = TeacherSerializer(teacher, many=False)
            return Response(serializer.data)
        elif data['status'] == 'Reject':
            teacher.status = data['status']
            teacher.save()
            message = {'detail': 'Teacher has not confirmed'}
            return Response(message, status=HTTP_400_BAD_REQUEST)
    except:
        message = {'detail': 'Teacher has not confirmed'}
        return Response(message, status=HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsTeacher])
def update_teacher_profile(request):
    try:
        teacher = request.user
        serializer = TeacherSerializerWithToken(teacher, many=False)
        data = request.data
        teacher.first_name = data['first_name']
        teacher.last_name = data['last_name']
        teacher.email = data['email']
        teacher.username = data['username']
        teacher.number = data['number']
        if data['password'] != '':
            teacher.password = make_password(data['password'])
        teacher.save()
        return Response(serializer.data)
    except:
        message = {'detail': 'Teacher has not updated'}
        return Response(message, status=HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_teacher(request, pk):
    try:
        data = request.data
        teacher = Teacher.objects.get(id=pk)
        teacher.first_name = data['first_name']
        teacher.last_name = data['last_name']
        teacher.email = data['email']
        teacher.username = data['username']
        teacher.number = data['number']
        if data['password'] != '':
            teacher.password = make_password(data['password'])
        teacher.save()
        serializer = TeacherSerializer(teacher, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'Teacher has not updated'}
        return Response(message, status=HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_teacher(request, pk):
    try:
        teacher = Teacher.objects.get(idd=pk)
        if len(teacher.courses) and teacher.total_courses > 1:
            message = {'detail': 'Teacher has not deleted'}
            return Response(message, status=HTTP_400_BAD_REQUEST)
        else:
            teacher.delete()
            message = {'detail': 'Teacher has deleted'}
            return Response(message)
    except:
        message = {'detail': 'Teacher has not deleted'}
        return Response(message, status=HTTP_400_BAD_REQUEST)
