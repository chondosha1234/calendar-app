from django.db import models
from django.urls import reverse
from datetime import datetime
from accounts.models import User


# Create your models here.
class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
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
