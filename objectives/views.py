from django.shortcuts import render

# Create your views here.


from django.shortcuts import render

from django.shortcuts import render, redirect
from .models import Objective
from .forms import ObjectiveForm


def home(request):
    objectives = Objective.objects.all()
    return render(request, 'objectives/home.html', {'objectives': objectives})


def add_objective(request):
    if request.method == "POST":
        form = ObjectiveForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('home')
    else:
        form = ObjectiveForm()
    return render(request, 'objectives/add_objective.html', {'form': form})