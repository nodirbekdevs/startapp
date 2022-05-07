from rest_framework.serializers import ModelSerializer, SerializerMethodField, PrimaryKeyRelatedField
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from .models import Teacher, Student, Category, Course


class UserLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data


class UserSerializer(ModelSerializer):
    is_admin = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'is_admin']

    def get_is_admin(self, obj):
        return obj.is_staff


class UserSerializerWithToken(UserSerializer):
    token = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'is_admin', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class TeacherLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = TeacherSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data


class TeacherSerializer(ModelSerializer):
    courses = PrimaryKeyRelatedField(many=True, queryset=Course.objects.all())

    class Meta:
        model = Teacher
        fields = '__all__'


class TeacherSerializerWithToken(TeacherSerializer):
    token = SerializerMethodField(read_only=True)

    class Meta:
        model = Teacher
        fields = '__all__'

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class StudentLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data


class StudentSerializer(ModelSerializer):
    courses = PrimaryKeyRelatedField(many=True, queryset=Course.objects.all())

    class Meta:
        model = Student
        fields = '__all__'


class StudentSerializerWithToken(StudentSerializer):
    token = SerializerMethodField(read_only=True)

    class Meta:
        model = Student
        fields = '__all__'

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CourseSerializer(ModelSerializer):
    coach = TeacherSerializer(read_only=True)
    students = PrimaryKeyRelatedField(many=True, queryset=Student.objects.all())

    class Meta:
        model = Course
        fields = '__all__'