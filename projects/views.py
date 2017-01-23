import markdown
import pypandoc
import re
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.files.temp import NamedTemporaryFile
from rest_framework import viewsets, status, mixins, generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from projects.models import IAA, Project, Buy
from projects.serializers import (
    IAASerializer,
    ProjectSerializer,
    BuySerializer,
)
from projects.filters import (
    BuyFilter,
    ProjectFilter,
)
from projects.forms import (
    IAAForm,
    ProjectForm,
    CreateBuyForm,
    EditBuyForm,
)
from acquisitions import settings
from nda.forms import NDAForm


# Create your views here.

# Utilities
def _public_check(thing, user):
    if not thing.public:
        return user.has_perm('projects.view_project')
    else:
        return True


def _make_response(doc_content, name, doc_type, doc_format):
    response = HttpResponse(doc_content, content_type='text/plain')
    disposition = 'attachment; filename="{0} {1}.{2}"'.format(
        name,
        doc_type,
        doc_format,
    )
    response['Content-Disposition'] = disposition
    return response


def _get_doc(buy, doc_type, access_private=False):
    available_docs = [d for d in buy.available_docs(
        access_private=access_private
    )]
    # Check that the request is for a document that is available
    if doc_type not in available_docs:
        raise Http404
    doc_content = getattr(buy, doc_type)
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
    buy = get_object_or_404(Buy, id=buy)
    if not _public_check(buy, request.user):
        return render(request, "projects/private-page.html")
    if request.method == 'POST':
        doc_type = [i for i in request.POST if re.match("generate_\w+", i)]
        if len(doc_type) > 0:
            doc_type = doc_type[0][9:]
            buy.create_document(doc_type)
            return redirect('buys:document', buy.id, doc_type)
    access_private = request.user.is_staff
    documents = buy.available_docs(access_private=access_private)
    return render(
        request,
        "projects/buy.html",
        {
            "buy": buy,
            "documents": documents
        }
    )


@login_required
def edit_iaa(request):
    if request.method == 'POST':
        form = IAAForm(request.POST)
        if form.is_valid():
            iaa = form.save()
            return redirect('iaas:iaa', iaa.id)
    else:
        form = IAAForm()
    return render(request, 'projects/edit_iaa.html', {
        'form': form
    })


@login_required
def edit_project(request, project=None):
    if request.method == 'POST':
        print('got post')
        form = ProjectForm(request.POST)
        if form.is_valid():
            print('valid!')
            project = form.save()
            return redirect('projects:project', project.id)
    else:
        if project is not None:
            project = Project.objects.get(id=project)
        form = ProjectForm(instance=project)
    return render(request, 'projects/edit_project.html', {
        'form': form,
        'project': project,
    })


@login_required
def create_buy(request):
    if request.method == 'POST':
        form = CreateBuyForm(request.POST)
        if form.is_valid():
            buy = form.save()
            return redirect('buys:buy', buy.id)
    else:
        form = CreateBuyForm()
    return render(request, 'projects/create_buy.html', {
        'form': form
    })


@login_required
def edit_buy(request, buy):
    buy = Buy.objects.get(id=buy)
    if request.method == 'POST':
        form = EditBuyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('buys:buy', buy.id)
    else:
        form = EditBuyForm(instance=buy)
    return render(request, 'projects/edit_buy.html', {
        'buy': buy,
        'form': form
    })


@login_required
def buy_nda(request, buy):
    if buy is None:
        return redirect(reverse('buys:buys'))
    buy = Buy.objects.get(id=buy)
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
    print('documents!')
    buy = get_object_or_404(Buy, id=buy)
    if not _public_check(buy, request.user):
        print('NO')
        raise Http404
    # Get the content of the document
    doc_content = _get_doc(buy, doc_type, request.user.is_staff)
    if doc_content is not None:
        print('yes!')
        return render(
            request,
            "projects/document.html",
            {
                "buy": buy,
                "document": doc_content
            }
        )
    else:
        # TODO: Give option to generate a document if it does not exist
        raise Http404


def download(request, buy, doc_type, doc_format):
    buy = get_object_or_404(Buy, id=buy)
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
            return _make_response(doc_content, buy.name, doc_type, doc_format)
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
            return _make_response(doc_content, buy.name, doc_type, doc_format)
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
            return _make_response(doc_content, buy.name, doc_type, doc_format)
    else:
        raise Http404


@staff_member_required(login_url=settings.LOGIN_URL)
def financials(request):
    docs = IAA.objects.all()
    return render(request, 'projects/financials.html', {'docs': docs})


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


class BuyList(mixins.ListModelMixin, generics.GenericAPIView):
    """
    List all buys. This response includes all buys across the various
    categories of buy that are available in the system.
    """
    serializer_class = BuySerializer
    filter_class = BuyFilter

    def get_queryset(self):
        if self.request.user.has_perm('projects.view_project'):
            return Buy.objects.all()
        else:
            return Buy.objects.select_related('project').filter(
                public=True,
                project__public=True
            )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BuyDetail(mixins.RetrieveModelMixin,
                generics.GenericAPIView):
    """
    Retrieve details of one buy.
    """
    serializer_class = BuySerializer

    def get_queryset(self):
        buy = Buy.objects.get(pk=self.kwargs['pk'])
        if buy.public is True:
            return Buy.objects.filter(pk=self.kwargs['pk'])
        elif self.request.user.has_perm('projects.view_project'):
            return Buy.objects.filter(pk=self.kwargs['pk'])
        else:
            raise Http404

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
