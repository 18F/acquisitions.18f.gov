import pytest
from django.shortcuts import reverse
from acquisitions.factories import UserFactory
# from projects.views import financials
from projects.factories import IAAFactory


class TestFinancialView:
    @pytest.mark.django_db
    def test_displays_iaas(self, client):
        user = UserFactory(is_staff=True)
        client.force_login(user)
        iaa = IAAFactory.create()
        response = client.get(reverse('financials'))
        assert response.status_code == 200
        assert str.encode(iaa.id) in response.content
