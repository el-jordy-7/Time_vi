from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import agregar_categoriaForm, agregar_tiempoForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Agregar_categoria, Usuarios, Agregar_Datos
import random

# Create your views here.
def login_home(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        login(request, authenticate(request, username=username, password=password))
        
        return render(request, 'home.html', {'username': username})
    return render(request, 'login_home.html')
#Cerrar sesion

#Registrar Usuarios:
from django.contrib import messages
from django.contrib.auth.models import User

def register_view(request):
    if request.method == 'POST':
        # 1. Obtener los datos del HTML usando los 'name' de los inputs
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        # 2. Validaciones básicas
        if password != password_confirm:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'registro_usuarios.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este correo ya está registrado')
            return render(request, 'registro_usuarios.html')

        if User.objects.filter(username=email).exists():
            messages.error(request, 'Este usuario ya existe')
            return render(request, 'registro_usuarios.html')

        # 3. Crear el usuario (NO será superusuario por defecto)
        # Usamos el email como username para simplificar, ya que tu form no pide username
        try:
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = full_name # Guardamos el nombre completo en first_name
            user.save()
            
            messages.success(request, 'Usuario creado exitosamente. Por favor inicia sesión.')
            return redirect('home') # Asegúrate de que tu URL de login se llame 'login'

        except Exception as e:
            messages.error(request, f'Error al crear usuario: {e}')
            return render(request, 'registro_usuarios.html')

    # Si es GET, solo mostramos el formulario
    return render(request, 'registro_usuarios.html')

from django.core.exceptions import PermissionDenied # 💡 Necesitas esta importación

# ... (Tus otras vistas como login_home, home, etc.)

def access_denied_view(request):
    """Muestra un error 403 (Acceso Denegado)."""
    # Puedes lanzar PermissionDenied para que Django maneje el error 403
    # o simplemente renderizar una plantilla 403 personalizada.
    raise PermissionDenied("Acceso no autorizado al panel de administración.")
def cerrar_sesion(request):
    logout(request)
    return redirect('login_home')

#Importante para la lógica de temporizadores activos
from django.db.models import F, ExpressionWrapper, DateTimeField
from .models import Agregar_Datos 

@login_required
def home(request):
    user_autenticate = request.user
    
    # --- LÓGICA DE TEMPORIZADORES ACTIVOS ---
    now = timezone.now()
    
    timers_activos = Agregar_Datos.objects.annotate(
        fin=ExpressionWrapper(F('tiempo') + F('duracion'), output_field=DateTimeField())
    ).filter(fin__gt=now).order_by('fin')
    total_activos = timers_activos.count()
    timers_visualizar = timers_activos[:2]

    context = {
        'user_autenticate': user_autenticate,
        'timers_activos': timers_visualizar,
        'contador_activos': total_activos,
    }
    return render(request, 'home.html', context, content_type='text/html')


def agregar_categoria(request): 

    ultimas_categorias = Agregar_categoria.objects.order_by('-id')[:2]
    if request.method == 'POST':
        form = agregar_categoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = agregar_categoriaForm()
    return render(request, 'agregar_categoria.html', {'form': form ,
                                                      'ultimas_categorias': ultimas_categorias})
def vista_agregar_tiempo(request):
    """Maneja la creación del nuevo temporizador y redirige al contador."""
    if request.method == 'POST':
        form = agregar_tiempoForm(request.POST)
        if form.is_valid():
            timer = form.save(commit=False)
            timer.tiempo = timezone.now() # Momento de inicio
            timer.save()
            
            # 💡 Redirige correctamente a la vista 'contador_tiempo'
            # Usamos 'pk' porque así está definido en tu urls.py
            return redirect('contador_tiempo', pk=timer.pk) 
            
    else:
        form = agregar_tiempoForm()
        
    return render(request, 'start_tiempo.html', {'form': form})

# views.py (Se mantiene la lógica, solo para referencia)
def contador_tiempo(request, pk):
    """Muestra la página con el temporizador corriendo."""
    timer = get_object_or_404(Agregar_Datos, pk=pk)
    
    tiempo_finalizacion = timer.tiempo + timer.duracion
    ahora = timezone.now()
    tiempo_restante = tiempo_finalizacion - ahora
    
    # Esta variable es la clave: tiempo restante en milisegundos
    tiempo_restante_ms = max(0, int(tiempo_restante.total_seconds() * 1000))

    contexto = {
        'timer': timer,
        'tiempo_restante_ms': tiempo_restante_ms, # Renombramos para mayor claridad en el HTML
    }
    
    # ⚠️ Asegúrate de que este sea el nombre real de tu plantilla
    return render(request, 'tiempo_corriendo.html', contexto)
def Muy_Pronto(request):
    return render(request, 'muy_pronto.html')