from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
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

'''class BbCreateView(CreateView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context'''


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

