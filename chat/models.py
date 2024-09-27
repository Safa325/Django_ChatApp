from django.db import models
from django.db.models.fields import DateField
from datetime import date
from django.conf import settings

class Chat(models.Model):
    """
    Das Chat-Modell repräsentiert einen Chatroom oder eine Konversation.
    
    Attribute:
        created_at (DateField): Das Datum, an dem der Chat erstellt wurde. 
        Standardmäßig wird das heutige Datum verwendet.
    """
    created_at = models.DateField(default=date.today)

    def __str__(self):
        return f"Chat {self.id} created on {self.created_at}"

class Message(models.Model):
    """
    Das Message-Modell repräsentiert eine einzelne Nachricht innerhalb eines Chats.
    
    Attribute:
        text (CharField): Der Inhalt der Nachricht, begrenzt auf 500 Zeichen.
        created_at (DateField): Das Datum, an dem die Nachricht erstellt wurde. 
        Standardmäßig wird das heutige Datum verwendet.
        chat (ForeignKey): Die Referenz zum zugehörigen Chat. Wenn der Chat gelöscht wird, 
        werden alle zugehörigen Nachrichten ebenfalls gelöscht.
        author (ForeignKey): Der Benutzer, der die Nachricht gesendet hat. 
        Verknüpft mit dem benutzerdefinierten Benutzer-Modell (AUTH_USER_MODEL).
        receiver (ForeignKey): Der Benutzer, der die Nachricht erhält. 
        Verknüpft mit dem benutzerdefinierten Benutzer-Modell (AUTH_USER_MODEL).
    """
    text = models.CharField(max_length=500)
    created_at = models.DateField(default=date.today)
    chat = models.ForeignKey(
        Chat, 
        on_delete=models.CASCADE, 
        related_name='chat_message_set', 
        default=None, 
        blank=True, 
        null=True
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='author_message_set'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='receiver_message_set'
    )

    def __str__(self):
        return f"Message from {self.author} to {self.receiver} on {self.created_at}"
    