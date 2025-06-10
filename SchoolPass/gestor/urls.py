from django.urls import path
from . import views


app_name = 'gestor'


urlpatterns = [
    path('home/', views.home, name='home'),
    path('cadastro_gestor/', views.cadastro_gestor, name='cadastro_gestor'),
    path('tela_gestor/', views.tela_gestor, name='tela_gestor'),
    path('editar_grade/', views.editar_grade, name='editar_grade'),
    path('logout/', views.sair_conta, name='logout'),
]