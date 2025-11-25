from .models import Agregar_categoria, Agregar_Datos
from django import forms
from datetime import timedelta


class agregar_categoriaForm(forms.ModelForm):
    class Meta:
        model = Agregar_categoria
        fields = ['categoria']
        labels = {
            'categoria': 'Nueva Categoria',
        }
        widgets = {
            'categoria': forms.TextInput(attrs={
                'class': 'form-control-categoria',
                'placeholder': 'Aqui agregue su categoria'
            })
             }
        
from django import forms
from .models import Agregar_Datos

class agregar_tiempoForm(forms.ModelForm):
    cantidad = forms.IntegerField(
        label='Cantidad',
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control-tiempo',
            'placeholder': 'Ej. 10'
        })
    )

    UNIDADES = [
        ('seconds', 'Segundos'),
        ('minutes', 'Minutos'),
        ('hours', 'Horas'),
    ]

    unidad = forms.ChoiceField(
        label='Unidad',
        choices=UNIDADES,
        widget=forms.Select(attrs={'class': 'form-control-categoria'})
    )

    class Meta:
        model = Agregar_Datos
        fields = ['categoria']
        labels = {'categoria': 'Categoría'}

    def save(self, commit=True):
        # 1. Asigna la instancia del modelo (instancia del objeto Agregar_Datos)
        instance = super().save(commit=False) # <--- Aquí se define 'instance'
        
        # 2. Obtiene los datos del formulario (cantidad y unidad)
        cantidad = self.cleaned_data['cantidad']
        unidad = self.cleaned_data['unidad']

        # 3. 🔹 Convertir a duración (timedelta) - ¡ESTO DEBE ESTAR INDENTADO CORRECTAMENTE!
        if unidad == 'seconds':
            instance.duracion = timedelta(seconds=cantidad)
        elif unidad == 'minutes':
            instance.duracion = timedelta(minutes=cantidad)
        elif unidad == 'hours':
            instance.duracion = timedelta(hours=cantidad)
        
        # 4. Guardar la instancia si commit=True
        if commit:
            instance.save()
            
        return instance