from django.shortcuts import render
from django.utils import timezone
from meetings.models import Meeting, Attachment, AgendaItem

def home(request):
    # 獲取最近的會議
    recent_meetings = Meeting.objects.filter(date__lte=timezone.now()).order_by('-date')[:5]
    
    # 獲取統計資訊
    meetings_count = Meeting.objects.count()
    attachments_count = Attachment.objects.count()
    agenda_items_count = AgendaItem.objects.count()
    
    # 傳遞數據到模板
    context = {
        'recent_meetings': recent_meetings,
        'meetings_count': meetings_count,
        'attachments_count': attachments_count,
        'agenda_items_count': agenda_items_count
    }
    
    return render(request, 'pages/home.html', context)