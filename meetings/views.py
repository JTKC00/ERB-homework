import os
from django.shortcuts import render, redirect
from django.http import FileResponse
from .models import Meeting, AgendaItem, Attachment
from docx import Document
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse
from .resources import MeetingResource, AgendaItemResource, AttachmentResource
from tablib import Dataset
from django.core.paginator import Paginator
# Create your views here.

def meeting_detail(request, meeting_id):
    meeting = Meeting.objects.get(id=meeting_id)
    agenda_items = AgendaItem.objects.filter(meeting=meeting)
    attachments = Attachment.objects.filter(meeting=meeting)
    return render(request, 'meetings/detail.html', {
        'meeting': meeting,
        'agenda_items': agenda_items,
        'attachments': attachments,
    })

def upload_attachment(request, meeting_id):
    if request.method == 'POST' and request.FILES.get('attachment_file'):
        meeting = Meeting.objects.get(id=meeting_id)
        attachment = Attachment(meeting=meeting)
        attachment.file = request.FILES['attachment_file']
        attachment.save()
        return redirect('meeting_detail', meeting_id=meeting.id)
    return render(request, 'meetings/upload.html', {'meeting_id': meeting_id})

def generate_meeting_doc(request, meeting_id):
    meeting = Meeting.objects.get(id=meeting_id)
    doc = Document()
    doc.add_heading(f'會議記錄: {meeting.title}', level=1)
    doc.add_paragraph(f'日期: {meeting.date}\n時間: {meeting.start_time} - {meeting.end_time}')
    doc.add_paragraph(f'地點: {meeting.location}\n參加人: {meeting.attendees}')
    doc.add_paragraph(f'記錄: {meeting.minutes or "無記錄"}')
    temp_file = f'meeting_{meeting.id}.docx'
    doc.save(temp_file)

    with open(temp_file, 'rb') as f:
        response = FileResponse(f, as_attachment=True, filename=temp_file)
        return response
    
    # meetings/views.py


def export_meetings(request):
    meeting_resource = MeetingResource()
    dataset = meeting_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="meetings.csv"'
    return response

def import_meetings(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()

        try:
            if file_extension in ['.csv']:
                # 处理 CSV 文件
                dataset = Dataset()
                imported_data = dataset.load(uploaded_file.read().decode('utf-8'), format='csv')
                meeting_resource = MeetingResource()
                result = meeting_resource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    meeting_resource.import_data(dataset, dry_run=False)
                    return render(request, 'import_success.html')
                else:
                    return render(request, 'import_error.html', {'errors': result.errors})

            elif file_extension in ['.txt', '.docx']:
                # 处理 TXT 或 Word 文件
                meetings_data = []
                if file_extension == '.txt':
                    content = uploaded_file.read().decode('utf-8')
                    lines = content.splitlines()
                    for line in lines:
                        if line.strip():
                            parts = line.split(',')
                            if len(parts) >= 6:  # 假设格式: title,date,start_time,end_time,location,attendees
                                meetings_data.append({
                                    'title': parts[0].strip(),
                                    'date': parts[1].strip(),
                                    'start_time': parts[2].strip(),
                                    'end_time': parts[3].strip(),
                                    'location': parts[4].strip(),
                                    'attendees': parts[5].strip(),
                                    'minutes': parts[6].strip() if len(parts) > 6 else ''
                                })
                elif file_extension == '.docx':
                    doc = Document(uploaded_file)
                    for para in doc.paragraphs:
                        if para.text.strip():
                            parts = para.text.split(',')
                            if len(parts) >= 6:
                                meetings_data.append({
                                    'title': parts[0].strip(),
                                    'date': parts[1].strip(),
                                    'start_time': parts[2].strip(),
                                    'end_time': parts[3].strip(),
                                    'location': parts[4].strip(),
                                    'attendees': parts[5].strip(),
                                    'minutes': parts[6].strip() if len(parts) > 6 else ''
                                })

                for data in meetings_data:
                    Meeting.objects.update_or_create(
                        title=data['title'],
                        defaults={
                            'date': data['date'],
                            'start_time': data['start_time'],
                            'end_time': data['end_time'],
                            'location': data['location'],
                            'attendees': data['attendees'],
                            'minutes': data['minutes']
                        }
                    )
                return render(request, 'import_success.html')

            else:
                return render(request, 'import_error.html', {'errors': ['不支持的文件格式。']})

        except Exception as e:
            return render(request, 'import_error.html', {'errors': [str(e)]})

    return render(request, 'import/import_form.html')

def meeting_detail(request, meeting_id):
    meeting = Meeting.objects.get(id=meeting_id)
    agenda_items = AgendaItem.objects.filter(meeting=meeting)
    attachments = Attachment.objects.filter(meeting=meeting)
    return render(request, 'meetings/meeting_detail.html', {
        'meeting': meeting,
        'agenda_items': agenda_items,
        'attachments': attachments,
    })

def meeting_list(request):
    meetings = Meeting.objects.all().order_by('-date')
    paginator = Paginator(meetings, 15)  # 每頁15個
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'meetings/meeting_list.html', {'page_obj': page_obj})