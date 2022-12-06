from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Message, World
from .rsa import get_prime_num, key_pair, encrypt, decrypt


def generate_key():
    primeLength = 6
    p = get_prime_num(primeLength)
    q = get_prime_num(primeLength)
    while p == q:
        p = get_prime_num(primeLength)
    public, private = key_pair(p, q)
    return public, private

def index(request):
    print(request.method)
    if request.method == "POST":
        print(request.POST)
        obj = World()
        if not World.objects.filter(roomname=request.POST['roomname']):

        
            obj.roomname = request.POST['roomname']
            obj.username = request.POST['username']
            obj.securitylevel = request.POST['securitylevel']
            public, private = generate_key()
            obj.privatekey1 = private[0]
            obj.privatekey2 = private[1]
            obj.publickey1 = public[0]
            obj.publickey2 = public[1]
        #print(obj.privatekey1, obj.privatekey2, obj.publickey1, obj.publickey2)
            obj.save()
        else:
            obj.roomname = request.POST['roomname']
            obj.username = request.POST['username']
            obj.securitylevel = request.POST['securitylevel']
            obj.privatekey1 = World.objects.first().privatekey1
            obj.privatekey2 = World.objects.first().privatekey2
            obj.publickey1 = World.objects.first().publickey1
            obj.publickey2 = World.objects.first().publickey2
        #print(obj.privatekey1, obj.privatekey2, obj.publickey1, obj.publickey2)
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
    publickey1 = getattr(World_obj, 'publickey1')
    publickey2 = getattr(World_obj, 'publickey2')
    privatekey1 = getattr(World_obj, 'privatekey1')
    privatekey2 = getattr(World_obj, 'privatekey2')
    World_obj_security_level= getattr(World_obj, 'securitylevel')
    print("security level: ", World_obj_security_level)
    if World_obj_security_level != "0":
        for m in messages:
            m.content = decrypt(m.content, (privatekey1, privatekey2))

    #field_object = World._meta.get_field('securitylevel')
    
    # print("obtained objects: ", World_obj, World_obj_field_value)
    
    return render(request, 'chat/room' + World_obj_security_level + '.html', {'worldobj': World_obj, 'room_name': room_name, 'username': username, 'messages': messages, 'publickey1': publickey1, 'publickey2': publickey2, 'privatekey1': privatekey1, 'privatekey2': privatekey2})