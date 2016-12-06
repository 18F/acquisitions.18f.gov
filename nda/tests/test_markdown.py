import pytest
from django.template.loader import render_to_string


def test_markdown():
    rendered = render_to_string('nda/nda.html')
    # The h1 tag has a tab due to markdown rendering for some reason
    expected = "<h1>    Non-Disclosure Agreement for TTS Office of "\
               "Acquisitions</h1>"
    assert expected in rendered
