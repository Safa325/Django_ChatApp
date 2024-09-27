from django.contrib import admin
from chat.models import Message
from chat.models import Chat

class MessageAdmin(admin.ModelAdmin):
    """
    Admin-Konfiguration für das Message-Modell.

    Diese Klasse definiert, wie das Message-Modell im Django Admin-Interface dargestellt wird.

    Attribute:
        fields (tuple): Eine Liste der Felder, die im Admin-Formular angezeigt werden.
        list_display (tuple): Eine Liste der Felder, die in der Admin-Liste angezeigt werden.
        search_fields (tuple): Eine Liste der Felder, nach denen in der Admin-Oberfläche gesucht werden kann.
    """
    fields = ('chat', 'author', 'text', 'created_at', 'receiver')
    list_display = ('created_at', 'author', 'chat', 'text', 'receiver')
    search_fields = ('text',)

class ChatAdmin(admin.ModelAdmin):
    """
    Admin-Konfiguration für das Chat-Modell.

    Diese Klasse definiert, wie das Chat-Modell im Django Admin-Interface dargestellt wird.

    Attribute:
        fields (tuple): Eine Liste der Felder, die im Admin-Formular angezeigt werden.
        list_display (tuple): Eine Liste der Felder, die in der Admin-Liste angezeigt werden.
    """
    fields = ('created_at',)
    list_display = ('created_at',)

# Register your models here.
# Registriert das Message- und Chat-Modell zusammen mit ihren jeweiligen Admin-Konfigurationen im Django Admin-Interface.
admin.site.register(Message, MessageAdmin)
admin.site.register(Chat, ChatAdmin)
