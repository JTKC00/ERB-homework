from django.shortcuts import render
from django.utils import timezone
from meetings.models import Meeting

def home(request):
    recent_meetings = Meeting.objects.filter(date__lte=timezone.now()).order_by('-date')[:5]
    return render(request, 'pages/home.html', {'recent_meetings': recent_meetings})