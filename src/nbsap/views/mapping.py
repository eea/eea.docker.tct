from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from nbsap import models


@login_required
def mapping_national_objectives(request):
    pass

