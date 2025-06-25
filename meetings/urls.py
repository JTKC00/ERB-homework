from django.urls import path
from . import views

app_name = 'meetings'

urlpatterns = [
    path('', views.meeting_list, name='meeting_list'),
    path('meeting/<int:meeting_id>/', views.meeting_detail, name='meeting_detail'),
    path('meeting/<int:meeting_id>/upload/', views.upload_attachment, name='upload_attachment'),
    path('meeting/<int:meeting_id>/generate_doc/', views.generate_meeting_doc, name='generate_meeting_doc'),
    path('export/', views.export_meetings, name='export_meetings'),
    path('import/', views.import_meetings, name='import_meetings'),
]