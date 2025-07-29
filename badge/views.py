from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Badge


class BadgeListView(ListView):
    model = Badge
    template_name = 'badge/badge_list.html'
    context_object_name = 'badges'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            context['default_badges'] = [
                {"name": "Început de călătorie", "description": "Ai finalizat primul tău obiectiv!"},
                {"name": "Momentum", "description": "Ai finalizat 3 obiective în ultima săptămână!"},
                {"name": "Explorer", "description": "Ai finalizat 5 obiective!"},
                {"name": "Aventurier", "description": "Ai finalizat 10 obiective!"},
                {"name": "Sprint final", "description": "Ai finalizat 2 obiective în aceeași zi!"},
                {"name": "100% completat", "description": "Ai finalizat toate obiectivele tale!"},
            ]
        return context


class BadgeDetailView(DetailView):
    model = Badge
    template_name = 'badge/badge_detail.html'


class BadgeCreateView(CreateView):
    model = Badge
    fields = ['name', 'description', 'icon']
    template_name = 'badge/badge_form.html'
    success_url = reverse_lazy('badge-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BadgeUpdateView(UpdateView):
    model = Badge
    fields = ['name', 'description', 'icon']
    template_name = 'badge/badge_form.html'
    success_url = reverse_lazy('badge-list')


class BadgeDeleteView(DeleteView):
    model = Badge
    template_name = 'badge/badge_confirm_delete.html'
    success_url = reverse_lazy('badge-list')

