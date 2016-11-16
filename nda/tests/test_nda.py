import pytest
from django.contrib.auth.models import User, Group
from django.test import TestCase, Client
from nda.views import sign_nda
from web.views import profile


class TestNDA:
    @pytest.mark.django_db
    def test_add_to_group(self, rf, django_user_model):
        group = Group.objects.create(name='NDA Signed')
        user = django_user_model.objects.create()
        # POST form data using request factory
        request = rf.post('/profile/sign_nda', {'agree': True})
        request.user = user
        response = sign_nda(request)
        # check group
        assert group == user.groups.get(id=group.id)

    @pytest.mark.django_db
    def test_did_not_agree(self, rf, django_user_model):
        group = Group.objects.create(name='NDA Signed')
        user = django_user_model.objects.create()
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
    def test_skip_if_unnecessary(self, rf, django_user_model):
        # create user
        user = django_user_model.objects.create()
        # add to group
        group = Group.objects.create(name='NDA Signed')
        user.groups.add(group)
        # go to view
        request = rf.get('/profile/sign_nda')
        request.user = user
        response = sign_nda(request)
        assert "previously signed the NDA" in str(response.content)


class TestViews(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name='NDA Signed')
        self.client = Client()
        self.user = User.objects.create_user(
            username='test', email='test@wow.biz', password='top_secret')

    def test_need_nda(self):
        self.client.force_login(self.user)
        response = self.client.get('/profile/sign_nda/')
        self.assertTemplateUsed(response, 'nda/nda.html')
        response = self.client.post('/profile/sign_nda/', {'agree': True})
        self.assertTemplateUsed(response, 'nda/success.html')
        response = self.client.get('/profile/sign_nda/')
        self.assertTemplateUsed(response, 'nda/already-signed.html')
