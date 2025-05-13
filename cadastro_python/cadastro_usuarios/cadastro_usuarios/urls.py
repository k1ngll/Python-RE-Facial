
from django.contrib import admin
from django.urls import path
from app_cad_usuarios import views
from django.conf.urls.static import static
from django.conf import settings

#Cria os caminhos da aplicação
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.cadastrar_usuario,name='cadastrar_usuario'),
    path('demo/', views.demonstracao, name='demo'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
