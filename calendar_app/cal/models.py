from django.db import models
from django.urls import reverse
from datetime import datetime
#from django.core.exceptions import ValidationError

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('cal:event_details', args=[self.id])

    @property
    def get_html_url(self):
        url = reverse('cal:event_details', args=[self.id])
        return f'<a class="event-link" href="{url}">{self.title}</a>'

"""
    def check_overlap(self, fixed_start, fixed_end, new_start, new_end):
        if new_start == fixed_end or new_end == fixed_start:
            return False
        elif (new_start >= fixed_start and new_start <= fixed_end) or (new_end >= fixed_start and new_end <= fixed_end):
            return True
        elif new_start <= fixed_start and new_end >= fixed_end:
            return True
        return False


    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError('Ending time must be after start time')

        events = Event.objects.filter(day=self.day)
        if events.exists():
            for event in events:
                if self.check_overlap(event.start_time, event.end_time, self.start_time, self.end_time):
                    raise ValidationError('There is an overlap with another event: ' + str(event.day) + ', ' + str(event.start_time) + '--' + str(event.end_time))
"""
