from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Room, Message
from django.core.exceptions import ObjectDoesNotExist
import subprocess

# Create your views here.

#section de demarrage de la video
def run_script(request):
    try:
        # Chemin vers le fichier Python à exécuter
        result = subprocess.run(['python', '/Livechat/templates/video_consultation.py'], capture_output=True, text=True)

        # Si vous voulez retourner la sortie du script
        return HttpResponse(f"Script exécuté avec succès !\n{result.stdout}")

    except Exception as e:
        return HttpResponse(f"Erreur lors de l'exécution du script : {str(e)}", status=500)
#fin de la section video


def home(request):
    return render(request, 'home.html')


def room(request, room):
    username = request.GET.get('username')

    # Essayer de récupérer les détails de la salle
    room_details, created = Room.objects.get_or_create(name=room)

    # Si la salle est nouvellement créée, `created` sera True
    if created:
        # Informer que la salle a été créée (facultatif)
        print(f"Salle {room} créée.")

    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })


def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    # Vérification si la salle existe, sinon elle est créée
    room_details, created = Room.objects.get_or_create(name=room)

    # Rediriger vers la salle avec l'utilisateur
    return redirect('/' + room + '/?username=' + username)


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']
    
    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        return HttpResponse("La salle n'existe pas.", status=404)

    new_message = Message.objects.create(value=message, user=username, room=room)
    new_message.save()
    
    return HttpResponse('Message envoyé avec succès')


def getMessages(request, room):
    try:
        room_details = Room.objects.get(name=room)
    except Room.DoesNotExist:
        return JsonResponse({"error": "La salle n'existe pas."}, status=404)

    # Récupérer les messages associés à la salle, triés par date
    messages = Message.objects.filter(room=room_details).order_by('date')

    # Conversion des messages en format JSON
    return JsonResponse({"messages": list(messages.values())})
