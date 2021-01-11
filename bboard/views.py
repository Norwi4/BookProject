from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect
from django.db.models import Count, Min, Max
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin

from .models import Bb, Rubric, Profile
from .forms import BbForm, UserForm, ProfileForm


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


class BbDetailView(DetailView):
    model = Bb

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubric'] = Rubric.objects.all()
        return context



@login_required
def my_posts(request):
    bbs = Bb.objects.filter(user=request.user)
    profile = Profile.objects.filter(user=request.user)
    count_post_by_rubric = Rubric.objects.annotate(Count('bb'))
    min_price_by_rubric = Rubric.objects.annotate(min=Min('bb__price'))  # минимальная цена
    context = {'bbs': bbs, 'minpbr': min_price_by_rubric, 'cpbr': count_post_by_rubric, 'profile': profile}
    return render(request, 'bboard/my_posts.html', context)


'''class BbAddView(FormView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    initial = {'price': 0.0}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        self.object = super().get_form(form_class)
        return self.object

    def get_success_url(self):
        return reverse('index')'''
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


'''def delete(request, pk):
    try:
        post = Bb.objects.get(id=pk)
        if post.user == request.user:
            post.delete()
            return HttpResponseRedirect('/bboard')
        else:
            return HttpResponseNotFound("<h2>У вас нет прав на удаление</h2>")
    except Bb.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")'''


class BbDeleteView(DeleteView):
    model = Bb
    template_name = 'bboard/delete.html'
    success_url = '/bboard'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


'''# изменение данных в бд
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
        return HttpResponseNotFound("<h2>Person not found</h2>")'''


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
            return redirect('my_posts')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'registration/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })