# meetings/resources.py
from import_export import resources
from .models import Meeting, AgendaItem, Attachment
from import_export.fields import Field
import os

class MeetingWithDetailsResource(resources.ModelResource):
    agenda_items = Field(column_name='Agenda Items')
    attachments = Field(column_name='Attachments')

    class Meta:
        model = Meeting
        fields = ('id', 'title', 'date', 'start_time', 'end_time', 'location', 'attendees', 'minutes', 'agenda_items', 'attachments')
        export_order = ('id', 'title', 'date', 'start_time', 'end_time', 'location', 'attendees', 'minutes', 'agenda_items', 'attachments')

    def dehydrate_agenda_items(self, meeting):
        # 獲取所有議程項並格式化
        agenda_items = AgendaItem.objects.filter(meeting=meeting)
        if agenda_items.exists():
            return "; ".join([f"{item.item_number}. {item.item_title} (負責人: {item.responsible_person})" for item in agenda_items])
        return "無議程項"

    def dehydrate_attachments(self, meeting):
        # 獲取所有附件，只顯示檔案名稱和類型
        attachments = Attachment.objects.filter(meeting=meeting)
        if attachments.exists():
            attachment_info = []
            for attachment in attachments:
                file_name = os.path.basename(attachment.file.name)
                file_type = attachment.file_type or os.path.splitext(file_name)[1].replace('.', '')
                attachment_info.append(f"{file_name} ({file_type})")
            return "; ".join(attachment_info)
        return "無附件"