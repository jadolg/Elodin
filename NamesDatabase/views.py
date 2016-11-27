import re

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from NamesDatabase.models import Name, Log
from django.contrib import messages


@login_required
def index(request):
    if request.method == 'POST':
        if request.POST.has_key('nombre') and request.POST.has_key('ip'):
            nombre = request.POST['nombre']
            if not str(nombre).endswith('.'):
                nombre += '.'
            ip = request.POST['ip']

            if len(Name.objects.filter(nombre=nombre)) > 0:
                messages.add_message(request, messages.ERROR,"Ya existe este registro. Cree uno nuevo o elimine el anterior")
            else:
                if re.match(r'(?:[0-9]{1,3}\.){3}[0-9]{1,3}', ip):
                    try:
                        Name(nombre=nombre,ip=ip).save()
                        Log(usuario=request.user.username, accion='agregar', nombre=nombre, ip=ip, ip_usuario=request.META.get('REMOTE_ADDR', None)).save()
                        messages.add_message(request, messages.INFO, "Registro agregado correctamente")
                    except:
                        pass
                else:
                    messages.add_message(request, messages.ERROR,"IP incorrecta")
        else:
            messages.add_message(request, messages.ERROR, "Datos insuficientes para agregar un nuevo registro")
    # messages.add_message(request, messages.INFO, "Utilizar palabras para hablar de palabras es como utilizar un lapiz para hacer un dibujo de ese lapiz sobre ese mismo lapiz. Imposible. Desconcertante. Frustrante. -Elodin. ")
    return render(request, 'index.html', {'names':Name.objects.all()})


@login_required
def logs(request):
    return render(request, 'log.html', {'logs': Log.objects.order_by("-fecha")[:50]})

@login_required
def delete(request,pk):
    try:
        name = Name.objects.get(id=pk)
        Log(usuario=request.user.username, accion='eliminar', nombre=name.nombre, ip=name.ip, ip_usuario=request.META.get('REMOTE_ADDR', None)).save()
        name.delete()
        messages.add_message(request, messages.INFO, "Registro eliminado satisfactoriamente")
    except:
        messages.add_message(request, messages.INFO, "Error eliminando registro")

    return HttpResponseRedirect('/')


def login_user(request):
    if request.user.is_authenticated():
        messages.add_message(request, messages.INFO, "Ya se encuentra autenticado")
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        if request.POST.has_key('user') and request.POST.has_key('password'):
            user = authenticate(username=request.POST['user'], password=request.POST['password'])

            if user is not None:
                login(request, user)
                messages.add_message(request, messages.INFO, "Bienvenido " + user.username)
                return HttpResponseRedirect('/')
            else:
                messages.add_message(request, messages.ERROR,"Credenciales incorrectas")

    return render(request,'login.html')


@login_required
def logout_user(request):
    logout(request)
    messages.add_message(request, messages.INFO, "Ha salido correctamente")
    return HttpResponseRedirect('/')


def signup_user(request):
    if request.method == 'POST':
        if request.POST.has_key('user') and request.POST.has_key('password') and request.POST.has_key('repassword'):
            username = request.POST['user']
            password = request.POST['password']
            repassword = request.POST['repassword']

            if password == repassword:
                if len(User.objects.filter(username=username)) == 0:
                    user = User.objects.create_user(username=username)
                    user.is_active = True
                    user.set_password(password)
                    user.save()
                    messages.add_message(request, messages.INFO, "Usuario " + username+" registrado satisfactoriamente. Por favor autentiquese para continuar")
                    return HttpResponseRedirect('/')
                else:
                    messages.add_message(request, messages.ERROR, "Este usuario ya existe. Si ha olvidado su contrasena por favor contacte a un Administrador")
            else:
                messages.add_message(request, messages.ERROR, "Las contrasenas no coinciden")
        else:
            messages.add_message(request, messages.ERROR, "Provea todos los datos necesarios para registrarse")

    return render(request,'register.html')