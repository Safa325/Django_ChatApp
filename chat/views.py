from django.shortcuts import render, redirect
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from .models import Chat, Message
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.core import serializers

@login_required(login_url='/login/')
def index(request):
    """
    Die Hauptansicht für den Chatroom.

    Wenn eine POST-Anfrage empfangen wird, wird eine neue Nachricht im Chat erstellt und die Nachricht als JSON zurückgegeben.
    Andernfalls wird die Seite mit allen bisherigen Nachrichten gerendert.

    Anfragen:
        GET: Rendert die Chat-Seite mit allen Nachrichten im Chat.
        POST: Erstellt eine neue Nachricht und gibt diese als JSON zurück.

    Berechtigungen:
        Nur angemeldete Benutzer können diese Ansicht sehen. Nicht angemeldete Benutzer werden zur Login-Seite weitergeleitet.
    
    Parameter:
        request (HttpRequest): Das HttpRequest-Objekt mit Anfragen-Metadaten.

    Rückgabewerte:
        HttpResponse: Die gerenderte Chat-Seite oder eine JsonResponse mit der neuen Nachricht.
    """
    if request.method == 'POST':
        print("Received data, " + request.POST['textMessage'])
        myChat = Chat.objects.get(id=1)
        new_message = Message.objects.create(text=request.POST['textMessage'], chat=myChat, author=request.user, receiver=request.user)
        json_message = serializers.serialize('json', [new_message])
        json_Resonse = JsonResponse(json_message, safe=False)
        print(json_Resonse)
        return JsonResponse(json_message, safe=False)
   
    chatMessages = Message.objects.filter(chat__id=1)
    return render(request, 'chat/index.html', {
        'messages': chatMessages,
    })

def login_view(request):
    """
    Die Login-Ansicht für die Anwendung.

    Diese Ansicht authentifiziert den Benutzer anhand des Benutzernamens und des Passworts.
    Bei erfolgreicher Authentifizierung wird der Benutzer zur Chat-Seite weitergeleitet.
    Bei fehlgeschlagener Authentifizierung wird die Login-Seite mit einer Fehlermeldung neu gerendert.

    Anfragen:
        GET: Zeigt die Login-Seite an.
        POST: Verarbeitet die Login-Daten und authentifiziert den Benutzer.

    Parameter:
        request (HttpRequest): Das HttpRequest-Objekt mit Anfragen-Metadaten.

    Rückgabewerte:
        HttpResponse: Die gerenderte Login-Seite oder eine HttpResponseRedirect zur Chat-Seite.
    """
    redirect_url = request.GET.get('next', '/chat/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(request.POST.get('redirect', redirect_url))
        else: 
            return render(request, 'auth/login.html', {'wrongPassword': True, 'redirect': redirect_url})
    return render(request, 'auth/login.html', {'redirect': redirect_url})

def register_view(request):
    """
    Die Registrierung-Ansicht für neue Benutzer.

    Diese Ansicht ermöglicht es neuen Benutzern, sich zu registrieren. 
    Nach erfolgreicher Registrierung wird der Benutzer automatisch eingeloggt und zur Chat-Seite weitergeleitet.
    Falls die eingegebenen Passwörter nicht übereinstimmen oder der Benutzername bereits vergeben ist,
    wird eine Fehlermeldung angezeigt.

    Anfragen:
        GET: Zeigt die Registrierungsseite an.
        POST: Verarbeitet die Registrierungsdaten und erstellt ein neues Benutzerkonto.

    Parameter:
        request (HttpRequest): Das HttpRequest-Objekt mit Anfragen-Metadaten.

    Rückgabewerte:
        HttpResponse: Die gerenderte Registrierungsseite oder eine HttpResponseRedirect zur Chat-Seite.
    """
    redirect_url = request.GET.get('next', '/chat/')
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        
        if password != password_confirm:
            messages.error(request, "Die Passwörter stimmen nicht überein.")
            return render(request, 'auth/register.html', {'redirect': redirect_url})
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Der Benutzername ist bereits vergeben.")
            return render(request, 'auth/register.html', {'redirect': redirect_url})
        
        # Neuen Benutzer erstellen
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
       
        # Benutzer automatisch einloggen
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(redirect_url)
   
    return render(request, 'auth/register.html', {'redirect': redirect_url})

def logout_view(request):
    """
    Die Logout-Ansicht.

    Diese Ansicht meldet den aktuellen Benutzer ab und leitet ihn zur Chat-Seite weiter.

    Anfragen:
        GET: Führt das Logout durch und leitet den Benutzer zur Chat-Seite.

    Parameter:
        request (HttpRequest): Das HttpRequest-Objekt mit Anfragen-Metadaten.

    Rückgabewerte:
        HttpResponseRedirect: Eine Weiterleitung zur Chat-Seite nach dem Logout.
    """
    logout(request)  
    return redirect('/chat/')
