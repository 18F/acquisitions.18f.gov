import pytest
from projects.forms import CreateBuyForm, EditBuyForm
from projects.factories import ProjectFactory, BuyFactory


@pytest.mark.django_db
def test_create_buy_form():
    project = ProjectFactory.create()
    data = {
        "name": "New Buy",
        "description": "This is a new buy for things",
        "dollars": 50,
        "project": project.id,
        "procurement_method": "agile_bpa"
    }
    form = CreateBuyForm(data)
    assert form.is_valid(), form.errors


@pytest.mark.django_db
def test_edit_buy_form():
    buy = BuyFactory.create()
    data = {
        "name": buy.name,
        "description": buy.description,
        "dollars": buy.dollars,
        "project": buy.project.id,
        "procurement_method": buy.procurement_method,
        "qasp": "something new"
    }
    form = EditBuyForm(instance=buy)
    print(buy.project.dollars, buy.project.budget_remaining(), buy.dollars)
    # assert form.is_valid(), form.errors
    # assert buy.qasp == "something new"
