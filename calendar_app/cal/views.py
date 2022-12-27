from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from datetime import timedelta, datetime, date
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import calendar

from cal.models.event import Event
from cal.utils import Calendar
from cal.forms import EventForm

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = f"month={str(prev_month.year)}-{str(prev_month.month)}"
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = f"month={str(next_month.year)}-{str(next_month.month)}"
    return month

class CalendarView(LoginRequiredMixin, ListView):
    login_url = "accounts:signin" #where users will be redirected to if unsuccessful
    model = Event
    template_name = 'calendar.html'

    #override method in order to add more to context than the generic event_list of objects
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(self.request.user, withyear=True)

        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

"""
View for page to create new event.
"""
@login_required(login_url="signup")  #redirects user if not logged in
def event_new(request):
    form = EventForm()
    context = {
        'form': form
    }
    return render(request, "event.html", context)


"""
View that processes POST to create new event then redirects to the calendar
"""
def create_event(request):
    print("inside create event")
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data["title"]
        description = form.cleaned_data["description"]
        start_time = form.cleaned_data["start_time"]
        end_time = form.cleaned_data["end_time"]
        Event.objects.get_or_create(
            user=request.user,
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time
        )
        return HttpResponseRedirect(reverse("cal:calendar"))

    context = {
        "form": form
    }
    return render(request, "event.html", context)


"""
View for seeing details of an event.
"""
@login_required(login_url="accounts:signup")
def event_details(request, event_id):
    event = Event.objects.get(id=event_id)
    context = {
        "event": event,
        "event_id": event_id,
    }
    return render(request, "event_detail.html", context)


"""
View to remove an event. Triggered from event details and reroutes to calendar.
"""
def delete_event(request, event_id):
    event = Event.objects.get(id=event_id)
    event.delete()
    return HttpResponseRedirect(reverse("cal:calendar"))
