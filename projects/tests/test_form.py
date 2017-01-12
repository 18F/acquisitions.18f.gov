import pytest
from projects.forms import CreateBuyForm
from projects.factories import ProjectFactory


@pytest.mark.django_db
def test_create_buy_form():
    project = ProjectFactory()
    data = {
        "name": "New Buy",
        "description": "This is a new buy for things",
        "dollars": 50,
        "project": project.id,
        "procurement_method": "agile_bpa"
    }
    form = CreateBuyForm(data)
    assert form.is_valid(), form.errors
