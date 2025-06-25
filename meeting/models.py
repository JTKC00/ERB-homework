from django.db import models

# Create your models here.
class Meeting(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=100)
    attendees = models.TextField()
    minutes = models.TextField(blank=True, null=True, help_text="會議記錄詳細內容")

class AgendaItem(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    item_number = models.IntegerField()
    item_title = models.CharField(max_length=200)
    description = models.TextField()
    responsible_person = models.CharField(max_length=100)
    estimated_time = models.DurationField()