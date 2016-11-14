import os
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from nda.forms import NDAForm


# Create your views here.
@login_required
def sign_nda(request):
    try:
        group = Group.objects.get(name='NDA Signed')
    except Group.DoesNotExist:
        print('NDA Signed group not yet created')
        raise Http404
    try:
        request.user.groups.get(id=group.id)
        return render(request, 'nda/already-signed.html')
    except Group.DoesNotExist:
        pass
    nda_form = NDAForm(request.POST or None)
    if nda_form.is_valid():
        request.user.groups.add(group)
        return render(request, 'nda/success.html')
    return render(request, 'nda/nda.html', {
        'nda_form': nda_form
    })
