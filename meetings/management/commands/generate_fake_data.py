from meetings.models import Meeting, AgendaItem, Attachment
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import tempfile
from django.core.files import File
from datetime import timedelta

fake = Faker()

class Command(BaseCommand):
    help = 'Generates fake data for meetings, agenda items, and attachments.'

    def add_arguments(self, parser):
        parser.add_argument('--num_meetings', type=int, default=5, help='Number of meetings to generate')

    def handle(self, *args, **options):
        num_meetings = options['num_meetings']
        for _ in range(num_meetings):
            # 產生會議日期與時間
            start_dt = fake.date_time_this_year(tzinfo=timezone.get_current_timezone())
            end_dt = start_dt + timedelta(hours=fake.random_int(min=1, max=4))
            
            meeting = Meeting.objects.create(
                title=fake.sentence(),
                date=start_dt.date(),
                start_time=start_dt.time(),
                end_time=end_dt.time(),
                location=fake.city(),
                attendees=", ".join([fake.name() for _ in range(3)]),
                minutes=fake.paragraph()
            )
            for i in range(3):
                AgendaItem.objects.create(
                    meeting=meeting,
                    item_number=i + 1,
                    item_title=fake.sentence(),
                    description=fake.paragraph(),
                    responsible_person=fake.name(),
                    estimated_time=timedelta(minutes=fake.random_int(min=10, max=30))
                )
            with tempfile.NamedTemporaryFile(delete=False, mode='w+', suffix='.txt') as tmp:
                tmp.write(fake.text())
                tmp.flush()
                with open(tmp.name, 'rb') as f:
                    Attachment.objects.create(
                        meeting=meeting,
                        file=File(f, name=f"attachment_{fake.uuid4()}.txt")
                    )

        self.stdout.write(self.style.SUCCESS(f'Successfully generated {num_meetings} fake meetings'))
#use faker to create fake data for the meeting app
# This command can be run using: python manage.py generate_fake_data()
# This script generates fake data for the Meeting, AgendaItem, and Attachment models.
# This command can be run using: python manage.py generate_fake_data --num_meetings 10
# It will create 10 fake meetings, each with 3 agenda items and one attachment.
# Adjust the number of meetings by changing the --num_meetings argument.
# Make sure to have the Faker library installed in your environment.
# You can install it using pip: pip install Faker