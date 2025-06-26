from django.urls import path
from . import views

app_name = 'meetings'

urlpatterns = [
    path('', views.meeting_list, name='meeting_list'),
    path('meeting/<int:meeting_id>/', views.meeting_detail, name='meeting_detail'),
    path('meeting/<int:meeting_id>/upload/', views.upload_attachment, name='upload_attachment'),
    path('meeting/<int:meeting_id>/generate_meeting_doc/', views.generate_meeting_doc, name='generate_meeting_doc'),
    path('export/', views.export_meetings, name='export_meetings'),
    path('import/', views.import_meetings, name='import_meetings'),
    path('meeting/<int:meeting_id>/delete/', views.delete_meeting, name='delete_meeting'),  # 新增刪除路由
    path('delete-selected/', views.delete_selected_meetings, name='delete_selected_meetings'),  # 新增批量刪除路由
    path('delete_all/', views.delete_all_meetings, name='delete_all_meetings'),  # 新增批量刪除所有會議路由
    path('attachment/<int:attachment_id>/delete/', views.delete_attachment, name='delete_attachment'),  # 刪除附件路由
]