from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound

from django.urls import reverse_lazy
import os
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import Bb, Rubric
from .forms import BbForm


def index(request):
    bbs = Bb.objects.all()
    rubrics = Rubric.objects.all()
    return render(request, 'bboard/index.html', {'bbs': bbs, 'rubrics': rubrics})


def by_rubric(request, rubric_id):
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
    return render(request, 'bboard/by_rubric.html', context)



@login_required
def my_posts(request):
    bbs = Bb.objects.filter(user=request.user)
    context = {'bbs': bbs}
    return render(request, 'bboard/by_rubric.html', context)


@login_required
def add_post(request):
    if request.method == 'POST':
        form = BbForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect('index')
    else:
        form = BbForm()
    template_name = 'bboard/create.html'
    context = {'form': form}
    return render(request, template_name, context)





def delete(request, pk):
    try:
        person = Bb.objects.get(id=pk)
        person.delete()
        return HttpResponseRedirect('/bboard')
    except Bb.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")





