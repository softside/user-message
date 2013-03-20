from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.contrib.auth.models import Group

from message.models import Message, MessageContact


class MessageAdmin(admin.ModelAdmin):
    """ Admin message class with inline recipients """

    fieldsets = (
        (None, {
            'fields': (
                'sender', 'body',
            ),
            'classes': ('monospace' ),
        }),
        (_('Date/time'), {
            'fields': (
                'sender_deleted_at',
            ),
            'classes': ('collapse', 'wide'),
        }),
    )
    list_display = ('sender', 'body', 'sent_at')
    list_filter = ('sent_at', 'sender')
    search_fields = ('body',)

admin.site.register(Message, MessageAdmin)
admin.site.register(MessageContact)
