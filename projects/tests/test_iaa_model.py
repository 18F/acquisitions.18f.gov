import pytest
from datetime import date, timedelta
from projects.factories import (
    IAAFactory,
)


@pytest.mark.django_db
def test_active():
    iaa = IAAFactory()
    iaa.performance_begins = date.today() - timedelta(days=1)
    iaa.performance_ends = date.today() + timedelta(days=1)
    assert iaa.active()


@pytest.mark.django_db
def test_inactive():
    iaa = IAAFactory()
    iaa.performance_begins = date.today() - timedelta(days=10)
    iaa.performance_ends = date.today() - timedelta(days=5)
    assert not iaa.active()
