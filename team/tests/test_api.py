import pytest
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
# from projects.views import ProjectList
from team.views import TeammateList
# from projects.models import Project
from team.models import Teammate
# from projects.factories import ProjectFactory
from team.factories import TeammateFactory
# from projects.factories import UserFactory
from team.factories import UserFactory
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
def test_unauthenticated():
    TeammateFactory.create_batch(10)
    view = TeammateList.as_view()
    factory = APIRequestFactory()

    request = factory.get('/team/api/team')
    response = view(request)

    assert len(response.data) == 10
    for t in response.data:
        assert 'slack' not in t


@pytest.mark.django_db
def test_authenticated():
    TeammateFactory.create_batch(10)
    # Create a user
    user = UserFactory.create()
    # Get required permission
    content_type = ContentType.objects.get_for_model(Teammate)
    permission = Permission.objects.get(
        codename='view_private',
        content_type=content_type,
    )
    user.user_permissions.add(permission)
    # Make authenticated request
    view = TeammateList.as_view()
    factory = APIRequestFactory()
    request = factory.get('/team/api/team')
    force_authenticate(request, user=user)
    response = view(request)

    assert len(response.data) == 10
    for t in response.data:
        assert 'slack' in t


@pytest.mark.django_db
def test_no_token_if_new():
    user = UserFactory.create()
    try:
        Token.objects.get(user=user)
    except:
        assert True
        return
    assert False
