from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from tasks.models import Task
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Send reminders for upcoming tasks'

    def handle(self, *args, **kwargs):
        upcoming_tasks = Task.objects.filter(due_date__lte=datetime.now() + timedelta(days=1))
        for task in upcoming_tasks:
            send_mail(
                'Task Reminder',
                f'Reminder: Your task "{task.title}" is due on {task.due_date}.',
                'rajanyd666@gmail.com',
                [task.user.email],
                fail_silently=False,
            )
        self.stdout.write(self.style.SUCCESS('Successfully sent reminders'))
