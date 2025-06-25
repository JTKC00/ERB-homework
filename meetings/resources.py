# meetings/resources.py
from import_export import resources
from .models import Meeting, AgendaItem, Attachment
from import_export.fields import Field

class MeetingResource(resources.ModelResource):
    class Meta:
        model = Meeting
        fields = ('title', 'date', 'start_time', 'end_time', 'location', 'attendees', 'minutes')
        import_id_fields = ('title',)  # 用於匹配現有記錄

class AgendaItemResource(resources.ModelResource):
    class Meta:
        model = AgendaItem
        fields = ('meeting', 'item_number', 'item_title', 'description', 'responsible_person', 'estimated_time')

class AttachmentResource(resources.ModelResource):
    class Meta:
        model = Attachment
        fields = ('meeting', 'file')