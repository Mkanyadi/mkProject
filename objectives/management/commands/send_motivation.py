from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from django.core.mail import send_mail
from objectives.models import Objective


class Command(BaseCommand):
    help = 'Trimite emailuri motivaționale utilizatorilor inactivi'

    def handle(self, *args, **kwargs):
        thirty_days_ago = timezone.now() - timedelta(days=30)
        users = User.objects.all()

        for user in users:
            obiective_recent = Objective.objects.filter(
                user=user,
                completed=True,
                updated_at__gte=thirty_days_ago
            )
            if not obiective_recent.exists():
                send_mail(
                    subject='📣 Îți amintești de obiectivele tale?',
                    message=(
                        f'Salut, {user.username}!\n\n'
                        'Se pare că nu ai completat niciun obiectiv în ultima lună. '
                        'E momentul perfect să-ți amintești de lista ta și să faci un pas mic spre visul tău!\n\n'
                        'Intră acum și adaugă sau bifează un obiectiv pe TripMania! 🚀'
                    ),
                    from_email='no-reply@tripmania.ro',
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                self.stdout.write(f"Email trimis către: {user.email}")

else:
self.stdout.write(f"ℹ️ {user.email} are obiective recente.")
