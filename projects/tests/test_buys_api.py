import pytest
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from projects.views import AgileBPAList
from projects.models import AgileBPA, Project
from projects.factories import AgileBPAFactory
from projects.factories import UserFactory
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
def test_unauthenticated():
    AgileBPAFactory.create_batch(10, public=True)
    AgileBPAFactory.create_batch(10, public=False)
    view = AgileBPAList.as_view()
    factory = APIRequestFactory()

    request = factory.get('/projects/api/buys')
    response = view(request)

    assert len(response.data) == 10
    for b in response.data:
        assert b['public'] is True


@pytest.mark.django_db
def test_authenticated():
    AgileBPAFactory.create_batch(10, public=True)
    AgileBPAFactory.create_batch(10, public=False)
    # Create a user
    user = UserFactory.create()
    # Get required permission
    content_type = ContentType.objects.get_for_model(Project)
    permission = Permission.objects.get(
        codename='view_project',
        content_type=content_type,
    )
    user.user_permissions.add(permission)
    # Make authenticated request
    view = AgileBPAList.as_view()
    factory = APIRequestFactory()
    request = factory.get('/projects/api/buys')
    force_authenticate(request, user=user)
    response = view(request)

    assert len(response.data) == 20


@pytest.mark.django_db
def test_no_token_if_new():
    user = UserFactory.create()
    try:
        Token.objects.get(user=user)
    except:
        assert True
        return
    assert False
