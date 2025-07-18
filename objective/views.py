from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

from .forms import UserRegisterForm
from .models import Objective
from badge.models import Badge





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



class ObjectiveListView(LoginRequiredMixin, ListView):
    model = Objective
    template_name = 'objectives/objective_list.html'

    def get_queryset(self):
        return Objective.objects.filter(user=self.request.user)


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