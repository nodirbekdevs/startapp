from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from ..models import Category
from ..serializers import CategorySerializer
from ..permissions import IsTeacher


@api_view(['GET'])
def get_categories(request):
    try:
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    except:
        message = {'detail': 'Categories does not exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_category(request, pk):
    try:
        category = Category.objects.get(id=pk)
        serializer = CategorySerializer(category, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'Category does not exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsTeacher])
def make_category(request):
    data = request.data
    try:
        category = Category.objects.create(
            name=data['name'],
            description=data['description']
        )
        serializer = CategorySerializer(category, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'Category with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_category(request, pk):
    try:
        data = request.data
        category = Category.objects.get(id=pk)
        category.name = data['name']
        category.description = data['description']
        category.save()
        serializer = CategorySerializer(category, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'Category has not updated'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_teacher(request, pk):
    try:
        category = Category.objects.get(idd=pk)
        if category.total_courses > 1:
            message = {'detail': 'Teacher has not deleted'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            category.delete()
            message = {'detail': 'Teacher has deleted'}
            return Response(message)
    except:
        message = {'detail': 'Teacher has not deleted'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)