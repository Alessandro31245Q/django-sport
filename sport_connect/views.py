from cProfile import Profile
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from sports.models import Amistad, Category, Court, Message
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .forms import ProfileEditForm
from django.contrib.auth.models import User
from django.db.models import Q


def home(request):
    courts = Court.objects.filter(is_featured = True).order_by('-update_at')

    context = {
        'featured_courts' : courts
    }
    return render(request, 'home.html', context)

def custom_404_view(request, exception):
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('register')
        else:
            messages.error(request, 'No se pudo completar el registro. Verifique los datos e intente nuevamente.')
    else: 
        form = RegistrationForm()
    context = {
        'form' : form
    }
    return render(request, 'register.html', context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
            return redirect('home')
    
    form = AuthenticationForm()
    context = {
        'form':form
    }
    return render(request, 'login.html', context)

def logout(request):
    auth.logout(request)
    return redirect('home')

@login_required(login_url='/') 
def profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)  
        if form.is_valid():
            form.save()  
            return redirect('profile')  
    else:
        form = ProfileEditForm(instance=request.user)  

    return render(request, 'profile.html', {'form': form})

@login_required(login_url='/') 
def all_users(request):
    if request.user.is_superuser:

        users = User.objects.all()
        return render(request, 'usuarios.html', {'users': users})
    else:

        return redirect('home')


@login_required(login_url='/') 
def create_user(request):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos suficientes para crear un usuario.')
        return redirect('home')  # O redirige a donde quieras
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('all_users')  # Redirige al listado de usuarios o donde necesites
        else:
            messages.error(request, 'Hubo un error al crear el usuario. Verifica los datos.')
    else:
        form = RegistrationForm()

    return render(request, 'create_user.html', {'form': form})

@login_required(login_url='/') 
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to edit this user.')
        return redirect('all_users')

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully!')
            return redirect('all_users') 
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileEditForm(instance=user)

    return render(request, 'edit_user.html', {'form': form, 'user': user})

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    # Verificar que el usuario logueado sea el administrador
    if request.user.is_superuser:
        user.delete()
        messages.success(request, 'User deleted successfully!')
        return redirect('all_users')
    else:
        messages.error(request, 'You are not authorized to delete this user.')
        return redirect('all_users')
    
@login_required(login_url='/') 
def view_users(request):
    # Obtener todos los usuarios registrados, excluyendo al usuario actual
    users = User.objects.exclude(id=request.user.id)
    context = {
        'users': users
    }
    return render(request, 'view_users.html', context)


def add_friend(request, user_id):
    try:
        # Obtén el usuario que está siendo agregado
        user_to_add = User.objects.get(id=user_id)
        
        # Asegúrate de que el usuario actual y el usuario a agregar no sean la misma persona
        if user_to_add == request.user:
            return redirect('some_view_name')  # Redirige si intentan agregar a sí mismos como amigos

        # Crea una nueva amistad en la base de datos
        amistad = Amistad.objects.create(usuario1=request.user, usuario2=user_to_add)
        amistad.save()

        # Redirige al usuario después de agregar al amigo
        return redirect('some_view_name')  # Cambia esto a la vista que quieras mostrar después

    except User.DoesNotExist:
        return render(request, 'error_page.html', {'error': 'Usuario no encontrado'})

@login_required(login_url='/') 
def send_message(request, user_id):
    # Obtener al usuario al que se enviará el mensaje
    receiver = User.objects.get(id=user_id)
    sender = request.user

    # Obtener la conversación entre el usuario actual (sender) y el receptor
    messages = Message.objects.filter(
        (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
    ).order_by('timestamp')

    if request.method == 'POST':
        # Obtener el mensaje enviado desde el formulario
        message_content = request.POST.get('message')
        
        # Guardar el mensaje en la base de datos
        message = Message(sender=sender, receiver=receiver, content=message_content)
        message.save()

        # Redirigir a la misma página para ver el mensaje enviado
        return redirect('send_message', user_id=user_id)

    return render(request, 'send_message.html', {
        'receiver': receiver,
        'messages': messages,
    })

@login_required(login_url='/') 
def delete_message(request, message_id):
    # Obtén el mensaje y verifica que sea del usuario actual
    message = Message.objects.get(id=message_id)
    if message.sender == request.user:
        message.delete()  # Elimina el mensaje de la base de datos
    
    # Redirige a la conversación (a la vista send_message) con el receptor del mensaje
    return redirect('send_message', user_id=message.receiver.id)

