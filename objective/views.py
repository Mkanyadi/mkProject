from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.contrib.auth.models import User
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm
from .models import Objective
from badge.models import Badge


BUCKET_OBJECTIVES = [
    {
        "title": "Santorini (Grecia)",
        "description": "Cină romantică pe o terasă cu vedere la mare."
    },
    {
        "title": "Japonia (Tokyo/Kyoto)",
        "description": "Privește cireșii în floare primăvara."
    },
    {
        "title": "Route 66 (SUA)",
        "description": "Aventură auto clasică de-a lungul Route 66 în SUA."
    },
]


def home(request):
    badges = Badge.objects.all()
    return render(request, 'objectives/home.html', {'badges': badges})



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})



class BucketListView(TemplateView):
    template_name = 'objectives/bucket_list.html'

class AddObjectiveFromBucketView(LoginRequiredMixin, View):
    def post(self, request):
        title = request.POST.get('title')
        description = request.POST.get('description')
        if title and description:
            Objective.objects.create(
                user=request.user,
                title=title,
                description=description,
            )
        return HttpResponseRedirect(reverse('bucket-list'))


# CRUD OBIECTIVE
class ObjectiveListView(LoginRequiredMixin, ListView):
    model = Objective
    template_name = 'objectives/objective_list.html'

    def get_queryset(self):
        queryset = Objective.objects.filter(user=self.request.user)
        if self.request.GET.get("completed") == "true":
            queryset = queryset.filter(completed=True)
        return queryset


class ObjectiveDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Objective
    template_name = 'objectives/objective_detail.html'

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class ObjectiveCreateView(LoginRequiredMixin, CreateView):
    model = Objective
    fields = ['title', 'description', 'image']
    template_name = 'objectives/objective_form.html'
    success_url = reverse_lazy('objective-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ObjectiveUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Objective
    fields = ['title', 'description', 'image']
    template_name = 'objectives/objective_form.html'
    success_url = reverse_lazy('objective-list')

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class ObjectiveDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Objective
    template_name = 'objectives/objective_confirm_delete.html'
    success_url = reverse_lazy('objective-list')

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user



@login_required
def toggle_completed(request, pk):
    objective = get_object_or_404(Objective, pk=pk, user=request.user)
    if request.method == 'POST':
        objective.completed = not objective.completed
        objective.save()
    return redirect('objective-list')
