import markdown
import pypandoc
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.files.temp import NamedTemporaryFile
from rest_framework import viewsets
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from drf_multiple_model.views import MultipleModelAPIView
from drf_multiple_model.mixins import Query
from projects.models import IAA, Project, AgileBPA, Micropurchase
from projects.serializers import (
    IAASerializer,
    ProjectSerializer,
    AgileBPASerializer,
    MicropurchaseSerializer,
)
from projects.forms import QASPForm, AcquisitionPlanForm, MarketResearchForm
from projects.filters import (
    AgileBPAFilter,
    MicropurchaseFilter,
    ProjectFilter,
)
from nda.forms import NDAForm


# Create your views here.
def iaas(request):
    return render(request, "projects/iaas.html")


def iaa(request, iaa):
    # Since we only want to show a page if the project exists, this can't
    # quite be an API-only thing. But most of the page is built via API.
    iaa = get_object_or_404(IAA, id=iaa)
    if not iaa.is_signed():
        if not request.user.has_perm('projects.view_project'):
            return render(request, "projects/private-page.html")
    return render(request, "projects/iaa.html", {"iaa": iaa})


def projects(request):
    return render(request, "projects/projects.html")


def project(request, project):
    # Since we only want to show a page if the project exists, this can't
    # quite be an API-only thing. But most of the page is built via API.
    project = get_object_or_404(Project, id=project)
    if not project.public:
        if not request.user.has_perm('projects.view_project'):
            return render(request, "projects/private-page.html")
    return render(request, "projects/project.html", {"project": project})


def buys(request):
    return render(request, "projects/buys.html")


def buy(request, buy):
    buy = get_object_or_404(AgileBPA, id=buy)
    if not buy.public:
        if not request.user.has_perm('projects.view_project'):
            return render(request, "projects/private-page.html")
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


@login_required
def buy_nda(request, buy):
    if buy is None:
        return redirect(reverse('buys:buys'))
    buy = AgileBPA.objects.get(id=buy)
    nda_form = NDAForm(request.POST or None)
    if nda_form.is_valid():
        buy.nda_signed.add(request.user)
        return redirect(reverse('buys:buy', args=[buy.id]))
    return render(request, "nda/buy_nda.html", {"buy": buy, "nda_form": nda_form})


def qasp(request, buy):
    buy = get_object_or_404(AgileBPA, id=buy)
    qasp_form = QASPForm(request.POST or None, buy=buy)
    if qasp_form.is_valid():
        buy.create_qasp()
    if not buy.public:
        if request.user.has_perm('projects.view_project'):
            pass
        else:
            raise Http404
    if buy.qasp:
        return render(request, "projects/qasp.html", {"buy": buy, "qasp_form": qasp_form})
    else:
        raise Http404


def market_research(request, buy):
    buy = get_object_or_404(AgileBPA, id=buy)
    market_research_form = MarketResearchForm(request.POST or None, buy=buy)
    if market_research_form.is_valid():
        buy.create_market_research()
    if not buy.public:
        if request.user.has_perm('projects.view_project'):
            pass
        else:
            raise Http404
    if buy.market_research:
        return render(
            request,
            "projects/market_research.html",
            {
                "buy": buy,
                "market_research_form": market_research_form
            }
        )
    else:
        raise Http404


def acquisition_plan(request, buy):
    buy = get_object_or_404(AgileBPA, id=buy)
    acquisition_plan_form = AcquisitionPlanForm(request.POST or None, buy=buy)
    if acquisition_plan_form.is_valid():
        buy.create_acquisition_plan()
    if not buy.public:
        if request.user.has_perm('projects.view_project'):
            pass
        else:
            raise Http404
    if buy.acquisition_plan:
        return render(
            request,
            "projects/acquisition_plan.html",
            {
                "buy": buy,
                "acquisition_plan_form": acquisition_plan_form
            }
        )
    else:
        raise Http404


def download(request, buy, doc_type, doc_format):
    buy = get_object_or_404(AgileBPA, id=buy)
    supported_formats = ['markdown', 'docx', 'pdf']
    available_docs = {
        'qasp': buy.qasp,
        'acquisition_plan': buy.acquisition_plan,
        'market_research': buy.market_research,
    }
    # Check that the request is for a document that is available
    if doc_type not in available_docs.keys():
        raise Http404
    # Return markdown is the format isn't clear
    if doc_format not in supported_formats:
        doc_format = 'markdown'
    # Check that the user has access to view this document
    if not buy.public:
        if request.user.has_perm('projects.view_project'):
            pass
        else:
            raise Http404
    # Get the content of the document
    doc_content = available_docs[doc_type]
    if doc_content is not None:
        # Markdown is the simplest: since the content is already stored that
        # way, it can be sent back directly
        if doc_format == 'markdown':
            response = HttpResponse(doc_content, content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename="{0} {1}.md"'.format(buy.name, doc_type)

            return response
        # For .docx, create a temporary file, use it as the output for pandoc,
        # and then send that file. Using NamedTemporaryFile means that the file
        # will be deleted as soon operations complete.
        elif doc_format == 'docx':
            dl = NamedTemporaryFile()
            output = pypandoc.convert_text(
                doc_content,
                'docx',
                format='markdown_github',
                outputfile=dl.name
            )
            response = HttpResponse(dl, content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename="{0} {1}.docx"'.format(buy.name, doc_type)
            return response
        elif doc_format == 'pdf':
            # This requires LaTeX support (via pdflatex) in addition to a
            # pandoc installation.
            dl = NamedTemporaryFile(suffix='.pdf')
            print(dl.name)
            output = pypandoc.convert_text(
                doc_content,
                'pdf',
                format='markdown_github',
                outputfile=dl.name
            )
            response = HttpResponse(dl, content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename="{0} {1}.pdf"'.format(buy.name, doc_type)
            return response
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
    filter_class = ProjectFilter

    def get_queryset(self):
        if self.request.user.has_perm('projects.view_project'):
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
        elif self.request.user.has_perm('projects.view_project'):
            return Project.objects.filter(pk=self.kwargs['pk'])
        else:
            raise Http404

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class BuyList(MultipleModelAPIView):
    """
    List all buys
    """

    flat = True
    sorting_field = 'id'
    add_model_type = False

    @staticmethod
    def buy_filter(queryset, request, *args, **kwargs):
        if 'id' in request.query_params:
            buy_id = request.query_params['id']
            queryset = queryset.filter(id=buy_id)
        if 'project_id' in request.query_params:
            project_id = request.query_params['project_id']
            queryset = queryset.filter(project__id=project_id)
        if 'name' in request.query_params:
            name = request.query_params['name']
            queryset = queryset.filter(name=name)
        # TODO: allow filtering by procurement_method
        return queryset

    def get_queryList(self):
        if self.request.user.has_perm('projects.view_project'):
            queryList = (
                Query(
                    AgileBPA.objects.all(),
                    AgileBPASerializer,
                    filter_fn=self.buy_filter,
                ),
                Query(
                    Micropurchase.objects.all(),
                    MicropurchaseSerializer,
                    filter_fn=self.buy_filter,
                )
            )
            return queryList
        else:
            queryList = (
                Query(
                    AgileBPA.objects.select_related('project').filter(
                        public=True, project__public=True
                    ),
                    AgileBPASerializer,
                    filter_fn=self.buy_filter,
                ),
                Query(
                    Micropurchase.objects.select_related('project').filter(
                        public=True, project__public=True),
                    MicropurchaseSerializer,
                    filter_fn=self.buy_filter,
                )
            )
            return queryList


class AgileBPAList(mixins.ListModelMixin,
                   generics.GenericAPIView):
    """
    List all Agile BPA buys
    """
    serializer_class = AgileBPASerializer
    filter_class = AgileBPAFilter

    def get_queryset(self):
        if self.request.user.has_perm('projects.view_project'):
            return AgileBPA.objects.all()
        else:
            return AgileBPA.objects.select_related('project').filter(
                public=True,
                project__public=True
            )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class AgileBPADetail(mixins.RetrieveModelMixin,
                     generics.GenericAPIView):
    """
    Retrieve details of one Agile BPA buy
    """
    serializer_class = AgileBPASerializer

    def get_queryset(self):
        buy = AgileBPA.objects.get(pk=self.kwargs['pk'])
        if buy.public is True:
            return AgileBPA.objects.filter(pk=self.kwargs['pk'])
        elif self.request.user.has_perm('projects.view_project'):
            return AgileBPA.objects.filter(pk=self.kwargs['pk'])
        else:
            raise Http404

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class MicropurchaseList(mixins.ListModelMixin,
                        generics.GenericAPIView):
    """
    List all Agile BPA buys
    """
    serializer_class = MicropurchaseSerializer
    filter_class = MicropurchaseFilter

    def get_queryset(self):
        if self.request.user.has_perm('projects.view_project'):
            return Micropurchase.objects.all()
        else:
            return Micropurchase.objects.select_related('project').filter(
                public=True,
                project__public=True
            )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class MicropurchaseDetail(mixins.RetrieveModelMixin,
                          generics.GenericAPIView):
    """
    Retrieve details of one Agile BPA buy
    """
    serializer_class = MicropurchaseSerializer

    def get_queryset(self):
        buy = Micropurchase.objects.get(pk=self.kwargs['pk'])
        if buy.public is True:
            return Micropurchase.objects.filter(pk=self.kwargs['pk'])
        elif self.request.user.has_perm('projects.view_project'):
            return Micropurchase.objects.filter(pk=self.kwargs['pk'])
        else:
            raise Http404

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
