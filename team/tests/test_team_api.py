import pytest
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from team.views import TeammateList
from team.models import Teammate
from team.factories import TeammateFactory
from team.factories import UserFactory
from django.contrib.auth.models import Permission, Group
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
        with pytest.raises(KeyError):
            assert t['slack']


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
        assert t['slack']


@pytest.mark.django_db
def test_no_token_if_new():
    user = UserFactory.create()
    try:
        Token.objects.get(user=user)
    except:
        assert True
        return
    assert False
