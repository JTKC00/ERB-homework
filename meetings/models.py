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

class Attachment(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/%Y/%m/%d/', help_text="上傳會議附件 (PPT, Word, Excel)")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_type = models.CharField(max_length=50, blank=True, help_text="文件類型 (如 PPT, Word)")

    def __str__(self):
        return f"{self.file.name}"