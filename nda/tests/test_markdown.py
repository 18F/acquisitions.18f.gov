import pytest
from django.template.loader import render_to_string


def test_markdown():
    rendered = render_to_string('nda/nda.html')
    assert "<h1>Non-Disclosure Agreement</h1>" in rendered
