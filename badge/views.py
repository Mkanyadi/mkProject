from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Badge


class BadgeListView(ListView):
    model = Badge
    template_name = 'badge/badge_list.html'
    context_object_name = 'badges'


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
