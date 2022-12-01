from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Message, World

def index(request):
    print(request.method)
    if request.method == "POST":
        print(request.POST)
        obj = World()
        obj.roomname = request.POST['roomname']
        obj.username = request.POST['username']
        obj.securitylevel = request.POST['securitylevel']
        obj.save()
        return HttpResponseRedirect(obj.roomname + '/?username=' + obj.username)
        #obj.roomname = request.POST
    return render(request, 'chat/index.html')

def room(request, room_name):
    print(request.GET, request.POST)
    username = request.GET.get('username', 'Anonymous')
    messages = Message.objects.filter(room=room_name)[0:25]
    World_obj = World.objects.get(roomname = room_name, username=username)
    print("obtained objects: ", World_obj)
    #field_object = World._meta.get_field('securitylevel')
    World_obj_security_level= getattr(World_obj, 'securitylevel')
    # print("obtained objects: ", World_obj, World_obj_field_value)
    
    return render(request, 'chat/room' + World_obj_security_level + '.html', {'worldobj': World_obj, 'room_name': room_name, 'username': username, 'messages': messages})