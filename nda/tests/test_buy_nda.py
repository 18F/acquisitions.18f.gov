import pytest
from django.contrib.auth.models import User, Group
from projects.factories import AgileBPAFactory
from acquisitions.factories import UserFactory


class TestBuyNDA:
    @pytest.fixture
    @pytest.mark.django_db
    def user(self):
        user = UserFactory()
        group = Group.objects.create(name='NDA Signed')
        user.groups.add(group)
        return user

    @pytest.fixture
    @pytest.mark.django_db
    def buy(self):
        buy = AgileBPAFactory()
        return buy

    @pytest.mark.django_db
    def test_signing_nda(self, user, buy):
        buy.technical_evaluation_panel.add(user)
        assert buy.all_nda_signed() is False
        buy.nda_signed.add(user)
        assert buy.all_nda_signed() is True
