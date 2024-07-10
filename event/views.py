from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventForm
from django.contrib.auth.decorators import login_required,permission_required
from .models import Event
from datetime import date, datetime, timezone
from calendar import monthrange, month_name
from django.http import HttpResponseRedirect
from django.utils import timezone

@login_required
@permission_required('event.add_event', raise_exception=True)
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.instance.created_by = request.user
            form.save()
            return redirect('event:calendar')
    else:
        form = EventForm()
    return render(request, 'event/create_event.html', {'form': form})

@login_required
def calendar_view(request, year=None, month=None):
    if year is None or month is None:
        current_date = timezone.localtime()
        year = current_date.year
        month = current_date.month

    _, num_days = monthrange(year, month)

    days_of_month = list(range(1, num_days + 1))

    events = Event.objects.filter(start_time__year=year, start_time__month=month)
    
    month_name_str = month_name[month]
    
    prev_year, prev_month = (year, month - 1) if month > 1 else (year - 1, 12)
    next_year, next_month = (year, month + 1) if month < 12 else (year + 1, 1)

    context = {
        'days_of_month': days_of_month,
        'events': events,
        'year': year,
        'month': month,
        'month_name': month_name_str,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
    }

    return render(request, 'event/calendar.html', context)
