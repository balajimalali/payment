from django.shortcuts import render, HttpResponse
from payments.models import Show
from datetime import datetime, timedelta


def start(request):
    startdate = datetime.today()
    enddate = startdate + timedelta(days=1000)
    shows = Show.objects.filter(date__range=[startdate, enddate])
    return render(request, 'starter.html', {'shows': shows})
