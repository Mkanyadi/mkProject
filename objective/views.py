from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.contrib.auth.models import User
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm, ObjectiveMemoryForm
from .models import Objective
from badge.models import Badge
from django.contrib import messages


BUCKET_OBJECTIVES = {
    "N01": {"title": "Santorini (Grecia)", "description": "Cină romantică pe o terasă cu vedere la mare."},
    "N02": {"title": "Japonia (Tokyo/Kyoto)", "description": "Privește cireșii în floare primăvara."},
    "N03": {"title": "Route 66 (SUA)", "description": "Aventură auto clasică de-a lungul Route 66 în SUA."},
    "N04": {"title": "Luminile Nordului (Norvegia, Islanda, Finlanda)", "description": "O noapte magică sub aurorele boreale."},
    "N05": {"title": "Machu Picchu (Peru)", "description": "O călătorie spre ruinele legendare ale incașilor."},
    "N06": {"title": "Safari în Africa (Kenya, Tanzania)", "description": "Leii, elefanții și peisaje spectaculoase."},
    "N07": {"title": "Tenerife (Spania)", "description": "Insula spaniolă plină de peisaje și minuni naturale."},
    "N08": {"title": "Tur cu rulotă", "description": "Călătorește cu o rulotă și descoperă lumea."},
    "N09": {"title": "Marea Barieră de Corali (Australia)", "description": "Un vis pentru orice scafandru."},
    "N10": {"title": "Crăciun în New York", "description": "Bradul de la Rockefeller și luminile din Times Square."},
    "N11": {"title": "Balon Cappadocia (Turcia)", "description": "Peisaje magice la răsărit."},
    "N12": {"title": "Înot cu delfinii", "description": "O experiență acvatică de vis."},
    "N13": {"title": "Maraton cu un prieten", "description": "Aleargă pentru sănătate și motivație împreună."},
    "N14": {"title": "Valea Loarei (Franța)", "description": "O aventură romantică printre nori."},
    "N15": {"title": "Laponia (Finlanda)", "description": "Privește stelele sub cerul polar."},
}


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

    def get(self, request):
        bucket = BUCKET_OBJECTIVES

        if request.user.is_authenticated:
            personal = Objective.objects.filter(user=request.user)
            user_titles = personal.values_list('title', flat=True)
        else:
            personal = Objective.objects.none()
            user_titles = []

        return render(request, self.template_name, {
            'bucket_list': bucket,
            'user_objectives': personal,
            'user_titles': list(user_titles),
        })

    def post(self, request):
        if request.user.is_authenticated:
            title = request.POST.get("title")
            description = request.POST.get("description")

            if title and description:
                already_exists = Objective.objects.filter(user=request.user, title=title).exists()
                if not already_exists:
                    Objective.objects.create(user=request.user, title=title, description=description)

        return redirect('bucket-list')


class AddObjectiveFromBucketView(LoginRequiredMixin, View):
    def post(self, request):
        title = request.POST.get('title')
        description = request.POST.get('description')
        if title and description:
            Objective.objects.create(user=request.user, title=title, description=description)
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


class ObjectiveMemoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Objective
    form_class = ObjectiveMemoryForm
    template_name = 'objectives/objective_memory_form.html'
    success_url = reverse_lazy('objective-list')

    def get_success_url(self):
        return reverse_lazy('objective-list')

    def get_queryset(self):
        return Objective.objects.filter(user=self.request.user)


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

    from datetime import timedelta
    from django.utils.timezone import now

    objectives = Objective.objects.filter(user=user)
    finalizate = objectives.filter(completed=True)
    total = objectives.count()
    finalizate_count = finalizate.count()
    badgeuri_obtinute = set(user.badges.values_list('name', flat=True))

    def acorda_badge(nume, descriere):
        if nume not in badgeuri_obtinute:
            badge, _ = Badge.objects.get_or_create(name=nume, defaults={"description": descriere})
            user.badges.add(badge)
            print(f"🏅 Acordat: {nume}")

    if finalizate_count >= 1:
        acorda_badge("Început de călătorie", "Ai finalizat primul tău obiectiv!")
    if total > 0 and finalizate_count == total:
        acorda_badge("100% completat", "Ai finalizat toate obiectivele tale!")
    if finalizate_count >= 5:
        acorda_badge("Explorer", "Ai finalizat 5 obiective!")
    if finalizate_count >= 10:
        acorda_badge("Aventurier", "Ai finalizat 10 obiective!")
    if finalizate_count >= 25:
        acorda_badge("Maestru al obiectivelor", "Ai finalizat 25 obiective!")
    if finalizate_count >= 50:
        acorda_badge("Legenda vieții", "Ai finalizat 50 obiective!")

    ultima_saptamana = now() - timedelta(days=7)
    recent = finalizate.filter(updated_at__gte=ultima_saptamana).count()
    if recent >= 3:
        acorda_badge("Momentum", "Ai finalizat 3 obiective în ultima săptămână!")

    zile_finalizate = finalizate.values_list("updated_at", flat=True)
    zile = [dt.date() for dt in zile_finalizate]
    for zi in set(zile):
        if zile.count(zi) >= 2:
            acorda_badge("Sprint final", "Ai finalizat 2 obiective în aceeași zi!")
            break

    if finalizate.filter(title__icontains="japonia").exists() or finalizate.filter(
            description__icontains="grecia").exists():
        acorda_badge("Călător", "Ai finalizat un obiectiv de tip travel!")

    if finalizate.filter(description__icontains="scris").exists() or finalizate.filter(
            description__icontains="pictat").exists():
        acorda_badge("Artist", "Ai atins un obiectiv creativ!")

    if finalizate.filter(description__icontains="sport").exists() or finalizate.filter(
            title__icontains="alergat").exists():
        acorda_badge("Sportiv", "Ai finalizat un obiectiv sportiv!")

    imagini = finalizate.exclude(image="").exclude(image=None).count()
    if imagini >= 5:
        acorda_badge("Amintiri vizuale", "Ai adăugat poze la 5 obiective!")
