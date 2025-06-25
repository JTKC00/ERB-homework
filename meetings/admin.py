from django.contrib import admin
from django.utils.html import format_html
from .models import Meeting, AgendaItem, Attachment

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date', 'start_time', 'end_time', 'location', 'attendees', 'minutes')
    list_filter = ('date', 'location')  # 添加過濾器
    search_fields = ('title', 'attendees', 'minutes')  # 添加搜索欄

@admin.register(AgendaItem)
class AgendaItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'meeting', 'item_number', 'item_title', 'responsible_person', 'estimated_time')
    list_filter = ('meeting__date', 'responsible_person')  # 過濾會議日期和負責人
    search_fields = ('item_title', 'description', 'responsible_person')  # 搜索

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'meeting', 'display_file_name', 'uploaded_at')
    list_filter = ('meeting__date', 'uploaded_at')  # 過濾會議日期和上傳時間
    search_fields = ('file',)  # 搜索文件名

    def display_file_name(self, obj):
        return format_html('<a href="{}">{}</a>', obj.file.url, obj.file.name)
    display_file_name.short_description = 'File'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('meeting')