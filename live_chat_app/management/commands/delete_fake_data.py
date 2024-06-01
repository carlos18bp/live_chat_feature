from django.core.management.base import BaseCommand
from live_chat_app.models import Chat, Message, User

class Command(BaseCommand):
    help = 'Create rake records in the database'

    """
    To delete fake data via console, run:
    python3 manage.py delete_fake_data
    """
    def handle(self, *args, **options):
        Chat.objects.all().delete()
        Message.objects.all().delete()
        User.objects.all().delete()