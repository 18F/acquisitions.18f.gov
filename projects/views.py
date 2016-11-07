from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from projects.models import IAA, Project
from projects.serializers import IAASerializer, ProjectSerializer


# Create your views here.
def home(request):
    return render(request, "projects/index.html")


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


# class IAAViewSet(viewsets.ModelViewSet):
#     """
#     API method to view IAAs
#     """
#     serializer_class = IAASerializer
#
#     def get_queryset(self):
#         if self.request.user.is_authenticated():
#             return IAA.objects.all()
#         else:
#             return IAA.objects.exclude(signed_on=null)


@csrf_exempt
def project_list(request):
    if request.method == 'GET':
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return JSONResponse(serializer.data)


# class ProjectList(APIView):
#     """
#     List all projects
#     """
#
#
#     def get_queryset(self):
#         if self.request.user.has_perm('projects.view_private'):
#             return Project.objects.all()
#         else:
#             return Project.objects.filter(public=True)
#
#     def get(self, request, *args, **kwargs):
#         serializer = ProjectSerializer
#         return JSONResponse(serializer.data)
