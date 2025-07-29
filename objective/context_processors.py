from datetime import timedelta
from django.utils import timezone
from .models import Objective

def obiective_finalizate_luna(request):
    if request.user.is_authenticated:
        acum = timezone.now()
        ultima_luna = acum - timedelta(days=30)
        nr_finalizate = Objective.objects.filter(
            user=request.user,
            completed=True,
            updated_at__gte=ultima_luna
        ).count()
    else:
        nr_finalizate = 0

    return {'obiective_finalizate_recent': nr_finalizate}