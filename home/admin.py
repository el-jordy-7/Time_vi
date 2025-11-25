from django.contrib import admin

# Register your models here.
class UsuariosAdmin(admin.ModelAdmin):
    list_display = ('name', 'password')