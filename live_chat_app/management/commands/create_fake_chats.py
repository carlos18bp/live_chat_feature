from faker import Faker
from django.core.management.base import BaseCommand
from live_chat_app.models import User, Chat, Message
import random
from django.utils import timezone

class Command(BaseCommand):
    help = 'Create fake chat records in the database'

    def add_arguments(self, parser):
        parser.add_argument('number_of_chats', type=int, nargs='?', default=10)

    def handle(self, *args, **options):
        number_of_chats = options['number_of_chats']
        fake = Faker()

        # Ensure there is an admin user
        admin_email = 'admin@example.com'
        admin, created = User.objects.get_or_create(
            email=admin_email,
            defaults={
                'first_name': 'Admin',
                'last_name': 'Web Site',
            }
        )

        for _ in range(number_of_chats):
            user, created = User.objects.get_or_create(
                email=fake.email(),
                defaults={
                    'first_name': fake.first_name(),
                    'last_name': fake.last_name(),
                }
            )
            chat = Chat.objects.create(user=user, admin=admin)
            last_message_time = None

            for _ in range(random.randint(2, 10)):
                sender = random.choice([user, admin])
                message_time = fake.date_time_this_year(tzinfo=timezone.get_current_timezone())
                message = Message.objects.create(
                    chat=chat,
                    user=sender,
                    text=fake.text(max_nb_chars=200),
                    created_at=message_time,
                )
                if not last_message_time or message_time > last_message_time:
                    last_message_time = message_time

            chat.last_message_timestamp = last_message_time
            chat.save()

        self.stdout.write(self.style.SUCCESS(f'{number_of_chats} chats created'))
