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
        post = Bb.objects.get(id=pk)
        if post.user == request.user:
            post.delete()
            return HttpResponseRedirect('/bboard')
        else:
            return HttpResponseNotFound("<h2>У вас нет прав на удаление</h2>")
    except Bb.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


# изменение данных в бд
def edit(request, pk):
    try:
        post = Bb.objects.get(id=pk)

        if request.method == "POST":
            post.title = request.POST.get("title")
            post.content = request.POST.get("content")
            post.rubric.name = request.POST.get("rubric")
            
            post.save()
            return HttpResponseRedirect("/bboard")
        else:
            return render(request, "bboard/edit.html", {"post": post})
    except Bb.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")
