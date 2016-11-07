from django.shortcuts import render
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from projects.models import IAA, Project
from projects.serializers import IAASerializer, ProjectSerializer


# Create your views here.
def home(request):
    return render(request, "projects/index.html")


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


# @api_view(['GET'])
# def project_list(request, format=None):
#     if request.method == 'GET':
#         projects = Project.objects.all()
#         serializer = ProjectSerializer(projects, many=True)
#         return Response(serializer.data)


@api_view(['GET'])
def project_detail(request, pk, format=None):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProjectSerializer(project)
        return Response(serializer.data)


class ProjectList(APIView):
    """
    List all projects
    """
    def get_queryset(self):
        if self.request.user.has_perm('projects.view_private'):
            return Project.objects.all()
        else:
            return Project.objects.filter(public=True)

    def get(self, request, format=None):
        queryset = self.get_queryset()
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)


class ProjectDetail(APIView):
    """
    Retrieve details of one project
    """
    def get_object(self, pk):
        project = Project.objects.get(pk=pk)
        if project.public:
            return project
        elif self.request.user.has_perm('projects.view_private'):
            return project
        else:
            raise Http404

    def get(self, request, pk, format=None):
        queryset = self.get_object(pk)
        serializer = ProjectSerializer(queryset)
        return Response(serializer.data)
