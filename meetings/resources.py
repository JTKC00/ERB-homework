# meetings/resources.py
from import_export import resources
from .models import Meeting, AgendaItem, Attachment
from import_export.fields import Field

class MeetingWithDetailsResource(resources.ModelResource):
    agenda_items = Field(column_name='Agenda Items')
    attachments = Field(column_name='Attachments')

    class Meta:
        model = Meeting
        fields = ('id', 'title', 'date', 'start_time', 'end_time', 'location', 'attendees', 'minutes', 'agenda_items', 'attachments')
        export_order = ('id', 'title', 'date', 'start_time', 'end_time', 'location', 'attendees', 'minutes', 'agenda_items', 'attachments')

    def dehydrate_agenda_items(self, meeting):
        # 獲取所有議程項並格式化，添加調試
        agenda_items = AgendaItem.objects.filter(meeting=meeting)
        print(f"Debug: Meeting {meeting.id} has {agenda_items.count()} agenda items")
        if agenda_items.exists():
            return "; ".join([f"{item.item_number}. {item.item_title} (負責人: {item.responsible_person})" for item in agenda_items])
        return "無議程項"

    def dehydrate_attachments(self, meeting):
        # 獲取所有附件並格式化，添加調試
        attachments = Attachment.objects.filter(meeting=meeting)
        print(f"Debug: Meeting {meeting.id} has {attachments.count()} attachments")
        if attachments.exists():
            return "; ".join([attachment.file.name for attachment in attachments])
        return "無附件"