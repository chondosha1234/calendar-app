from datetime import datetime, timedelta
from calendar import HTMLCalendar
from cal.models import Event
from django.utils.safestring import mark_safe

class Calendar(HTMLCalendar):

    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatday(self, day, events):
        events_per_day = events.filter(start_time__day=day)
        d = ''
        for event in events_per_day:
            d += f'<li class="calendar-list"> {event.get_html_url} </li>'  #{event.get_html_url}   {str(event)}
        if day:
            return f'<td><span class="date">{day}</span><ul class="event-list">{d}</ul></td>'
        else:
            return '<td></td>'

    def formatweek(self, week, events):
        w = ''
        for d, weekday in week:
            w += self.formatday(d, events)
        return f'<tr> {w} </tr>'

    def formatmonth(self, withyear=True):
        events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month)
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        cal += f'</table>'

        return cal
