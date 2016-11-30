import markdown
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from projects.models import IAA, Project, Buy
from projects.serializers import IAASerializer, ProjectSerializer, BuySerializer
from projects.forms import QASPForm, AcquisitionPlanForm, MarketResearchForm


# Create your views here.
def projects(request):
    return render(request, "projects/projects.html")


def project(request, project):
    # Since we only want to show a page if the project exists, this can't
    # quite be an API-only thing. But most of the page is built via API.
    project = get_object_or_404(Project, id=project)
    if not project.public:
        if not request.user.has_perm('projects.view_private'):
            return render(request,
                          "projects/private-page.html",
                          {"project": project}
                          )
    return render(request, "projects/project.html", {"project": project})


def buys(request):
    return render(request, "projects/buys.html")


def buy(request, buy):
    buy = get_object_or_404(Buy, id=buy)
    if request.method == 'POST':
        if 'generate_qasp' in request.POST:
            qasp_form = QASPForm(request.POST, buy=buy)
            if qasp_form.is_valid():
                buy.create_qasp()
                return redirect('buys:qasp', buy.id)
        if 'generate_acquisition_plan' in request.POST:
            acquisition_plan_form = AcquisitionPlanForm(request.POST, buy=buy)
            if acquisition_plan_form.is_valid():
                buy.create_acquisition_plan()
                return redirect('buys:acquisition_plan', buy.id)
        if 'generate_market_research' in request.POST:
            market_research_form = MarketResearchForm(request.POST, buy=buy)
            if market_research_form.is_valid():
                buy.create_market_research()
                return redirect('buys:market_research', buy.id)
    else:
        qasp_form = QASPForm(buy=buy)
        acquisition_plan_form = AcquisitionPlanForm(buy=buy)
        market_research_form = MarketResearchForm(buy=buy)
    if not buy.public:
        if request.user.has_perm('projects.view_private'):
            pass
        else:
            raise Http404
    return render(
        request,
        "projects/buy.html",
        {
            "buy": buy,
            "qasp_form": qasp_form,
            "acquisition_plan_form": acquisition_plan_form,
            "market_research_form": market_research_form
        }
    )


def qasp(request, buy):
    buy = get_object_or_404(Buy, id=buy)
    qasp_form = QASPForm(request.POST or None, buy=buy)
    if qasp_form.is_valid():
        buy.create_qasp()
    if not buy.public:
        if request.user.has_perm('projects.view_private'):
            pass
        else:
            raise Http404
    if buy.qasp:
        return render(request, "projects/qasp.html", {"buy": buy, "qasp_form": qasp_form})
    else:
        raise Http404


def qasp_download(request, buy, format='markdown'):
    buy = get_object_or_404(Buy, id=buy)
    if not buy.public:
        if request.user.has_perm('projects.view_private'):
            pass
        else:
            raise Http404
    if buy.qasp:
        if format == 'markdown':
            response = HttpResponse(buy.qasp, content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename="{0} QASP.md"'.format(buy.name)

            return response
        elif format == 'docx':
            # TODO: is this possible without leaving python?
            pass
    else:
        raise Http404


def market_research(request, buy):
    buy = get_object_or_404(Buy, id=buy)
    market_research_form = MarketResearchForm(request.POST or None, buy=buy)
    if market_research_form.is_valid():
        buy.create_market_research()
    if not buy.public:
        if request.user.has_perm('projects.view_private'):
            pass
        else:
            raise Http404
    if buy.market_research:
        return render(request, "projects/market_research.html", {"buy": buy, "market_research_form": market_research_form})
    else:
        raise Http404


def market_research_download(request, buy, format='markdown'):
    buy = get_object_or_404(Buy, id=buy)
    if not buy.public:
        if request.user.has_perm('projects.view_private'):
            pass
        else:
            raise Http404
    if buy.market_research:
        if format == 'markdown':
            response = HttpResponse(buy.market_research, content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename="{0} Market Research.md"'.format(buy.name)

            return response
        elif format == 'docx':
            # TODO: is this possible without leaving python?
            pass
    else:
        raise Http404


def acquisition_plan(request, buy):
    buy = get_object_or_404(Buy, id=buy)
    acquisition_plan_form = AcquisitionPlanForm(request.POST or None, buy=buy)
    if acquisition_plan_form.is_valid():
        buy.create_acquisition_plan()
    if not buy.public:
        if request.user.has_perm('projects.view_private'):
            pass
        else:
            raise Http404
    if buy.acquisition_plan:
        return render(request, "projects/acquisition_plan.html", {"buy": buy, "acquisition_plan_form": acquisition_plan_form})
    else:
        raise Http404


def acquisition_plan_download(request, buy, format='markdown'):
    buy = get_object_or_404(Buy, id=buy)
    if not buy.public:
        if request.user.has_perm('projects.view_private'):
            pass
        else:
            raise Http404
    if buy.acquisition_plan:
        if format == 'markdown':
            response = HttpResponse(buy.acquisition_plan, content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename="{0} Acquisition Plan.md"'.format(buy.name)

            return response
        elif format == 'docx':
            # TODO: is this possible without leaving python?
            pass
    else:
        raise Http404


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'projects': reverse('projects:project-list', request=request, format=format),
        'buys': reverse('projects:buy-list', request=request, format=format),
        'iaas': reverse('projects:iaa-list', request=request, format=format)
    })


class IAAList(mixins.ListModelMixin,
              generics.GenericAPIView):
    """
    List all IAAs
    """
    serializer_class = IAASerializer

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return IAA.objects.all()
        else:
            return IAA.objects.exclude(signed_on=None)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class IAADetail(mixins.RetrieveModelMixin,
              generics.GenericAPIView):
    """
    Retrieve details of one IAA
    """
    serializer_class = IAASerializer

    def get_queryset(self):
        iaa = IAA.objects.get(pk=self.kwargs['pk'])
        if iaa.signed_on:
            return IAA.objects.filter(pk=self.kwargs['pk'])
        elif self.request.user.is_authenticated():
            return IAA.objects.filter(pk=self.kwargs['pk'])
        else:
            raise Http404

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ProjectList(mixins.ListModelMixin,
                  generics.GenericAPIView):
    """
    List all projects
    """
    serializer_class = ProjectSerializer

    def get_queryset(self):
        if self.request.user.has_perm('projects.view_private'):
            return Project.objects.all()
        else:
            return Project.objects.filter(public=True)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ProjectDetail(mixins.RetrieveModelMixin,
                    generics.GenericAPIView):
    """
    Retrieve details of one project
    """
    serializer_class = ProjectSerializer

    def get_queryset(self):
        project = Project.objects.get(pk=self.kwargs['pk'])
        if project.public is True:
            return Project.objects.filter(pk=self.kwargs['pk'])
        elif self.request.user.has_perm('projects.view_private'):
            return Project.objects.filter(pk=self.kwargs['pk'])
        else:
            raise Http404

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class BuyList(mixins.ListModelMixin,
              generics.GenericAPIView):
    """
    List all buys
    """
    serializer_class = BuySerializer

    def get_queryset(self):
        if self.request.user.has_perm('projects.view_private'):
            return Buy.objects.all()
        else:
            return Buy.objects.select_related('project').filter(public=True, project__public=True)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BuyDetail(mixins.RetrieveModelMixin,
                generics.GenericAPIView):
    """
    Retrieve details of one buy
    """
    serializer_class = BuySerializer

    def get_queryset(self):
        buy = Buy.objects.get(pk=self.kwargs['pk'])
        if buy.public is True:
            return Buy.objects.filter(pk=self.kwargs['pk'])
        elif self.request.user.has_perm('projects.view_private'):
            return Buy.objects.filter(pk=self.kwargs['pk'])
        else:
            raise Http404

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
