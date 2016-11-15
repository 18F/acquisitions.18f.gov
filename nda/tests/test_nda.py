import pytest
from django.contrib.auth.models import Group
from team.factories import UserFactory
from nda.views import sign_nda
from web.views import profile


class TestNDA:
    @pytest.mark.django_db
    def test_add_to_group(self, rf):
        group = Group.objects.create(name='NDA Signed')
        user = UserFactory.create()
        # POST form data using request factory
        request = rf.post('/profile/sign_nda', {'agree': True})
        request.user = user
        response = sign_nda(request)
        # check group
        assert group == user.groups.get(id=group.id)

    @pytest.mark.django_db
    def test_did_not_agree(self, rf):
        group = Group.objects.create(name='NDA Signed')
        user = UserFactory.create()
        # POST form data using request factory
        request = rf.post('/profile/sign_nda', {'agree': False})
        request.user = user
        response = sign_nda(request)
        # check group
        try:
            user.groups.get(id=group.id)
        except:
            assert True
            return
        assert False

    @pytest.mark.django_db
    def test_skip_if_unnecessary(self, rf):
        # create user
        user = UserFactory.create()
        # add to group
        group = Group.objects.create(name='NDA Signed')
        user.groups.add(group)
        # go to view
        request = rf.get('/profile/sign_nda')
        request.user = user
        response = sign_nda(request)
        assert "previously signed the NDA" in str(response.content)
