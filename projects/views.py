import markdown
import pypandoc
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.files.temp import NamedTemporaryFile
from rest_framework import viewsets, status, mixins, generics
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
from projects.filters import (
    AgileBPAFilter,
    MicropurchaseFilter,
    ProjectFilter,
)
from nda.forms import NDAForm


# Create your views here.

# Utilities
def _public_check(thing, user):
    if not thing.public:
        return user.has_perm('projects.view_project')
    else:
        return True


def _make_response(doc_content, name, doc_type):
    response = HttpResponse(doc_content, content_type='text/plain')
    disposition = 'attachment; filename="{0} {1}.{2}"'.format(
        name,
        doc_type,
        fmt
    )
    response['Content-Disposition'] = disposition
    return response


def _get_doc(buy, doc_type):
    available_docs = {
        'qasp': buy.qasp,
        'acquisition_plan': buy.acquisition_plan,
        'market_research': buy.market_research,
    }
    # Check that the request is for a document that is available
    if doc_type not in available_docs.keys():
        raise Http404
    doc_content = available_docs[doc_type]
    return doc_content


# Views
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
    if not _public_check(project, request.user):
        return render(request, "projects/private-page.html")
    return render(request, "projects/project.html", {"project": project})


def buys(request):
    return render(request, "projects/buys.html")


def buy(request, buy):
    buy = get_object_or_404(AgileBPA, id=buy)
    if not _public_check(buy, request.user):
        return render(request, "projects/private-page.html")
    if request.method == 'POST':
        print(request.POST)
        if 'generate_qasp' in request.POST:
            buy.create_document('qasp')
            return redirect('buys:document', buy.id, 'qasp')
        if 'generate_acquisition_plan' in request.POST:
            buy.create_document('acquisition_plan')
            return redirect('buys:document', buy.id, 'acquisition_plan')
        if 'generate_market_research' in request.POST:
            buy.create_document('market_research')
            return redirect('buys:document', buy.id, 'market_research')
    return render(
        request,
        "projects/buy.html",
        {"buy": buy}
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
    return render(
        request,
        "nda/buy_nda.html",
        {"buy": buy, "nda_form": nda_form}
    )


def document(request, buy, doc_type):
    buy = get_object_or_404(AgileBPA, id=buy)
    if not _public_check(buy, request.user):
        raise Http404
    # Get the content of the document
    doc_content = _get_doc(buy, doc_type)
    if doc_content is not None:
        return render(
            request,
            "projects/{0}.html".format(doc_type),
            {"buy": buy}
        )
    else:
        # TODO: Give option to generate a document if it does not exist
        raise Http404


def download(request, buy, doc_type, doc_format):
    buy = get_object_or_404(AgileBPA, id=buy)
    supported_formats = ['markdown', 'md', 'docx', 'pdf']
    # Get the content of the document
    doc_content = _get_doc(buy, doc_type)
    # Return markdown is the format isn't clear
    if doc_format not in supported_formats:
        doc_format = 'md'
    # Standardize format spelling
    if doc_format == 'markdown':
        doc_format = 'md'
    # Check that the user has access to view this document
    if not _public_check(buy, request.user):
        raise Http404
    if doc_content is not None:
        if doc_format == 'md':
            # Markdown is the simplest: since the content is already stored
            # that way, it can be sent back directly
            _make_response(doc_content, buy.name, doc_type)
        elif doc_format == 'docx':
            # For .docx, create a temporary file, use it as the output for
            # pandoc, and then send that file. Using NamedTemporaryFile means
            # that the file will be deleted as soon operations complete.
            dl = NamedTemporaryFile()
            output = pypandoc.convert_text(
                doc_content,
                'docx',
                format='markdown_github',
                outputfile=dl.name
            )
            _make_response(doc_content, buy.name, doc_type)
        elif doc_format == 'pdf':
            # This requires LaTeX support (via pdflatex) in addition to a
            # pandoc installation.
            dl = NamedTemporaryFile(suffix='.pdf')
            output = pypandoc.convert_text(
                doc_content,
                'pdf',
                format='markdown_github',
                outputfile=dl.name
            )
            _make_response(doc_content, buy.name, doc_type)
    else:
        raise Http404


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
    List all projects. Projects may include one or more buys, which
    are nested within the response.
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
    Get details for one project. Projects may include one or more buys, which
    are nested within the response.
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
    List all buys. This response includes all buys across the various
    categories of buy that are available in the system.
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
    List all Agile BPA buys.
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
    Retrieve details of one Agile BPA buy.
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
    List all Micro-purchase buys. Micro-purchases have a maximum value of $3500
    and require significantly less information that the other procurement
    methods.
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
    Retrieve details of one Micro-purchase buy. Micro-purchases have a maximum
    value of $3500 and require significantly less information that the other
    procurement methods.
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
