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
from django.contrib import messages

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

@login_required
def home(request):
    badges = request.user.badges.all()
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

class ObjectiveListView(LoginRequiredMixin, ListView):
    model = Objective
    template_name = 'objectives/objective_list.html'

    def get_queryset(self):
        queryset = Objective.objects.filter(user=self.request.user)
        if self.request.GET.get("completed") == "true":
            queryset = queryset.filter(completed=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['badges'] = self.request.user.badges.all()
        return context

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

        badgeuri_initiale = set(request.user.badges.values_list('name', flat=True))
        verifica_si_acorda_badgeuri(request.user)
        badgeuri_noi = set(request.user.badges.values_list('name', flat=True)) - badgeuri_initiale

        for badge in badgeuri_noi:
            messages.success(request, f'🎉 Felicitări! Ai primit un nou badge: {badge}')

    return redirect('objective-list')

def verifica_si_acorda_badgeuri(user):
    print(f"🟢 Verific badge-uri pentru: {user.username}")

    total = Objective.objects.filter(user=user).count()
    finalizate = Objective.objects.filter(user=user, completed=True).count()
    print(f"🥇 Obiective finalizate: {finalizate} / {total}")

    badgeuri_obtinute = set(user.badges.values_list('name', flat=True))

    if finalizate >= 1 and "Început de călătorie" not in badgeuri_obtinute:
        badge, created = Badge.objects.get_or_create(
            name="Început de călătorie",
            defaults={"description": "Ai finalizat primul tău obiectiv!"}
        )
        badge.users.add(user)
        print("🏅 Acordat: Început de călătorie")


    if total > 0 and finalizate == total and "100% completat" not in badgeuri_obtinute:
        badge, created = Badge.objects.get_or_create(
            name="100% completat",
            defaults={"description": "Ai finalizat toate obiectivele tale!"}
        )
        badge.users.add(user)
        print("🏆 Acordat: 100% completat")
