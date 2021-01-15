from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect
from django.db.models import Count, Min, Max
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin

from .forms import UserForm, ProfileForm, BbForm, ResponseForm
from .models import Bb, Rubric, Profile, Response


#from .forms import BbForm, UserForm, ProfileForm, ResponseForm


def index(request):
    bbs = Bb.objects.all()
    rubrics = Rubric.objects.all()
    count_post_by_rubric = Rubric.objects.annotate(Count('bb'))
    min_price_by_rubric = Rubric.objects.annotate(min=Min('bb__price')) #минимальная цена
    max_price_by_rubric = Rubric.objects.annotate(max=Max('bb__price')) #максимальная цена
    return render(request, 'bboard/index.html', {'bbs': bbs, 'rubrics': rubrics, 'cpbr': count_post_by_rubric,
                                                 'minpbr': min_price_by_rubric, 'maxpbr': max_price_by_rubric})

class BbByRubricView(SingleObjectMixin, ListView):
    template_name = 'bboard/by_rubric.html'
    pk_url_kwarg = 'rubric_id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Rubric.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_rubric'] =self.object
        context['rubric'] = Rubric.objects.all()
        context['bbs'] = context['object_list']
        return context

    def get_queryset(self):
        return self.object.bb_set.all()


def post_detail(request, pk):
    post = Bb.objects.get(id=pk)
    comments = Response.objects.filter(post_id=pk)
    context = {'post': post, 'comments': comments}
    return render(request, 'bboard/bb_detail.html', context)


@login_required
def my_posts(request):
    bbs = Bb.objects.filter(user=request.user)
    profile = Profile.objects.get(user=request.user)
    count_post_by_rubric = Rubric.objects.annotate(Count('bb'))
    min_price_by_rubric = Rubric.objects.annotate(min=Min('bb__price'))  # минимальная цена
    context = {'bbs': bbs, 'minpbr': min_price_by_rubric, 'cpbr': count_post_by_rubric, 'profile': profile}
    return render(request, 'bboard/my_posts.html', context)


def profile_view(request, pk):
    profile = Profile.objects.get(user_id=pk)
    my_post = Bb.objects.filter(user_id=pk)
    #comments = Response.objects.filter(user_id=pk)
    context = {'profile': profile, 'my_post': my_post}

    return render(request, 'bboard/profile.html', context)


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


class BbDeleteView(DeleteView):
    model = Bb
    template_name = 'bboard/delete.html'
    success_url = '/bboard'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbEditView(UpdateView):
    model = Bb
    template_name = 'bboard/edit.html'
    form_class = BbForm
    success_url = '/bboard'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('index')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'registration/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


class AddResponse(View):
    """Отклики"""
    def post(self, request, pk):
        form = ResponseForm(request.POST)
        post = Bb.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.post = post
            form.save()
        return redirect('index')
