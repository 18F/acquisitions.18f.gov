import pytest
from datetime import date
from django.template import TemplateDoesNotExist
# from projects.models import AgileBPA, Project
from projects.factories import (
    AgileBPAFactory,
    MicropurchaseFactory,
)
from acquisitions.factories import UserFactory


@pytest.mark.django_db
def test_create_agilebpa_document():
    agile_bpa = AgileBPAFactory()
    assert not agile_bpa.qasp
    agile_bpa.create_document('qasp')
    assert agile_bpa.qasp


@pytest.mark.django_db
def test_create_micropurchase_document():
    micropurchase = MicropurchaseFactory()
    with pytest.raises(AttributeError):
        assert not micropurchase.qasp
    with pytest.raises(TemplateDoesNotExist):
        micropurchase.create_document('qasp')
