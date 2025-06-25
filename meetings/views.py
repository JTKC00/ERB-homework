import os
from django.shortcuts import render, redirect, get_object_or_404
from .models import Meeting, AgendaItem, Attachment
from docx import Document
from django.core.files.storage import default_storage
from django.http import HttpResponse, HttpResponseBadRequest
from .resources import MeetingWithDetailsResource
from tablib import Dataset
from django.core.paginator import Paginator
import zipfile
from django.core.exceptions import ObjectDoesNotExist
from django.utils.text import slugify
from django.db.models import Q
from django.contrib import messages

# Create your views here.

def meeting_detail(request, meeting_id):
    meeting = Meeting.objects.get(id=meeting_id)
    agenda_items = AgendaItem.objects.filter(meeting=meeting)
    attachments = Attachment.objects.filter(meeting=meeting)
    return render(request, 'meetings/meeting_detail.html', {
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
    try:
        # 獲取會議數據
        meeting = Meeting.objects.get(id=meeting_id)
        agenda_items = AgendaItem.objects.filter(meeting=meeting)
        attachments = Attachment.objects.filter(meeting=meeting)

        # 創建臨時目錄
        temp_dir = default_storage.path('temp_' + str(meeting_id))
        os.makedirs(temp_dir, exist_ok=True)

        # 格式化文件名：使用日期和標題
        date_str = meeting.date.strftime('%Y-%m-%d')
        title_slug = slugify(meeting.title)[:50]  # 限制長度，避免文件名過長
        base_name = f'{date_str}_{title_slug}'

        # 生成會議記錄文件
        meeting_doc = Document()
        meeting_doc.add_heading(f'會議記錄: {meeting.title}', level=1)
        meeting_doc.add_paragraph(f'日期: {meeting.date}')
        meeting_doc.add_paragraph(f'時間: {meeting.start_time} - {meeting.end_time}')
        meeting_doc.add_paragraph(f'地點: {meeting.location}')
        meeting_doc.add_paragraph(f'參加人: {meeting.attendees}')
        meeting_doc.add_paragraph(f'記錄: {meeting.minutes or "無記錄"}')
        meeting_file = os.path.join(temp_dir, f'{base_name}_record.docx')
        meeting_doc.save(meeting_file)

        # 生成議程文件
        agenda_doc = Document()
        agenda_doc.add_heading(f'會議議程: {meeting.title}', level=1)
        for item in agenda_items:
            agenda_doc.add_paragraph(f'{item.item_number}. {item.item_title} - {item.description} '
                                  f'(負責人: {item.responsible_person}, 時間: {item.estimated_time})')
        agenda_file = os.path.join(temp_dir, f'{base_name}_agenda.docx')
        agenda_doc.save(agenda_file)

        # 生成附件文件（列出附件信息）
        attachment_doc = Document()
        attachment_doc.add_heading(f'會議附件: {meeting.title}', level=1)
        if attachments.exists():
            for attachment in attachments:
                attachment_doc.add_paragraph(f'文件名: {attachment.file.name} '
                                          f'(連結: {attachment.file.url})')
        else:
            attachment_doc.add_paragraph('無附件')
        attachment_file = os.path.join(temp_dir, f'{base_name}_attachments.docx')
        attachment_doc.save(attachment_file)

        # 壓縮為 ZIP 文件
        zip_path = default_storage.path(f'{base_name}_files.zip')
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(meeting_file, os.path.basename(meeting_file))
            zipf.write(agenda_file, os.path.basename(agenda_file))
            zipf.write(attachment_file, os.path.basename(attachment_file))

        # 回傳 ZIP 文件
        with open(zip_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{base_name}_files.zip"'
            return response

    except ObjectDoesNotExist:
        return HttpResponse("會議不存在", status=404)
    except Exception as e:
        return HttpResponse(f"生成文件失敗: {str(e)}", status=500)
    finally:
        # 清理臨時文件和目錄
        if os.path.exists(temp_dir):
            for file in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, file))
            os.rmdir(temp_dir)
        if os.path.exists(zip_path):
            os.remove(zip_path)


def export_meetings(request):
    meeting_resource = MeetingWithDetailsResource()
    dataset = meeting_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="meetings_with_details.csv"'
    return response

def import_meetings(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()

        try:
            if file_extension in ['.csv']:
                # 處理 CSV 文件
                dataset = Dataset()
                imported_data = dataset.load(uploaded_file.read().decode('utf-8'), format='csv')
                meeting_resource = MeetingResource()
                result = meeting_resource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    import_result = meeting_resource.import_data(dataset, dry_run=False)
                    imported_count = len(import_result.rows)  # 獲取導入的記錄數
                    return render(request, 'import/import_success.html', {'imported_count': imported_count})
                else:
                    return render(request, 'import/import_error.html', {'errors': result.errors})

            elif file_extension in ['.txt', '.docx']:
                # 處理 TXT 或 Word 文件
                meetings_data = []
                if file_extension == '.txt':
                    content = uploaded_file.read().decode('utf-8')
                    lines = content.splitlines()
                    for line in lines:
                        if line.strip():
                            parts = line.split(',')
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
                return render(request, 'import/import_success.html')

            else:
                return render(request, 'import/import_error.html', {'errors': ['不支持的文件格式。']})

        except Exception as e:
            return render(request, 'import/import_error.html', {'errors': [str(e)]})

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
    # 初始查詢集
    meetings = Meeting.objects.all()

    # 搜索功能
    search_query = request.GET.get('q')
    if search_query:
        meetings = meetings.filter(
            Q(title__icontains=search_query) | Q(attendees__icontains=search_query)
        )

    # 過濾功能
    date_filter = request.GET.get('date')
    if date_filter:
        meetings = meetings.filter(date=date_filter)

    location_filter = request.GET.get('location')
    if location_filter:
        meetings = meetings.filter(location__icontains=location_filter)

    # 排序功能
    sort_by = request.GET.get('sort', '-date')  # 默認按日期降序
    if sort_by in ['date', '-date', 'title', '-title']:
        meetings = meetings.order_by(sort_by)
    else:
        meetings = meetings.order_by('-date')  # 默認排序

    # 分頁功能
    paginator = Paginator(meetings, 15)  # 每頁15個會議
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 傳遞參數到模板
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'date_filter': date_filter,
        'location_filter': location_filter,
        'sort_by': sort_by,
    }
    return render(request, 'meetings/meeting_list.html', context)

def delete_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    if request.method == 'POST':
        meeting.delete()
        messages.success(request, '會議已成功刪除。')
        return redirect('meetings:meeting_list')
    return render(request, 'meetings/confirm_delete.html', {'meeting': meeting})

def delete_selected_meetings(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_meetings')
        if not selected_ids:
            return HttpResponseBadRequest("請選擇至少一個會議。")
        meetings = Meeting.objects.filter(id__in=selected_ids)
        if meetings.exists():
            meetings.delete()
            messages.success(request, f'成功刪除了 {meetings.count()} 個會議。')
        return redirect('meetings:meeting_list')
    return HttpResponseBadRequest("無效請求。")