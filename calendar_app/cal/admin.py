from django.contrib import admin
from cal.models.event import Event

class EventAdmin(admin.ModelAdmin):
    pass

admin.site.register(Event, EventAdmin)
