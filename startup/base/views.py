from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def get_routes(request):
    routes = [
        "ViewSets paketi bilan ishlagim kemadi u bilan qisam juda oddiy bo'p qolardi",

        ' ===== Category ===== ',

        'GET      /api/category/',
        'GET      /api/category/<id>/',
        'POST     /api/category/make/',
        'DELETE   /api/category/delete/<id>/',
        'PUT      /api/category/update/<id>/',

        ' ===== User ===== ',

        'GET       /api/user/',
        'GET       /api/user/<id>/',
        'GET       /api/user/profile/',
        'POST      /api/user/make/',
        'POST      /api/user/login/',
        'PUT       /api/user/profile/update/',
        'PUT       /api/user/update/<id>/',
        'DELETE    /api/user/delete/<id>/',

        ' ===== Student ===== ',

        'GET       /api/student/',
        'GET       /api/student/<id>/',
        'GET       /api/student/profile/',
        'POST      /api/student/make/',
        'POST      /api/student/login/',
        'PUT       /api/student/course_add/<id>/',
        'PUT       /api/student/profile/update/',
        'PUT       /api/student/update/<id>/',
        'PUT       /api/course/course_remove/<id>/',
        'DELETE    /api/student/delete/<id>/',

        ' ===== Course ===== ',

        'GET      /api/course/',
        'GET      /api/course/<id>/',
        'POST     /api/course/make/',
        'PUT      /api/course/confirm/<id>/',
        'PUT      /api/course/update/<id>/',
        'DELETE   /api/course/delete/<id>/',

        ' ===== Teacher ===== ',

        'GET       /api/teacher/',
        'GET       /api/teacher/<id>/',
        'GET       /api/teacher/profile/',
        'POST      /api/teacher/make/',
        'POST      /api/teacher/login/',
        'PUT       /api/teacher/profile/update/',
        'PUT       /api/teacher/update/<id>/',
        'PUT       /api/teacher/confirm/<id>/',
        'DELETE    /api/teacher/delete/<id>/',
    ]

    return Response(routes)